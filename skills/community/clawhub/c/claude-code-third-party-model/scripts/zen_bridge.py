#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
zen_bridge.py —— 零依赖单文件桥接：OpenAI 兼容端点  ->  opencode serve 的 SDK API

为什么需要它：
    OpenCode Zen 的免费模型（如 deepseek-v4.1-flash-free）已限制只能在 OpenCode 客户端内调用，
    直连 HTTP 一律返回 FreeTierError。但 opencode 自带的 headless server（`opencode serve`）
    会代理这些请求。本脚本把标准的 OpenAI /v1/chat/completions 请求翻译成 opencode 的 SDK 调用，
    于是任何支持 OpenAI 协议的客户端（WorkBuddy 自定义模型、Claude Code、Cline、curl…）都能用上。

用法：
    python zen_bridge.py                        # 监听 127.0.0.1:8787
    python zen_bridge.py --port 9000            # 换端口
    python zen_bridge.py --model deepseek-v4.1-flash-free
    python zen_bridge.py --sdk-port 41234 --auto-start

可选的客户端配置（以 WorkBuddy 为例，models.json 里加一条）：
    {"id":"deepseek-v4.1-flash-free","name":"DS V4.1 Flash Free",
     "vendor":"opencode","url":"http://127.0.0.1:8787/v1/chat/completions",
     "apiKey":"sk-local","supportsToolCall":false,"supportsImages":true,"supportsReasoning":true}

已知限制：
    * stream=true 且请求不带 tools 时走「prompt_async + /event」真增量流式（2026-10-18 起）：
      首字延迟从「整段返回完」提前到「第一批增量到达」。增量按上游网络块批量下发，
      不是逐 token；订阅/协议异常时自动降级为整段返回，语义不变。
      等待期每 15s 发 SSE 注释心跳（防中间链路读超时）；
      中途失败由 session.error / assistant message.error 秒级检测，不干等超时。
    * 带 tools 的请求（agent 循环）仍走同步整段：工具调用要靠提示词模拟解析，
      流式吐到一半才发现是工具调用会同时吐出正文 JSON，反而更糟。
    * OpenAI 的 tools / function calling 不透传（opencode 自己会不会调工具由它的 agent 决定）
    * 每次请求默认新建 session 并在结束后删除，因此跨请求不保留上下文；
      客户端需要靠 messages 数组自带历史（桥接会把历史拼成带 role 前缀的文本）
    * 依赖 opencode serve 在跑；可加 --auto-start 让它自己拉起
"""

import argparse
import atexit
import http.client
import json
import mimetypes
import os
import queue
import re
import subprocess
import sys
import threading
import time
import urllib.parse
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PROVIDER = "opencode"
# 默认模型换成实测最快最稳的 space-bunny-free（2026-10-18 延迟实测 1.8s，
# 且代码/逻辑质量在线；deepseek-v4.1-flash-free 时快时慢，偶发 60s+ 超时）。
# ccproxy 各 profile 都会显式传 model，这个默认值只影响不指定模型的直连请求。
DEFAULT_MODEL = "space-bunny-free"
# opencode 里可用的免费模型，只用于 /v1/models 展示，实际转发不限制。
# 2026-10-18 按 Zen 实时目录 + 桥接实测重校：
#   - 只列实测能用的；已死的留在注释里备查，别默认推荐。
#   - space-bunny-free：最快 ~1.8s，质量在线，首选。
#   - deepseek-v4.1-flash-free：能用但不稳（2.8s~22s+，偶发超时）。
#   - glm-5.3-flash-free：能用+工具模拟✅，但慢（代码 14.6s / 逻辑题 75s）。
#   - 实测不可用：ll-alpha-free 502、jev-1.13-free 502、beam-free 71s 无输出、
#     nemotron-3.5-lightning-free 超时、cat-jam-free / muse-spark-*-contributor-free 地区封锁。
KNOWN_FREE = [
    "space-bunny-free",
    "deepseek-v4.1-flash-free",
    "big-pickle",
    "nemotron-3.5-super-vl-free",
    "longcat-2.5-preview-free",
    "mimo-v2.6-flash-free",
    "glm-5.3-flash-free",
]


def log(msg):
    print("[%s] %s" % (time.strftime("%H:%M:%S"), msg), flush=True)


class OpencodeSDK:
    """薄封装：本地 opencode serve 的 REST SDK。"""

    def __init__(self, port, auto_start=False, opencode_bin=None, agent=None,
                 keep_session=False, max_inflight=4, stream_ok=True, timeout=600):
        self.port = port
        self.auto_start = auto_start
        self.opencode_bin = opencode_bin
        self.agent = agent
        self.keep_session = keep_session
        self.timeout = timeout   # 单次上游调用超时；推理模型思考 75s+，别设太小
        # 并发上限：opencode serve 是单进程，并行 session 太多会互相拖慢
        self._sem = threading.BoundedSemaphore(max(1, max_inflight))
        self.stream_ok = stream_ok
        # 只保护「建/复用 session」这一小段临界区（原先是全程持锁，请求被串行化）
        self._sess_lock = threading.Lock()
        self._session_id = None
        self._proc = None
        atexit.register(self._cleanup)

    def _cleanup(self):
        """退出时收掉由本进程拉起的 opencode serve。"""
        if self._proc and self._proc.poll() is None:
            log("关闭 opencode serve (pid=%s)" % self._proc.pid)
            try:
                self._proc.terminate()
                self._proc.wait(timeout=10)
            except Exception:
                try:
                    self._proc.kill()
                except Exception:
                    pass

    # ---------- 底层请求 ----------
    def _req(self, method, path, body=None, timeout=600):
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=timeout)
        headers = {"Accept": "application/json"}
        data = None
        if body is not None:
            data = json.dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json"
        try:
            conn.request(method, path, body=data, headers=headers)
            resp = conn.getresponse()
            raw = resp.read().decode("utf-8", "replace")
            status = resp.status
        finally:
            conn.close()
        return status, raw

    # ---------- 服务存活 / 拉起 ----------
    def alive(self):
        try:
            conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=3)
            conn.request("GET", "/session")
            conn.getresponse().read()
            conn.close()
            return True
        except Exception:
            return False

    def ensure(self):
        if self.alive():
            return True
        if not self.auto_start:
            log("opencode serve 未在 127.0.0.1:%d 运行，请先在终端执行：opencode serve --port %d"
                % (self.port, self.port))
            return False
        exe = _find_opencode(self.opencode_bin)
        if not exe:
            log("找不到 opencode 可执行文件")
            return False
        log("拉起 opencode serve --port %d ..." % self.port)
        creationflags = 0
        startupinfo = None
        if os.name == "nt":
            creationflags = subprocess.CREATE_NEW_PROCESS_GROUP
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        self._proc = subprocess.Popen(
            [exe, "serve", "--port", str(self.port)],
            stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT,
            creationflags=creationflags, startupinfo=startupinfo,
        )
        for _ in range(120):
            time.sleep(1)
            if self.alive():
                log("opencode serve 已就绪")
                return True
        log("opencode serve 启动超时")
        return False

    def _session_alive(self, sid):
        try:
            st, _ = self._req("GET", "/session/%s" % sid, timeout=10)
            return st == 200
        except Exception:
            return False

    # ---------- 一次对话 ----------
    def _new_session(self, model_id, provider):
        """建会话（keep_session 模式优先复用），返回 sid。"""
        if self.keep_session and self._session_id and self._session_alive(self._session_id):
            return self._session_id
        st, raw = self._req("POST", "/session", {
            "title": "zen-bridge " + time.strftime("%m-%d %H:%M:%S"),
            "model": {"id": model_id, "providerID": provider},
        }, timeout=30)
        if st != 200:
            raise RuntimeError("create session failed: %s %s" % (st, raw[:300]))
        sid = json.loads(raw)["id"]
        if self.keep_session:
            self._session_id = sid
        return sid

    def _delete_session(self, sid):
        """顺手清理会话，避免 opencode 本地库不断膨胀（keep_session 模式保留）。"""
        if self.keep_session:
            return
        try:
            self._req("DELETE", "/session/%s" % sid, timeout=15)
        except Exception:
            pass

    def _prompt_body(self, model_id, openai_parts, system_text, provider, agent):
        body = {
            "parts": openai_parts,
            "model": {"providerID": provider, "modelID": model_id},
        }
        if system_text:
            body["system"] = system_text
        agent = agent or self.agent
        if agent:
            body["agent"] = agent
        return body

    def complete(self, model_id, openai_parts, system_text, agent=None,
                 provider=None):
        """同步版：整段返回 (assistant_text, usage_dict)。

        只锁 session 创建那一小段；上游调用期间不持锁，多请求可并行
        （总量由 self._sem 控制，见 --max-inflight）。
        """
        provider = provider or PROVIDER
        with self._sem:
            with self._sess_lock:
                sid = self._new_session(model_id, provider)
            try:
                body = self._prompt_body(model_id, openai_parts, system_text,
                                         provider, agent)
                st, raw = self._req("POST", "/session/%s/message" % sid, body,
                                    timeout=self.timeout)
                try:
                    msg = json.loads(raw)
                except Exception:
                    raise RuntimeError("bad upstream response: %s" % raw[:300])
                if st != 200:
                    raise RuntimeError("message failed: HTTP %s %s" % (st, raw[:300]))
                parts = msg.get("parts") or []
                texts = [p.get("text", "") for p in parts if p.get("type") == "text"]
                answer = "".join(texts).strip()
                tokens = msg.get("info", {}).get("tokens", {}) or {}
            finally:
                self._delete_session(sid)
        usage = {
            "prompt_tokens": tokens.get("input", 0),
            "completion_tokens": tokens.get("output", 0),
            "total_tokens": tokens.get("total", 0) or (
                tokens.get("input", 0) + tokens.get("output", 0)),
        }
        return answer, usage

    def complete_stream(self, model_id, openai_parts, system_text, agent=None,
                        provider=None, on_delta=None, on_heartbeat=None,
                        timeout=None):
        """流式版：prompt_async + 订阅 /event，增量经 on_delta 回调实时吐出。

        返回 (assistant_text, usage_dict)。
        - 请求发出前的失败抛 _PrePromptError：调用方可安全降级到同步 complete()，
          不会重复提问（prompt 还没发）。
        - 请求已发出后的失败抛 RuntimeError（此时重问会双倍计费/双倍回复）。
        """
        provider = provider or PROVIDER
        timeout = timeout or self.timeout
        with self._sem:
            with self._sess_lock:
                sid = self._new_session(model_id, provider)
            tap = _EventTap(self.port, sid, timeout=timeout)
            try:
                tap.start()
            except Exception as e:
                self._delete_session(sid)
                raise _PrePromptError("event subscribe failed: %s" % e)
            try:
                body = self._prompt_body(model_id, openai_parts, system_text,
                                         provider, agent)
                st, raw = self._req("POST", "/session/%s/prompt_async" % sid, body,
                                    timeout=60)
                if st not in (200, 201, 202, 204):
                    raise _PrePromptError("prompt_async failed: HTTP %s %s"
                                          % (st, raw[:200]))
                answer, usage, note = tap.collect(on_delta, on_heartbeat)
                if not answer:
                    # 增量没拿到（协议抖动）：回读会话兜底，不重复问模型
                    try:
                        answer, usage = self._read_back(sid)
                    except Exception:
                        pass
                if not answer:
                    raise RuntimeError(note or "empty upstream response")
                return answer, usage
            finally:
                tap.stop()
                self._delete_session(sid)

    def _read_back(self, sid):
        """回读会话里最后一条 assistant 消息（流式增量丢失时的兜底）。"""
        st, raw = self._req("GET", "/session/%s/message" % sid, timeout=30)
        if st != 200:
            raise RuntimeError("read back failed: HTTP %s" % st)
        data = json.loads(raw)
        msgs = data if isinstance(data, list) else [data]
        last = None
        for m in msgs:
            if (m.get("info") or m).get("role") == "assistant":
                last = m
        if last is None:
            raise RuntimeError("no assistant message in session")
        parts = last.get("parts") or []
        texts = [p.get("text", "") for p in parts if p.get("type") == "text"]
        tokens = (last.get("info") or {}).get("tokens", {}) or {}
        usage = {
            "prompt_tokens": tokens.get("input", 0),
            "completion_tokens": tokens.get("output", 0),
            "total_tokens": tokens.get("total", 0) or (
                tokens.get("input", 0) + tokens.get("output", 0)),
        }
        return "".join(texts).strip(), usage


class _PrePromptError(Exception):
    """prompt 还没发出去就失败了——调用方可安全降级到同步 complete()。"""


def _err_msg(err):
    """从 opencode 的 error 对象里抠出可读消息（各 error schema 形状不一）。"""
    if not isinstance(err, dict):
        return str(err)[:200]
    data = err.get("data") or {}
    if isinstance(data, dict) and data.get("message"):
        return str(data["message"])[:200]
    if err.get("message"):
        return str(err["message"])[:200]
    if err.get("name"):
        return str(err["name"])
    return json.dumps(err, ensure_ascii=False)[:200]


class _EventTap:
    """一次性订阅 opencode /event，只收集某个 session 的文本增量。

    /event 是全局广播（所有 session 的事件都流经这里），按 properties.sessionID
    过滤。文本增量是 message.part.delta(field='text')，完成信号是 session.status
    的 busy -> idle（订阅在 prompt_async 之前建立，不会错过）。
    """

    def __init__(self, port, sid, timeout=600):
        self.port = port
        self.sid = sid
        self.timeout = timeout
        self.q = queue.Queue()
        self._stop = threading.Event()
        self._conn = None
        self._thread = None

    def start(self):
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self):
        self._stop.set()
        conn = self._conn
        if conn is not None:
            try:
                conn.close()   # 让阻塞在 readline 的读取线程立刻退出
            except Exception:
                pass

    def _run(self):
        conn = None
        try:
            conn = http.client.HTTPConnection("127.0.0.1", self.port,
                                              timeout=self.timeout)
            conn.request("GET", "/event", headers={"Accept": "text/event-stream"})
            resp = conn.getresponse()
            self._conn = conn
            buf = b""
            saw_busy = False
            while not self._stop.is_set():
                line = resp.readline()
                if not line:
                    self.q.put(("end", "event stream EOF"))
                    return
                buf += line
                if not buf.endswith(b"\n\n"):
                    continue
                s = buf.decode("utf-8", "replace")
                buf = b""
                if s.startswith(":") or not s.startswith("data: "):
                    continue   # 心跳注释 / 非 data 行
                try:
                    e = json.loads(s[6:])
                except Exception:
                    continue
                p = e.get("properties") or {}
                if p.get("sessionID") != self.sid:
                    continue
                t = e.get("type")
                if t == "message.part.delta":
                    if p.get("field") == "text":
                        d = p.get("delta") or ""
                        if d:
                            self.q.put(("delta", d))
                elif t == "message.updated":
                    info = p.get("info") or {}
                    if info.get("role") == "assistant":
                        # 中途失败（限流/GEO/内容过长等）：秒级报错，别傻等 idle
                        if info.get("error"):
                            self.q.put(("end", "upstream error: %s"
                                        % _err_msg(info["error"])))
                            return
                        if info.get("tokens"):
                            tk = info["tokens"]
                            self.q.put(("usage", {
                                "prompt_tokens": tk.get("input", 0),
                                "completion_tokens": tk.get("output", 0),
                                "total_tokens": tk.get("total", 0) or (
                                    tk.get("input", 0) + tk.get("output", 0)),
                            }))
                elif t == "session.error":
                    # 会话级错误事件：同上，fail fast
                    self.q.put(("end", "session error: %s"
                                % _err_msg(p.get("error"))))
                    return
                elif t == "session.status":
                    # 状态有 busy / retry / idle 三种。只有 idle 才算真结束：
                    # retry 是上游在重试（免费池限流很常见，实测 glm-5.3 会
                    # busy->retry 反复好几次），把 retry 当结束会提前断流、返回空回复。
                    st = (p.get("status") or {}).get("type")
                    if st == "busy":
                        saw_busy = True
                    elif st == "idle" and saw_busy:
                        self.q.put(("end", ""))
                        return
        except Exception as e:
            self.q.put(("end", "event tap error: %s" % e))
        finally:
            if conn is not None:
                try:
                    conn.close()
                except Exception:
                    pass

    def collect(self, on_delta=None, on_heartbeat=None, heartbeat_gap=15.0):
        """阻塞收集到会话空闲。返回 (text, usage, note)。

        - on_delta 写客户端失败会抛异常直接穿出去（客户端已断开，没必须继续收）。
        - 上游思考期没有增量（推理模型能静默 60s+）：每 heartbeat_gap 秒调一次
          on_heartbeat，让中间链路（ccproxy 等）的连接保持存活，防读超时。
        """
        deadline = time.time() + self.timeout
        chunks = []
        usage = {}
        note = ""
        last_out = time.time()
        while True:
            remain = deadline - time.time()
            if remain <= 0:
                note = "stream timeout after %ds" % self.timeout
                break
            try:
                item = self.q.get(timeout=min(remain, 0.5))
            except queue.Empty:
                if on_heartbeat is not None and time.time() - last_out >= heartbeat_gap:
                    on_heartbeat()
                    last_out = time.time()
                continue
            kind = item[0]
            if kind == "delta":
                chunks.append(item[1])
                if on_delta is not None:
                    on_delta(item[1])
                last_out = time.time()
            elif kind == "usage":
                usage = item[1]
            else:  # end
                note = item[1] if len(item) > 1 else ""
                break
        return "".join(chunks), usage, note


def _find_opencode(user_supplied=None):
    """定位 opencode 可执行文件。"""
    if user_supplied and os.path.isfile(user_supplied):
        return user_supplied
    exe = "opencode.exe" if os.name == "nt" else "opencode"
    from shutil import which
    found = which(exe)
    if found:
        return found
    home = os.path.expanduser("~")
    cand = os.path.join(home, ".opencode", "bin", exe)
    if os.path.isfile(cand):
        return cand
    return None


# ---------------- OpenAI 请求 -> opencode parts ----------------

TOOL_INSTRUCTION = """You have access to the following tools:
{tools}

Rules for tool use:
- If the request should be answered by calling tool(s), reply with EXACTLY ONE line of JSON and nothing else, in this shape:
  {{"calls":[{{"id":"call_1","name":"<tool_name>","arguments":{{<object matching that tool's parameters>}}}}]}}
- Put multiple objects inside "calls" if several calls are needed.
- Arguments must be a JSON object; use exact parameter names from the tool definition.
- If the conversation already contains "tool result for <id>:" lines, those calls have ALREADY run —
  use their content to answer in plain language. Never call the same tool with the same arguments twice.
- If no tool fits, or the answer needs no tool, reply in plain natural language instead.
- Never invent a tool name that is not in the list above.
- Do NOT wrap the JSON in code fences."""

_FENCE_RE = re.compile(r"^```(?:json|JSON)?\s*|\s*```$")


def build_tools_digest(tools):
    """OpenAI tools 数组 -> 给模型看的精简清单（控制长度，别把上下文撑爆）。"""
    items = []
    for t in tools:
        fn = t.get("function", t)
        name = fn.get("name")
        if not name:
            continue
        desc = (fn.get("description") or "").strip().replace("\n", " ")
        params = fn.get("parameters") or {}
        compact = params
        # 只保留最有用的字段，properties 里的说明省略
        if isinstance(params, dict) and "properties" in params:
            props = {}
            for k, v in (params.get("properties") or {}).items():
                if isinstance(v, dict):
                    props[k] = v.get("type", "any") + (
                        " // " + v.get("description", "") if v.get("description") else "")
                else:
                    props[k] = v
            compact = {"type": params.get("type", "object"),
                       "properties": props,
                       "required": params.get("required", [])}
        items.append({"name": name, "description": desc[:200],
                      "parameters": compact})
    digest = json.dumps(items, ensure_ascii=False)
    if len(digest) > 4000:
        digest = digest[:4000] + "...(truncated)"
    return digest


def _with_tool_prefix(parts, prefix):
    """把工具指令前置到用户正文里（不能放 system，会被 agent 提示压掉）。"""
    out = []
    injected = False
    for p in parts:
        if p.get("type") == "text" and not injected:
            out.append({"type": "text",
                        "text": prefix + "\n\nUser request:\n" + p.get("text", "")})
            injected = True
        else:
            out.append(p)
    if not injected:
        out.append({"type": "text", "text": prefix + "\n\nUser request:\n(empty)"})
    return out


def extract_first_json(text):
    """扫出文本里第一个完整的 JSON 对象/数组。

    不能简单用 find('{') / find('[') 切：那样会截到串内部的下标导致 JSON 损坏
    （踩过：JSON 以 '{' 开头，却因为内部有 '[' 被从中间切断 -> json.loads 报 Extra data）。
    用 raw_decode 逐个起点尝试最稳。
    """
    dec = json.JSONDecoder()
    for i, ch in enumerate(text):
        if ch in "{[":
            try:
                obj, _ = dec.raw_decode(text[i:])
                return obj
            except Exception:
                continue  # 这个起点不是完整 JSON，换下一个
    return None


def repair_json_text(text):
    """模型 JSON 常见毛病的本地修复（修复成功就能省掉一次上游重试 = 省一倍延迟）。

    修三样（合法 JSON 经过这些变换保持逐字节不变，所以可以直接无脑跑）：
      1. 对象/数组里的尾逗号：{"a":1,} -> {"a":1}
      2. 字符串里的裸换行/制表符：转义成 \\n / \\t
      3. 尾部缺失的闭合括号：{"calls":[{...} -> 补齐 }] 或 }
    """
    out = []
    in_str = False
    esc = False
    for ch in text:
        if esc:
            out.append(ch)
            esc = False
            continue
        if ch == "\\" and in_str:
            out.append(ch)
            esc = True
            continue
        if ch == '"':
            in_str = not in_str
            out.append(ch)
            continue
        if in_str:
            if ch == "\n":
                out.append("\\n")
                continue
            if ch == "\r":
                continue
            if ch == "\t":
                out.append("\\t")
                continue
        out.append(ch)
    t = "".join(out)
    t = re.sub(r",(\s*[}\]])", r"\1", t)
    stack = []
    in_str = False
    esc = False
    for ch in t:
        if esc:
            esc = False
            continue
        if ch == "\\" and in_str:
            esc = True
            continue
        if ch == '"':
            in_str = not in_str
            continue
        if in_str:
            continue
        if ch in "{[":
            stack.append(ch)
        elif ch in "}]" and stack:
            stack.pop()
    while stack:
        t += "}" if stack.pop() == "{" else "]"
    return t


def parse_tool_calls(text, valid_names):
    """从模型回复里尽力抠出工具调用，返回 OpenAI 的 tool_calls 列表（失败返回 []）。

    两阶段：原文直接解 → 解不开再修复常见毛病后重解（repair 对合法 JSON 是幂等的）。
    """
    cand = text.strip()
    cand = _FENCE_RE.sub("", cand).strip()
    obj = extract_first_json(cand)
    if obj is None:
        obj = extract_first_json(repair_json_text(cand))
    if obj is None:
        return []

    if isinstance(obj, dict):
        raw_calls = obj.get("calls") or [obj]
    elif isinstance(obj, list):
        raw_calls = obj
    else:
        return []

    out = []
    for idx, c in enumerate(raw_calls, 1):
        if not isinstance(c, dict):
            continue
        name = c.get("name")
        if name not in valid_names:
            continue
        args = c.get("arguments", {})
        if isinstance(args, str):
            try:
                args = json.loads(args)
            except Exception:
                return []
        if not isinstance(args, dict):
            continue
        out.append({
            "id": c.get("id") or ("call_%d" % idx),
            "type": "function",
            "function": {"name": name, "arguments": json.dumps(args, ensure_ascii=False)},
        })
    return out


def _text_of(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        buf = []
        for item in content:
            if not isinstance(item, dict):
                continue
            t = item.get("type")
            if t == "text":
                buf.append(item.get("text", ""))
            elif t in ("input_text", "output_text"):
                buf.append(item.get("text", ""))
        return "\n".join(buf)
    return "" if content is None else str(content)


def _image_parts_from(content):
    """把 OpenAI content 里的图片抽成 opencode 的 file part。"""
    out = []
    if not isinstance(content, list):
        return out
    for item in content:
        if not isinstance(item, dict):
            continue
        if item.get("type") != "image_url":
            continue
        url = (item.get("image_url") or {}).get("url", "")
        if not url:
            continue
        if url.startswith("data:"):
            mime = url.split(";", 1)[0][5:]
            out.append({"type": "file", "mime": mime or "image/png", "url": url})
        else:
            mime, _ = mimetypes.guess_type(url.split("?")[0])
            out.append({"type": "file", "mime": mime or "image/jpeg", "url": url})
    return out


def split_model(raw, default_provider=None):
    """'provider/model' -> (model, provider)；无前缀时 provider 为 None。

    只按**第一个**斜杠切分，因此 'deepinfra/anthropic/claude-fable-5' 能正确拆成
    provider='deepinfra' + model='anthropic/claude-fable-5'（模型 id 自身含斜杠）。
    'opencode/xxx' 这类显式前缀也照此处理；纯模型名则交给调用方的默认值。
    """
    raw = (raw or "").strip()
    if "/" in raw:
        prov, _, model = raw.partition("/")
        if prov and model:
            return model, prov
    return raw, default_provider


def build_payload(body, default_provider=None):
    """OpenAI body -> (parts, system_text, model_id, stream, tools, provider)"""
    messages = body.get("messages") or []
    raw_model = body.get("model") or DEFAULT_MODEL
    model_id, provider = split_model(raw_model, default_provider)

    system_chunks, turns, images = [], [], []
    for m in messages:
        role = m.get("role", "user")
        content = m.get("content")
        txt = _text_of(content)
        if role == "system":
            if txt:
                system_chunks.append(txt)
            continue
        # 助手发起工具调用这条消息，content 通常是 null——必须在 if txt 之外处理，
        # 否则整条调用记录会从历史里消失，模型看到「提问 + 孤立工具结果」会重复调
        # 同一个工具（实测第二轮必复现，这是 agent 循环跑不起来的主因）。
        if role == "assistant" and m.get("tool_calls"):
            calls = []
            for tc in m["tool_calls"]:
                fn = tc.get("function") or {}
                calls.append("%s(%s)" % (fn.get("name", "?"), fn.get("arguments", "")))
            turns.append("assistant: called %s%s" % (
                " ; ".join(calls), ("  [say] " + txt) if txt else ""))
            continue
        if txt:
            if role == "tool":
                turns.append("tool result%s: %s" % (
                    " for " + m.get("tool_call_id", "") if m.get("tool_call_id") else "", txt))
            else:
                turns.append("%s: %s" % (role, txt))
        images.extend(_image_parts_from(content))

    parts = list(images)
    tools = body.get("tools") or []
    prompt = "\n\n".join(turns).strip()
    if prompt:
        parts.append({"type": "text", "text": prompt})

    if not parts:
        parts.append({"type": "text", "text": "hello"})

    stream = bool(body.get("stream"))
    return parts, "\n\n".join(system_chunks).strip(), model_id, stream, tools, provider


# ---------------- HTTP 服务 ----------------

class Handler(BaseHTTPRequestHandler):
    server_version = "zen-bridge/1.1"
    sdk = None            # type: OpencodeSDK
    default_model = DEFAULT_MODEL
    default_provider = PROVIDER

    def _send(self, code, obj, stream=False):
        if stream:
            # 不写 Content-Length / keep-alive：handler 返回后连接自动关闭（HTTP/1.0），
            # 客户端以 EOF 作为流结束信号。少了这一步，客户端会一直空等到超时。
            self.send_response(code)
            self.send_header("Content-Type", "text/event-stream; charset=utf-8")
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            return
        data = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _sse(self, obj):
        chunk = "data: " + json.dumps(obj, ensure_ascii=False) + "\n\n"
        self.wfile.write(chunk.encode("utf-8"))
        self.wfile.flush()

    def _read_body(self):
        length = int(self.headers.get("Content-Length") or 0)
        if length <= 0:
            return {}
        raw = self.rfile.read(length)
        try:
            return json.loads(raw.decode("utf-8"))
        except Exception:
            return {}

    # ---- 路由 ----
    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path
        if path in ("/", "/healthz", "/health"):
            self._send(200, {
                "ok": self.sdk.alive(),
                "bridge_model": self.default_model,
                "bridge_provider": self.default_provider,
                "upstream": "http://127.0.0.1:%d" % self.sdk.port,
            })
        elif path == "/v1/models":
            data = [{
                "id": m, "object": "model", "created": 0,
                "owned_by": self.default_provider,
            } for m in [self.default_model] + [x for x in KNOWN_FREE if x != self.default_model]]
            self._send(200, {"object": "list", "data": data})
        else:
            self._send(404, {"error": {"message": "not found: " + path}})

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.end_headers()

    def do_POST(self):
        path = urllib.parse.urlparse(self.path).path
        if path not in ("/v1/chat/completions", "/chat/completions"):
            self._send(404, {"error": {"message": "not found: " + path}})
            return

        body = self._read_body()
        try:
            parts, system_text, model_id, stream, tools, provider = build_payload(
                body, self.default_provider)
        except Exception as e:
            self._send(400, {"error": {"message": "bad request: %s" % e}})
            return

        # 工具模拟：把 tools 清单塞进 system 提示，让模型按要求吐 JSON
        # 注意：指令必须放进**用户消息正文**而不是 system 字段 ——
        # 实测 system 会被 opencode agent 自己的提示压掉，模型会转头去用它内置的工具。
        valid_names = []
        if tools:
            digest = build_tools_digest(tools)
            valid_names = [n for n in
                           [t.get("function", t).get("name") for t in tools] if n]
            prefix = TOOL_INSTRUCTION.format(tools=digest)
            parts = _with_tool_prefix(parts, prefix)

        t0 = time.time()
        try:
            if not self.sdk.ensure():
                self._send(503, {"error": {
                    "message": "opencode serve unavailable on port %d" % self.sdk.port}})
                return

            # ---- 真流式路径：无 tools 的 stream 请求（聊天场景，打字机效果）----
            # 带 tools 的请求不走流式：工具调用是提示词模拟的，吐到一半才发现是
            # 工具调用会同时泄出正文 JSON，不如整段回来再判。
            if stream and not tools and getattr(self.sdk, "stream_ok", False):
                self._send(200, None, stream=True)
                cid = "chatcmpl-" + uuid.uuid4().hex[:24]
                ts = int(time.time())

                def emit(delta, finish=None, usage=None):
                    obj = {"id": cid, "object": "chat.completion.chunk",
                           "created": ts, "model": model_id,
                           "choices": [{"index": 0, "delta": delta,
                                        "finish_reason": finish}]}
                    if usage is not None:
                        obj["usage"] = usage
                    self._sse(obj)

                emit({"role": "assistant"})
                degraded = False
                try:
                    answer, usage = self.sdk.complete_stream(
                        model_id, parts, system_text, provider=provider,
                        on_delta=lambda d: emit({"content": d}),
                        on_heartbeat=self._heartbeat)
                except _PrePromptError as e:
                    # prompt 还没发出去：安全降级成同步整段（行为同旧版）
                    log("流式降级: %s" % e)
                    degraded = True
                except Exception as e:
                    log("ERROR(stream) %s" % e)
                    self._stream_error(str(e))
                    return
                if degraded:
                    try:
                        answer, usage = self.sdk.complete(model_id, parts,
                                                          system_text,
                                                          provider=provider)
                    except Exception as e:
                        log("ERROR %s" % e)
                        self._stream_error(str(e))
                        return
                    emit({"content": answer})
                emit({}, "stop", usage)
                self.wfile.write(b"data: [DONE]\n\n")
                self.wfile.flush()
                log("%s  %.1fs  in=%s out=%s  [stream%s]" % (
                    model_id, time.time() - t0, usage["prompt_tokens"],
                    usage["completion_tokens"],
                    "-degraded" if degraded else ""))
                return

            # ---- 同步路径：整段返回（agent 循环 / 非流式请求）----
            answer, usage = self.sdk.complete(model_id, parts, system_text,
                                              provider=provider)
            tool_calls = []
            if valid_names:
                tool_calls = parse_tool_calls(answer, valid_names)
                # 看着像要调工具却没解析出来 -> 只重试一次，避免延迟翻倍
                looks_json = ("calls" in answer) or ('"' in answer and "}" in answer)
                if not tool_calls and looks_json:
                    retry_parts = list(parts) + [{
                        "type": "text",
                        "text": "Your previous reply was not valid JSON. "
                                "Output ONLY one JSON line in the required format, with no explanation."}]
                    answer2, usage2 = self.sdk.complete(model_id, retry_parts,
                                                        system_text,
                                                        provider=provider)
                    calls2 = parse_tool_calls(answer2, valid_names)
                    if calls2:
                        answer, tool_calls = answer2, calls2
                        usage = {"prompt_tokens": usage["prompt_tokens"] + usage2["prompt_tokens"],
                                 "completion_tokens": usage["completion_tokens"] + usage2["completion_tokens"],
                                 "total_tokens": usage["total_tokens"] + usage2["total_tokens"]}
        except Exception as e:
            log("ERROR %s" % e)
            err = {"error": {"message": str(e), "type": "upstream_error"}}
            if stream:
                self._send(200, None, stream=True)
                self._sse(err)
                self.wfile.write(b"data: [DONE]\n\n")
            else:
                self._send(502, err)
            return

        log("%s  %.1fs  in=%s out=%s%s" % (
            model_id, time.time() - t0, usage["prompt_tokens"], usage["completion_tokens"],
            "  [tool_calls=%d]" % len(tool_calls) if tool_calls else ""))
        cid = "chatcmpl-" + uuid.uuid4().hex[:24]
        ts = int(time.time())

        if stream:
            self._send(200, None, stream=True)
            self._sse({"id": cid, "object": "chat.completion.chunk", "created": ts,
                       "model": model_id,
                       "choices": [{"index": 0, "delta": {"role": "assistant"}, "finish_reason": None}]})
            if tool_calls:
                for i, tc in enumerate(tool_calls):
                    tc = dict(tc, index=i)   # OpenAI 流式规范要求带 index，客户端靠它归并
                    self._sse({"id": cid, "object": "chat.completion.chunk", "created": ts,
                               "model": model_id,
                               "choices": [{"index": 0, "delta": {"tool_calls": [tc]},
                                            "finish_reason": None}]})
                self._sse({"id": cid, "object": "chat.completion.chunk", "created": ts,
                           "model": model_id,
                           "choices": [{"index": 0, "delta": {}, "finish_reason": "tool_calls"}],
                           "usage": usage})
            else:
                self._sse({"id": cid, "object": "chat.completion.chunk", "created": ts,
                           "model": model_id,
                           "choices": [{"index": 0, "delta": {"content": answer}, "finish_reason": None}]})
                self._sse({"id": cid, "object": "chat.completion.chunk", "created": ts,
                           "model": model_id,
                           "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}],
                           "usage": usage})
            self.wfile.write(b"data: [DONE]\n\n")
            self.wfile.flush()
        else:
            message = {"role": "assistant", "content": None if tool_calls else answer}
            if tool_calls:
                message["tool_calls"] = tool_calls
            self._send(200, {
                "id": cid, "object": "chat.completion", "created": ts, "model": model_id,
                "choices": [{"index": 0, "message": message,
                             "finish_reason": "tool_calls" if tool_calls else "stop"}],
                "usage": usage,
            })

    def _stream_error(self, msg):
        """流式响应头已发出时的错误通道：只能走 SSE error + [DONE]。"""
        try:
            self._sse({"error": {"message": msg, "type": "upstream_error"}})
            self.wfile.write(b"data: [DONE]\n\n")
            self.wfile.flush()
        except Exception:
            pass

    def _heartbeat(self):
        """SSE 注释行保活：ccproxy 会静默跳过它，但连接上有字节流动就不会被读超时。"""
        self.wfile.write(b": zen-bridge heartbeat\n\n")
        self.wfile.flush()

    def log_message(self, fmt, *args):
        pass  # 安静模式：不用默认访问日志刷屏


def _autopick_once(delay=25.0):
    """后台跑一次免费模型巡检（install_free_llms.py --auto）。

    为什么单开线程 + 延迟：桥接的首要任务是尽快能接请求，而巡检要 10 秒
    到 1 分半（真的有模型掉队时会触发全量重选）。挡在启动路径上会让
    「点一下模型」等很久。巡检本身也带冷却，不会每次启动都改配置。
    """
    time.sleep(max(0.0, delay))
    here = os.path.dirname(os.path.abspath(__file__))
    script = os.path.join(os.path.dirname(os.path.dirname(here)),
                          "free-llm-installer", "scripts",
                          "install_free_llms.py")
    if not os.path.exists(script):
        log("autopick: 找不到 %s，跳过" % script)
        return
    flags = 0x08000000 if os.name == "nt" else 0    # CREATE_NO_WINDOW
    try:
        log("autopick: 开始巡检免费模型（已在跑的请求不受影响）")
        r = subprocess.run([sys.executable, script, "--auto"],
                           capture_output=True, text=True, timeout=900,
                           creationflags=flags)
    except Exception as e:
        log("autopick 执行失败：%s" % e)
        return
    for line in (r.stdout or "").strip().splitlines()[-10:]:
        if line.strip():
            log("autopick| " + line)
    if r.returncode:
        err = (r.stderr or "").strip().splitlines()
        log("autopick| 退出码 %d%s" % (r.returncode,
                                      ("：" + err[-1][:180]) if err else ""))


def main():
    ap = argparse.ArgumentParser(description="OpenAI -> opencode SDK 桥接（零依赖单文件）")
    ap.add_argument("--port", type=int, default=8787, help="本桥接监听端口（默认 8787）")
    ap.add_argument("--sdk-port", type=int, default=41234, help="opencode serve 的端口（默认 41234）")
    ap.add_argument("--model", default=DEFAULT_MODEL, help="默认模型 ID")
    ap.add_argument("--provider", default=PROVIDER,
                    help="默认 provider（默认 %s）。opencode 下共 230 个 provider，"
                         "换这个值即可把桥接指向别的 provider；"
                         "也可在请求 model 字段里写 'provider/模型名' 单次覆盖" % PROVIDER)
    ap.add_argument("--agent", default="general",
                    help="opencode agent 名；general 实测最快（默认 general）"
                         "，可选 build/plan/explore/summary 等")
    ap.add_argument("--opencode-bin", default=None, help="opencode 可执行文件路径")
    ap.add_argument("--auto-start", action="store_true", help="SDK 未运行时自动拉起 opencode serve")
    ap.add_argument("--keep-session", action="store_true",
                    help="复用同一个 opencode session（更快，但上下文会累积）")
    ap.add_argument("--max-inflight", type=int, default=4,
                    help="同时向上游发起的请求上限（默认 4）。防止 opencode 挂起时线程堆积")
    ap.add_argument("--no-upstream-stream", action="store_true",
                    help="禁用真流式，全部走同步整段返回（排查流式问题用）")
    ap.add_argument("--timeout", type=int, default=600,
                    help="单次上游调用超时秒数（默认 600）。推理模型思考 75s+，别设太小")
    ap.add_argument("--autopick", action="store_true",
                    help="启动后后台巡检免费模型，掉队了才自动重选（不阻塞请求）")
    ap.add_argument("--autopick-delay", type=float, default=25.0,
                    help="--autopick 延迟多少秒开始（默认 25，先让桥接服务请求）")
    args = ap.parse_args()

    sdk = OpencodeSDK(args.sdk_port, args.auto_start, args.opencode_bin, args.agent,
                      args.keep_session, max_inflight=args.max_inflight,
                      stream_ok=not args.no_upstream_stream, timeout=args.timeout)
    Handler.sdk = sdk
    Handler.default_model = args.model
    Handler.default_provider = args.provider

    srv = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    log("zen_bridge 监听 http://127.0.0.1:%d/v1/chat/completions" % args.port)
    log("默认模型: %s (provider=%s) | Ctrl+C 退出" % (args.model, args.provider))

    # --auto-start 时先把 SDK 拉起来预热，否则第一个请求要额外等 20s 才有响应
    if args.auto_start:
        log("预热 opencode serve ...")
        sdk.ensure()
        log("上游 opencode SDK: http://127.0.0.1:%d  (%s)" % (
            args.sdk_port, "在线" if sdk.alive() else "未运行"))
    else:
        log("上游 opencode SDK: http://127.0.0.1:%d  (%s)" % (
            args.sdk_port, "在线" if sdk.alive() else "未运行"))
    try:
        if args.autopick:
            threading.Thread(target=_autopick_once,
                             args=(args.autopick_delay,), daemon=True).start()
            log("autopick: %ds 后巡检免费模型（后台线程，不阻塞请求）"
                % int(args.autopick_delay))
        srv.serve_forever()
    except KeyboardInterrupt:
        log("退出")
        srv.server_close()


if __name__ == "__main__":
    main()
