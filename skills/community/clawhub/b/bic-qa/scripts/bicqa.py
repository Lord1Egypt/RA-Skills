#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BIC-QA Open API 有状态问答客户端（仅标准库，零依赖）

子命令:
  ask      提问（自动复用或新建会话）
  new      只新建会话，不提问
  list     列出本地会话
  resume   切换当前会话（按 id 前缀匹配）
  check    自检凭证、状态目录与当前会话（--online 才会联网）
  selftest 离线自测，不发起任何网络请求

凭证（按优先级）:
  环境变量 BIC_API_KEY / BICQA_API_KEY / BIC_QA_API_KEY
  ~/.bic/config/api_key
  ~/.bic/openapi/api_key
  $BICQA_KEY_FILE

状态文件（按优先级）:
  $BICQA_STATE_FILE
  $BICQA_STATE_DIR/sessions.json
  ~/.bic/openapi/sessions.json

网络安全:
  默认只向 https://api.bic-qa.com 发送凭证。自定义 BICQA_BASE_URL 必须同时设置
  BICQA_ALLOW_CUSTOM_BASE_URL=1；远程自定义地址必须使用 HTTPS，且不跟随重定向。

调试参数（可用，但刻意不在 --help 中显示——技能场景下用不到）:
  -m/--model          指定上游模型，留空用默认
  -s/--stream         增量输出到 stderr
  --timeout N         单轮超时秒数，默认 600
  --debug             打印请求细节到 stderr（子命令前后均可）

  -s 的输出一律走 stderr，不会进 stdout，因此不会影响给模型的答案。
"""

import argparse
import http.client
import json
import os
import socket
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

OFFICIAL_BASE_URL = "https://api.bic-qa.com"
CREATE_PATH = "/open-api/v1/session/create"
CHAT_PATH = "/open-api/v1/chat"

KEY_ENVS = ("BIC_API_KEY", "BICQA_API_KEY", "BIC_QA_API_KEY")
KEY_FILES = (
    Path.home() / ".bic" / "config" / "api_key",
    Path.home() / ".bic" / "openapi" / "api_key",
)

TTL_ACTIVE = int(os.environ.get("BICQA_TTL_ACTIVE", str(2 * 3600)))
TTL_HARD = int(os.environ.get("BICQA_TTL_HARD", str(24 * 3600)))
MAX_TURNS = int(os.environ.get("BICQA_MAX_TURNS", "20"))

STATE_PATH = None  # 由 resolve_state_path() 惰性填充
DEBUG = False

# 出现这些错误码时，本地会话已不可用，需静默重建后重试一次
RECREATE_CODES = {"OPEN_API_SESSION_NOT_FOUND"}


class ApiError(Exception):
    def __init__(self, code, message, http_status=None, retry_after=None):
        super().__init__(message or code)
        self.code = code
        self.message = message or ""
        self.http_status = http_status
        self.retry_after = retry_after


class _NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ApiError("UNSAFE_REDIRECT", "拒绝携带 API Key 跟随 HTTP 重定向")


def resolve_base_url():
    """默认只向官方域名发送凭证；自定义地址必须显式启用。"""
    value = (os.environ.get("BICQA_BASE_URL") or OFFICIAL_BASE_URL).strip().rstrip("/")
    try:
        parsed = urllib.parse.urlsplit(value)
        port = parsed.port
    except ValueError:
        raise ApiError("INVALID_BASE_URL", "BICQA_BASE_URL 不是有效地址")
    official = urllib.parse.urlsplit(OFFICIAL_BASE_URL)
    is_official = (
        parsed.scheme == official.scheme
        and parsed.hostname == official.hostname
        and port in (None, 443)
        and not parsed.username
        and not parsed.password
        and not parsed.path.rstrip("/")
        and not parsed.query
        and not parsed.fragment
    )
    if is_official:
        return value

    if os.environ.get("BICQA_ALLOW_CUSTOM_BASE_URL") != "1":
        raise ApiError(
            "UNSAFE_BASE_URL",
            "拒绝向非官方地址发送 API Key。仅测试或受控代理场景可同时设置 "
            "BICQA_ALLOW_CUSTOM_BASE_URL=1。",
        )

    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        raise ApiError("INVALID_BASE_URL", "BICQA_BASE_URL 必须是有效的 HTTP(S) 地址")
    if parsed.scheme == "http" and parsed.hostname not in ("localhost", "127.0.0.1", "::1"):
        raise ApiError("UNSAFE_BASE_URL", "自定义 HTTP 地址仅允许 localhost；远程地址必须使用 HTTPS")
    if parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ApiError("INVALID_BASE_URL", "BICQA_BASE_URL 不得包含凭证、查询参数或 fragment")
    return value


# ---------------------------------------------------------------- 凭证与状态

def mask(s):
    s = str(s or "")
    if len(s) <= 8:
        return "*" * len(s)
    return s[:4] + "*" * (len(s) - 8) + s[-4:]


def resolve_key():
    for env in KEY_ENVS:
        v = (os.environ.get(env) or "").strip()
        if v:
            return v, "环境变量 %s" % env
    candidates = list(KEY_FILES)
    custom = os.environ.get("BICQA_KEY_FILE")
    if custom:
        candidates.insert(0, Path(custom).expanduser())
    for p in candidates:
        try:
            v = p.read_text(encoding="utf-8").strip()
        except OSError:
            continue
        if v:
            return v, "密钥文件 %s" % p
    raise ApiError(
        "NO_API_KEY",
        "未找到 BIC-QA API Key。请到 https://www.bic-qa.com 注册获取，然后二选一：\n"
        "  1) export BIC_API_KEY='<你的Key>'\n"
        "  2) printf '%s' '<你的Key>' > ~/.bic/config/api_key && chmod 600 ~/.bic/config/api_key",
    )


def resolve_state_path():
    global STATE_PATH
    if STATE_PATH is None:
        f = os.environ.get("BICQA_STATE_FILE")
        d = os.environ.get("BICQA_STATE_DIR")
        if f:
            STATE_PATH = Path(f).expanduser()
        elif d:
            STATE_PATH = Path(d).expanduser() / "sessions.json"
        else:
            STATE_PATH = Path.home() / ".bic" / "openapi" / "sessions.json"
    return STATE_PATH


def load_state():
    p = resolve_state_path()
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError
    except (OSError, ValueError):
        return {"version": 1, "active": None, "sessions": {}}, p
    data.setdefault("version", 1)
    data.setdefault("active", None)
    data.setdefault("sessions", {})
    return data, p


def save_state(state):
    p = resolve_state_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, p)
    try:
        os.chmod(p, 0o600)
    except OSError:
        pass


def is_fresh(m):
    age = time.time() - float(m.get("last_used") or 0)
    if age > TTL_HARD:
        return False, "超过硬过期时间 %.0fh" % (TTL_HARD / 3600.0)
    if age > TTL_ACTIVE:
        return False, "空闲超过 %.0f 分钟" % (TTL_ACTIVE / 60.0)
    if int(m.get("turns") or 0) >= MAX_TURNS:
        return False, "轮数达到上限 %d" % MAX_TURNS
    return True, ""


def guess_title(question):
    t = " ".join(str(question).split())
    return (t[:30] + "…") if len(t) > 31 else (t or "新会话")


def new_record(cid, title):
    return {
        "id": cid,
        "title": title,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "last_used": time.time(),
        "turns": 0,
        "last_question": "",
        "tokens": 0,
    }


def find_by_prefix(state, prefix):
    prefix = prefix.lower().lstrip("#")
    hits = [sid for sid in state["sessions"] if sid.lower().startswith(prefix)
            or sid.lower().endswith(prefix)]
    return hits


# ---------------------------------------------------------------- HTTP

def _request(path, payload, key, accept, timeout):
    if timeout <= 0:
        raise ApiError("INVALID_TIMEOUT", "timeout 必须大于 0 秒")
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    headers = {
        "Authorization": "Bearer " + key,
        "Content-Type": "application/json",
        "Accept": accept,
        "Accept-Language": "zh-CN",
        "Cache-Control": "no-cache",
        "User-Agent": "bic-qa-skill/2.0",
    }
    base_url = resolve_base_url()
    req = urllib.request.Request(base_url + path, data=body, headers=headers, method="POST")
    if DEBUG:
        safe_payload = dict(payload)
        for field in ("question", "title"):
            if isinstance(safe_payload.get(field), str):
                safe_payload[field] = "<redacted:%d chars>" % len(safe_payload[field])
        sys.stderr.write("[debug] POST %s%s body=%s\n" % (
            base_url, path, json.dumps(safe_payload, ensure_ascii=False)))
    try:
        return urllib.request.build_opener(_NoRedirectHandler()).open(req, timeout=timeout)
    except urllib.error.HTTPError as e:
        raw = ""
        try:
            raw = e.read().decode("utf-8", "replace")
        except Exception:
            pass
        code, msg, retry = "HTTP_%d" % e.code, raw[:400], None
        try:
            env = json.loads(raw)
            code = env.get("code") or code
            msg = env.get("message") or env.get("msg") or msg
        except ValueError:
            pass
        if e.code == 429:
            retry = e.headers.get("Retry-After")
        raise ApiError(code, msg, http_status=e.code, retry_after=retry)
    except (TimeoutError, socket.timeout):
        raise ApiError("OPEN_API_TIMEOUT", "连接或等待响应头超时（%s 秒）" % timeout)
    except urllib.error.URLError as e:
        if isinstance(e.reason, (TimeoutError, socket.timeout)):
            raise ApiError("OPEN_API_TIMEOUT", "连接或等待响应头超时（%s 秒）" % timeout)
        raise ApiError("NETWORK_ERROR", "网络不可达：%s" % e.reason)


def create_session(title, key, timeout=60):
    resp = _request(CREATE_PATH, {"title": title}, key, "application/json", timeout)
    try:
        env = json.loads(resp.read().decode("utf-8", "replace"))
    except (TimeoutError, socket.timeout):
        raise ApiError("OPEN_API_TIMEOUT", "创建会话时读取响应超时（%s 秒）" % timeout)
    except (OSError, http.client.HTTPException) as e:
        raise ApiError("OPEN_API_RESPONSE_INTERRUPTED", "创建会话响应中断：%s" % e)
    except ValueError:
        raise ApiError("OPEN_API_RESPONSE_INVALID", "创建会话返回了无效 JSON")
    finally:
        try:
            resp.close()
        except Exception:
            pass
    if env.get("status") not in (None, "success", "ok"):
        raise ApiError(env.get("code") or "CREATE_FAILED", env.get("message") or "创建会话失败",
                       http_status=resp.status)
    data = env.get("data") or {}
    cid = data.get("conversationId") or data.get("conversation_id")
    if not cid:
        raise ApiError("NO_CONVERSATION_ID", "响应中缺少 conversationId：%s" % json.dumps(env, ensure_ascii=False)[:300])
    return cid, data.get("chatTitle") or title


def _set_response_timeout(resp, timeout):
    """将剩余总时限同步到底层 socket；标准 urllib 响应均走此结构。"""
    fp = getattr(resp, "fp", None)
    raw = getattr(fp, "raw", None)
    sock = getattr(raw, "_sock", None)
    if sock is not None:
        sock.settimeout(max(0.001, timeout))


def iter_sse(resp, deadline=None):
    """解析 SSE 流，逐个产出 data: 行里的 JSON 对象。"""
    buf = b""
    read = getattr(resp, "read1", None) or (lambda n: resp.read(n))
    while True:
        if deadline is not None:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise ApiError("OPEN_API_STREAM_TIMEOUT", "流式回答超过总时限")
        try:
            if deadline is not None:
                _set_response_timeout(resp, remaining)
            chunk = read(65536)
        except (TimeoutError, socket.timeout):
            raise ApiError("OPEN_API_STREAM_TIMEOUT", "等待流式回答超时")
        except (OSError, http.client.HTTPException) as e:
            raise ApiError("OPEN_API_STREAM_INTERRUPTED", "流式回答传输中断：%s" % e)
        if not chunk:
            break
        buf += chunk
        while b"\n" in buf:
            line, buf = buf.split(b"\n", 1)
            line = line.rstrip(b"\r").decode("utf-8", "replace").strip()
            if not line or line.startswith(":"):
                continue
            if not line.startswith("data:"):
                continue
            payload = line[5:].strip()
            if not payload or payload == "[DONE]":
                continue
            try:
                yield json.loads(payload)
            except ValueError:
                if DEBUG:
                    sys.stderr.write("[debug] 忽略非 JSON 行: %s\n" % payload[:120])
                continue


def chat(question, cid, key, model=None, timeout=600, stream=False):
    started_at = time.monotonic()
    payload = {"question": question, "conversationId": cid}
    if model:
        payload["model"] = model
    resp = _request(CHAT_PATH, payload, key, "text/event-stream", timeout)

    parts, files = [], []
    error = None
    tokens = None
    session_id = None
    started = False
    last_kind = None
    done_received = False

    try:
        deadline = started_at + timeout
        for ev in iter_sse(resp, deadline=deadline):
            t = ev.get("type")
            if t == "delta" and error is None:
                d = ev.get("delta") or {}
                if isinstance(d.get("content"), str):
                    started = True
                    parts.append(d["content"])
                    if stream:
                        if last_kind != "answer":
                            sys.stderr.write("\n[answer]\n")
                            last_kind = "answer"
                        sys.stderr.write(d["content"])
                        sys.stderr.flush()
            elif t == "meta":
                session_id = ev.get("chatSessionId") or session_id
            elif t == "file":
                files.append(ev.get("filename") or ev.get("file") or "")
            elif t == "error":
                error = (ev.get("errorCode") or "SSE_ERROR", ev.get("content") or "流内错误")
            elif t == "done":
                done_received = True
                tokens = ev.get("totalTokens")
                if tokens is None:
                    tokens = (ev.get("summary") or {}).get("total_tokens")
                break
    except ApiError as e:
        error = (e.code, e.message)
    finally:
        try:
            resp.close()
        except Exception:
            pass

    if error is None and not done_received:
        error = ("OPEN_API_STREAM_INCOMPLETE", "流式回答在 done 事件前结束")

    if stream:
        sys.stderr.write("\n")
    return {
        "text": "".join(parts),
        "files": [f for f in files if f],
        "error": error,
        "tokens": tokens,
        "session_id": session_id,
        "empty": not started,
    }


# ---------------------------------------------------------------- 子命令

def cmd_ask(args):
    key, src = resolve_key()
    state, _ = load_state()
    sessions = state["sessions"]

    sid = state.get("active")
    reason = ""
    if args.new:
        sid, reason = None, "--new 指定"
    elif sid and sid in sessions:
        ok, why = is_fresh(sessions[sid])
        if not ok:
            sid, reason = None, why
    else:
        sid = None

    created = False
    if not sid:
        title = args.title or (guess_title(args.q) if not args.new else "新会话")
        sid, title = create_session(title, key)
        sessions[sid] = new_record(sid, title)
        state["active"] = sid
        created = True
        save_state(state)
        if reason:
            sys.stderr.write("[bic-qa] 新建会话（%s）\n" % reason)

    try:
        result = chat(args.q, sid, key, model=args.model, timeout=args.timeout,
                      stream=args.stream)
    except ApiError as e:
        if e.code not in RECREATE_CODES:
            raise
        result = {
            "text": "", "files": [],
            "error": (e.code, e.message), "tokens": None,
            "session_id": None, "empty": True,
        }

    if result["error"] and result["error"][0] in RECREATE_CODES:
        sys.stderr.write("[bic-qa] 服务端会话失效（%s），重建后重试一次\n" % result["error"][0])
        old = sid
        sid, title = create_session(sessions.get(old, {}).get("title") or "新会话", key)
        sessions[sid] = new_record(sid, title)
        state["active"] = sid
        created = True
        save_state(state)
        result = chat(args.q, sid, key, model=args.model, timeout=args.timeout,
                      stream=args.stream)

    rec = sessions.setdefault(sid, new_record(sid, args.title or "新会话"))
    rec["last_used"] = time.time()
    rec["turns"] = int(rec.get("turns") or 0) + 1
    rec["last_question"] = args.q[:200]
    if result["tokens"]:
        rec["tokens"] = int(rec.get("tokens") or 0) + int(result["tokens"])
    save_state(state)

    if result["error"]:
        code, msg = result["error"]
        sys.stderr.write("[bic-qa] 错误 %s: %s\n" % (code, msg))
        if result["text"]:
            sys.stderr.write("[bic-qa] 已丢弃不完整正文（%d 字符）\n" % len(result["text"]))
        sys.stderr.write("[bic-qa] 已保存会话 %s，可用 resume 继续\n" % sid[-8:])
        return 2

    if not result["text"].strip():
        sys.stderr.write("[bic-qa] 警告：本轮没有返回正文（可能被上游过滤）\n")

    print(result["text"])
    if result["files"]:
        print("\n生成文件: " + ", ".join(result["files"]))
    tail = "[session %s] turns=%d" % (sid[-8:], rec["turns"])
    if result["tokens"]:
        tail += " tokens=%d" % result["tokens"]
    if created:
        tail += " (新建)"
    print("\n" + tail)
    return 0


def cmd_new(args):
    key, _ = resolve_key()
    state, _ = load_state()
    cid, title = create_session(args.title, key)
    state["sessions"][cid] = new_record(cid, title)
    state["active"] = cid
    save_state(state)
    print("%s  %s  (已设为当前会话)" % (cid[-8:], title))
    return 0


def cmd_list(args):
    state, path = load_state()
    sessions = state["sessions"]
    if not sessions:
        print("暂无本地会话。状态文件：%s" % path)
        return 0
    print("状态文件：%s\n" % path)
    rows = sorted(sessions.values(), key=lambda m: m.get("last_used") or 0, reverse=True)
    for m in rows:
        flag = "*" if m["id"] == state.get("active") else " "
        age = time.time() - float(m.get("last_used") or 0)
        fresh = "可用" if is_fresh(m)[0] else ("空闲 %.0fh" % (age / 3600.0))
        print("%s %s  %s  turns=%-3d %-8s %s" % (
            flag, m["id"][-8:],
            time.strftime("%m-%d %H:%M", time.localtime(float(m.get("last_used") or 0))),
            int(m.get("turns") or 0), fresh, m.get("title") or ""))
    print("\n* = 当前会话")
    return 0


def cmd_resume(args):
    state, _ = load_state()
    hits = find_by_prefix(state, args.prefix)
    if not hits:
        print("未找到匹配 %r 的会话" % args.prefix)
        return 1
    if len(hits) > 1:
        print("匹配到多个会话，请给更长的前缀：")
        for h in hits:
            print("  " + h[-8:])
        return 1
    state["active"] = hits[0]
    save_state(state)
    print("已切换到会话 %s（%s）" % (hits[0][-8:], state["sessions"][hits[0]].get("title")))
    return 0


def cmd_check(args):
    """排障入口：只查本地环节，不消耗 token（除非加 --online）。"""
    print("BIC-QA 技能自检\n")
    ok = True

    try:
        key, src = resolve_key()
        print("  凭证      已配置  %s  来源：%s" % (mask(key), src))
    except ApiError as e:
        key = None
        ok = False
        print("  凭证      未配置")
        for line in e.message.splitlines():
            print("            " + line)

    p = resolve_state_path()
    try:
        p.parent.mkdir(parents=True, exist_ok=True)
        probe = p.parent / ".write-probe"
        probe.write_text("x", encoding="utf-8")
        probe.unlink()
        writable = "可写"
    except OSError:
        writable = "不可写"
        ok = False
    st, _ = load_state()
    cur = st.get("active")
    print("  状态文件  %s  %s" % (writable, p))
    print("  会话      共 %d 个%s" % (len(st["sessions"]),
                                  ("，当前 " + cur[-8:]) if cur else "，无当前会话"))

    if args.online:
        if not key:
            print("  连通性    跳过（无凭证）")
        else:
            try:
                cid, _t = create_session("连通性自检", key, timeout=30)
                print("  连通性    正常  已创建测试会话 %s（可在官网删除）" % cid[-8:])
            except ApiError as e:
                ok = False
                print("  连通性    失败  %s: %s" % (e.code, e.message))
    else:
        print("  连通性    未检查（加 --online 会创建一个测试会话验证 Key）")

    print("\n%s" % ("一切正常" if ok else "存在问题，按上面提示处理"))
    return 0 if ok else 1


# ---------------------------------------------------------------- 自测

class _FakeStream:
    def __init__(self, chunks):
        self.chunks = list(chunks)
        self.i = 0

    def read1(self, n):
        if self.i >= len(self.chunks):
            return b""
        c = self.chunks[self.i]
        self.i += 1
        return c


def cmd_selftest(args):
    ok = True

    def check(name, cond, extra=""):
        nonlocal ok
        print(("  PASS  " if cond else "  FAIL  ") + name + (("  -> " + str(extra)) if (extra and not cond) else ""))
        if not cond:
            ok = False

    print("1) SSE 解析")
    raw = (
        'data:{"type":"meta","chatSessionId":"abc-123","done":false}\n'
        "\n"
        ": keep-alive\n"
        'data:{"type":"delta","delta":{"role":"assistant"},"done":false}\n'
        "\n"
        'data:{"type":"delta","delta":{"content":"第一段"},"done":false}\n'
        "\n"
        'data:{"type":"delta","delta":{"content":"第二段"},"done":false}\n'
        "\n"
        'data:{"type":"file","filename":"report.md","file":"/x/report.md","done":false}\n'
        "\n"
        'data:{"type":"done","done":true,"totalTokens":123,"questionId":9}\n'
        "\n"
    ).encode("utf-8")
    # 故意从中间切分，验证跨 chunk 拼接
    mid = len(raw) // 2
    events = list(iter_sse(_FakeStream([raw[:mid], raw[mid:]])))
    check("事件数量=6", len(events) == 6, len(events))
    text = "".join(e.get("delta", {}).get("content", "")
                   for e in events if e.get("type") == "delta")
    check("正文拼接正确", text == "第一段第二段", repr(text))
    check("捕获 file 事件", any(e.get("type") == "file" and e.get("filename") == "report.md" for e in events))
    tokens = [e.get("totalTokens") for e in events if e.get("type") == "done"]
    check("捕获 done 的 totalTokens", tokens == [123], tokens)

    print("2) 错误流")
    err_raw = (
        'data:{"type":"delta","delta":{"content":"半句"},"done":false}\n'
        "\n"
        'data:{"type":"error","content":"上游服务暂时不可用","done":true,"errorCode":"OPEN_API_UPSTREAM_UNAVAILABLE"}\n'
        "\n"
    ).encode("utf-8")
    evs = list(iter_sse(_FakeStream([err_raw])))
    err = [(e.get("errorCode"), e.get("content")) for e in evs if e.get("type") == "error"]
    check("识别 error 事件", err and err[0][0] == "OPEN_API_UPSTREAM_UNAVAILABLE", err)

    print("3) 状态与过期判定")
    import tempfile
    tmp = Path(tempfile.mkdtemp(prefix="bicqa-st-"))
    global STATE_PATH
    saved = STATE_PATH
    STATE_PATH = tmp / "sessions.json"
    try:
        st, _ = load_state()
        check("空状态可加载", st["sessions"] == {} and st["active"] is None)
        rid = "eaf05aa6-bc61-4e18-baf7-df1839ef3928"
        st["sessions"][rid] = new_record(rid, "索引失效排查")
        st["active"] = rid
        save_state(st)
        check("落盘后可读回", json.loads(STATE_PATH.read_text(encoding="utf-8"))["sessions"][rid]["title"] == "索引失效排查")
        check("新建会话是新鲜的", is_fresh(st["sessions"][rid])[0])
        check("前缀匹配", find_by_prefix(st, "eaf05") == [rid])
        check("尾号匹配", find_by_prefix(st, "3928") == [rid])
        st["sessions"][rid]["last_used"] = time.time() - TTL_ACTIVE - 10
        f, why = is_fresh(st["sessions"][rid])
        check("空闲超时后判定失效", not f, why)
        st["sessions"][rid]["last_used"] = time.time()
        st["sessions"][rid]["turns"] = MAX_TURNS
        check("轮数超限后判定失效", not is_fresh(st["sessions"][rid])[0])
    finally:
        STATE_PATH = saved

    print("4) 凭证读取与脱敏")
    global KEY_FILES
    saved_key_files = KEY_FILES
    # 隔离真实环境：只看临时目录，避免本机已配置的 Key 影响断言
    KEY_FILES = (tmp / "no-such-dir" / "api_key",)
    try:
        check("短串全遮掩", mask("abc") == "***", mask("abc"))
        sample_key = "example-key-1234abcd"
        m = mask(sample_key)
        check("脱敏保持长度", len(m) == len(sample_key), m)
        check("脱敏保留首尾各 4 位", m.startswith("exam") and m.endswith("abcd"), m)
        check("脱敏中段全为 *", set(m[4:-4]) == {"*"}, m)
        for env in KEY_ENVS:
            os.environ.pop(env, None)
        os.environ.pop("BICQA_KEY_FILE", None)
        try:
            resolve_key()
            check("无凭证时抛错", False, "竟然拿到了 key")
        except ApiError as e:
            check("无凭证时抛错", e.code == "NO_API_KEY")
            check("报错信息不含测试密钥串", sample_key not in e.message, e.message)
        fake_key = "example-selftest-key-0123456789"
        kf = tmp / "api_key"
        kf.write_text(fake_key + "\n", encoding="utf-8")
        os.environ["BICQA_KEY_FILE"] = str(kf)
        try:
            got, _src = resolve_key()
            check("从密钥文件读取（自动去空白）", got == fake_key, got)
            os.environ["BIC_API_KEY"] = "example-env-key-9999"
            got2, _ = resolve_key()
            check("环境变量覆盖文件", got2 == "example-env-key-9999", got2)
        finally:
            os.environ.pop("BICQA_KEY_FILE", None)
            os.environ.pop("BIC_API_KEY", None)
    finally:
        KEY_FILES = saved_key_files

    print("\n%s" % ("自测全部通过" if ok else "自测存在失败项"))
    return 0 if ok else 1


# ---------------------------------------------------------------- CLI

def build_parser():
    p = argparse.ArgumentParser(prog="bicqa.py", description="BIC-QA Open API 有状态问答客户端")
    p.add_argument("--debug", action="store_true", help="打印请求细节到 stderr（子命令前后均可）")
    sub = p.add_subparsers(dest="cmd", required=True)

    # 子命令也接受 --debug；用 SUPPRESS 避免子解析器默认值覆盖父解析器已解析到的值
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--debug", action="store_true", default=argparse.SUPPRESS,
                        help=argparse.SUPPRESS)

    a = sub.add_parser("ask", parents=[common], help="提问（自动复用或新建会话）")
    a.add_argument("-q", "--q", "--question", dest="q", required=True, help="问题原文")
    a.add_argument("-n", "--new", action="store_true", help="强制新建会话")
    a.add_argument("-t", "--title", default=None, help="新建会话时的标题，默认取问题前 30 字")
    a.add_argument("-m", "--model", default=None, help=argparse.SUPPRESS)
    a.add_argument("--timeout", type=int, default=600, help=argparse.SUPPRESS)
    a.add_argument("-s", "--stream", action="store_true", help=argparse.SUPPRESS)
    a.set_defaults(func=cmd_ask)

    n = sub.add_parser("new", parents=[common], help="只新建会话")
    n.add_argument("-t", "--title", required=True, help="会话标题")
    n.set_defaults(func=cmd_new)

    l = sub.add_parser("list", parents=[common], help="列出本地会话")
    l.set_defaults(func=cmd_list)

    c = sub.add_parser("check", parents=[common], help="自检凭证与状态目录")
    c.add_argument("--online", action="store_true", help="额外创建一个测试会话验证 Key（会产生一个空会话）")
    c.set_defaults(func=cmd_check)

    r = sub.add_parser("resume", parents=[common], help="切换当前会话")
    r.add_argument("prefix", help="会话 id 前缀或尾号")
    r.set_defaults(func=cmd_resume)

    s = sub.add_parser("selftest", help="离线自测，不联网")
    s.set_defaults(func=cmd_selftest)
    return p


def main(argv=None):
    global DEBUG
    parser = build_parser()
    args = parser.parse_args(argv)
    DEBUG = args.debug
    try:
        return args.func(args)
    except ApiError as e:
        msg = "[bic-qa] %s: %s" % (e.code, e.message)
        if e.http_status:
            msg += " (HTTP %s)" % e.http_status
        if e.retry_after:
            msg += " 请在 %s 秒后重试" % e.retry_after
        sys.stderr.write(msg + "\n")
        return 3
    except KeyboardInterrupt:
        sys.stderr.write("\n[bic-qa] 已中断\n")
        return 130


if __name__ == "__main__":
    sys.exit(main())
