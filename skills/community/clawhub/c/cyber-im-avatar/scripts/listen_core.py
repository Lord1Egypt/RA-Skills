#!/usr/bin/env python3
"""listen_core.py — 单发唤醒式 IM 监听通用引擎（v2）。

设计要点
--------
1. **平台差异全部收敛在 ADAPTER**：命令模板 + 字段候选路径，引擎不含任何平台分支。
2. **命令链回退（cmd_*_chain）**：同一语义可给多条候选命令，引擎按序试到能解析出
   消息数组为止。CLI 大版本改名（如 `message list` → `message history`）不用改代码。
3. **全量 overrides**：~/.im-standin/env.json 的 `overrides.<platform>` 可覆盖/新增
   ADAPTER 任意键（命令或字段路径）。schema 漂移就地修配置，不动代码。
4. **失败可诊断**：字段路径全不命中时上抛 `SCHEMA_MISMATCH` + 原始输出，供 agent/人
   对照写出 override。
5. **55 分钟缓存续期**：模型上下文缓存通常 1 小时过期；到 55 分钟主动退出（退出码 3），
   agent 重挂时那次模型调用会命中并续上缓存，等待期仍然只有本地轮询。

退出码: 0=命中(stdout 单行 JSON) · 3=超时未命中/缓存续期 · 2=参数/环境错误
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timedelta

from data_guard import atomic_write_json, ensure_private_dir, redact_sensitive, schema_outline

ENV_DIR = os.environ.get("IM_STANDIN_DIR") or os.path.expanduser("~/.im-standin")
ENV_PATH = os.path.join(ENV_DIR, "env.json")
STATE_DIR = os.path.join(ENV_DIR, "states")
DEFAULT_CACHE_REFRESH_MIN = 55.0


def dig(obj, paths):
    """按候选路径列表取值，返回第一个命中的；paths 为空/非法返回 None。"""
    if not paths:
        return None
    if isinstance(paths, (str, int)):
        paths = [paths]
    for p in paths:
        cur, ok = obj, True
        for k in (p if isinstance(p, (list, tuple)) else [p]):
            if isinstance(cur, dict) and k in cur:
                cur = cur[k]
            elif isinstance(cur, list) and isinstance(k, int) and -len(cur) <= k < len(cur):
                cur = cur[k]
            else:
                ok = False
                break
        if ok:
            return cur
    return None


def load_env():
    try:
        with open(ENV_PATH) as f:
            return json.load(f)
    except Exception:
        return {}


class Listener:
    def __init__(self, platform, adapter):
        self.platform = platform
        self.base = dict(adapter)
        env = load_env()
        # 全量合并：既能覆盖已有键，也能新增键（如给老版本 CLI 补 cmd_list_chain）
        ov = env.get("overrides", {}).get(platform) or \
            env.get("field_overrides", {}).get(platform) or {}
        self.ad = dict(self.base)
        self.ad.update(ov)
        self.env = env
        self._good = {}  # 命令链里已验证可用的模板缓存，避免每轮重试失败命令
        self.window = {}  # 每轮刷新的时间窗（供 {begin_time}/{end_time} 占位）

    # ---- CLI 调用 -------------------------------------------------------
    def run_cli(self, args, timeout=30):
        try:
            p = subprocess.run([self.ad["cli"]] + list(args),
                               capture_output=True, text=True, timeout=timeout)
        except FileNotFoundError:
            return 127, None, f"CLI not found: {self.ad['cli']}（未安装或不在 PATH）"
        except subprocess.TimeoutExpired:
            return 124, None, "cli timeout"
        raw = (p.stdout or "").strip()
        # 有的 CLI 会连续输出多个 JSON 文档（结果 + 错误块），只取第一个
        try:
            obj, _end = json.JSONDecoder().raw_decode(raw.lstrip())
            return p.returncode, obj, raw
        except Exception:
            return p.returncode, None, raw + (("\n" + p.stderr) if p.stderr else "")

    def _argv(self, tmpl, **kw):
        """模板展开；模板里未出现的占位键不影响。"""
        out = []
        for a in tmpl:
            try:
                out.append(a.format(**kw))
            except (KeyError, IndexError):
                out.append(a)
        return out

    def get_self_id(self):
        cached = (self.env.get("platforms", {}).get(self.platform, {}) or {}).get("self_id")
        if cached:
            return cached
        rc, j, raw = self.run_cli(self.ad["cmd_whoami"])
        if rc == 0 and j is not None:
            v = dig(j, self.ad.get("f_self_id"))
            if v:
                return v
        # 有的 CLI whoami 只返回人类可读文本（如 `wecom-cli auth show`），用正则兜底
        import re
        pat = self.ad.get("self_id_regex")
        if pat and raw:
            m = re.search(pat, raw)
            if m:
                return m.group(1)
        return None

    # ---- 取消息 ---------------------------------------------------------
    def _candidate_commands(self, by_user):
        """返回候选命令模板列表：优先链，其次单条。"""
        if by_user and self.ad.get("cmd_list_user"):
            chain = self.ad.get("cmd_list_user_chain")
            return chain or [self.ad["cmd_list_user"]]
        chain = self.ad.get("cmd_list_chain")
        return chain or [self.ad["cmd_list"]]

    def _msg_id(self, it):
        """消息唯一键：优先原生 ID；无 ID 的 CLI（如企微）用复合指纹。"""
        native = dig(it, self.ad.get("f_msg_id"))
        if native:
            return native
        comp = self.ad.get("f_msg_id_compose")
        if comp:
            parts = []
            for p in comp:
                v = dig(it, [p])
                parts.append("" if v is None else str(v))
            return "fp_" + hashlib.md5("|".join(parts).encode()).hexdigest()[:16]
        return None

    def fetch_messages(self, target, by_user=False):
        """返回 (ok, msgs | error_raw)。msgs 统一为「最新在前」。"""
        last_err = None
        cands = self._candidate_commands(by_user)
        key = "user" if by_user else "chat"
        cached = self._good.get(key)
        if cached in cands:  # 已验证过的命令排最前
            cands = [cached] + [c for c in cands if c != cached]
        for tmpl in cands:
            kw = {"chat_id": target, "user_id": target, "target": target, "id": target}
            kw.update(self.window)
            rc, j, raw = self.run_cli(self._argv(tmpl, **kw))
            if rc != 0 or j is None:
                last_err = redact_sensitive(raw)[:3000]
                continue
            items = dig(j, self.ad["f_items"])
            if items is None:
                # 区分「空结果」与「字段不对」：空结果时服务端只回计数/翻页字段
                cnt = dig(j, self.ad.get("f_count"))
                if cnt == 0 or dig(j, self.ad.get("f_has_more")) is False:
                    items = []
                else:
                    outline = json.dumps(schema_outline(j), ensure_ascii=False)
                    last_err = "SCHEMA_MISMATCH keys: " + outline[:3000]
                    continue
            self._good[key] = tmpl
            return True, self._normalize(items)
        return False, last_err or "no candidate command produced messages"

    def _normalize(self, items):
        msgs, need_fill = [], []
        for it in items:
            mid = self._msg_id(it)
            content = dig(it, self.ad.get("f_content_list")) or ""
            msgs.append({
                "id": mid,
                "sender": dig(it, self.ad["f_sender"]),
                "content": content,
                "ts": dig(it, self.ad["f_create_time"]) or "",
            })
            if not content and mid and self.ad.get("cmd_mget"):
                need_fill.append(mid)
        if need_fill:
            rc2, j2, _ = self.run_cli(
                [a.format(ids=",".join(need_fill)) for a in self.ad["cmd_mget"]])
            if rc2 == 0 and j2 is not None:
                filled = {}
                arr = dig(j2, self.ad["f_items"]) or (j2 if isinstance(j2, list) else [])
                for it in arr:
                    mid = dig(it, self.ad["f_msg_id"])
                    c = dig(it, self.ad.get("f_content_mget"))
                    if mid and c:
                        filled[mid] = c
                for m in msgs:
                    if not m["content"] and m["id"] in filled:
                        m["content"] = filled[m["id"]]
        if (self.ad.get("order") or "desc").lower() == "asc":
            msgs.reverse()  # 统一成最新在前，主循环按此推水位
        return msgs


def load_watermark(state_file):
    try:
        with open(state_file) as f:
            return json.load(f).get("last_id")
    except Exception:
        return None


def save_watermark(state_file, last_id):
    atomic_write_json(state_file, {"last_id": last_id, "ts": time.time()})


def time_window(lookback_min):
    """轮询用的时间窗占位：{begin_time}/{end_time}（本地时间串）与 {now_ts}。"""
    end = datetime.now()
    begin = end - timedelta(minutes=max(1, lookback_min))
    fmt = "%Y-%m-%d %H:%M:%S"
    return {
        "begin_time": begin.strftime(fmt),
        "end_time": end.strftime(fmt),
        "now": end.strftime(fmt),
        "begin_ts": int(begin.timestamp()),
        "end_ts": int(end.timestamp()),
        "now_ts": int(end.timestamp()),
    }


def resolve_deadline(until="", timeout=0):
    if until and timeout > 0:
        raise ValueError("--until 与 --timeout 不能同时使用")
    if not until:
        return time.time() + timeout if timeout > 0 else None
    try:
        return float(until)
    except ValueError:
        try:
            return datetime.fromisoformat(until.replace("Z", "+00:00")).timestamp()
        except ValueError as e:
            raise ValueError("--until 必须是 Unix 时间戳或 ISO 8601 时间") from e


def sleep_capped(seconds, deadline=None):
    """睡 seconds，但不超过 deadline，避免大 interval 拖过缓存续期点。"""
    if deadline is not None:
        seconds = min(seconds, max(0.0, deadline - time.time()))
    if seconds > 0:
        time.sleep(seconds)


def main(platform, adapter):
    ap = argparse.ArgumentParser(description=f"单发唤醒式 {platform} 消息监听")
    ap.add_argument("--chat-id", default="", help="目标会话 ID（与 --user-id 二选一）")
    ap.add_argument("--user-id", default="",
                    help="目标用户 ID（私聊免查 chat_id；平台支持时生效）")
    ap.add_argument("--sender", default="", help="只盯该发送者；空=除自己外所有人")
    ap.add_argument("--keyword", default="", help="命中关键词（子串匹配）")
    ap.add_argument("--interval", type=int, default=60, help="轮询间隔秒（最小 2）")
    ap.add_argument("--lookback-min", type=int, default=60,
                    help="每轮拉取的回看窗口（分钟），仅需时间窗参数的平台用")
    ap.add_argument("--init", choices=["latest", "zero"], default="latest",
                    help="latest=只盯今后新消息；zero=立刻对存量最新一条判定")
    ap.add_argument("--state", default="", help="水位文件路径")
    ap.add_argument("--timeout", type=int, default=0,
                    help="相对超时秒，0=不设额外上限（仍受缓存续期约束）；到点退出码 3")
    ap.add_argument("--until", default="",
                    help="绝对截止时间（Unix 时间戳/ISO 8601）；重挂沿用，不能和 --timeout 同用")
    ap.add_argument("--cache-refresh-min", type=float, default=DEFAULT_CACHE_REFRESH_MIN,
                    help="到点主动退出以续模型上下文缓存（分钟，0=关闭）")
    args = ap.parse_args()

    try:
        user_deadline = resolve_deadline(args.until, args.timeout)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(2)
    cache_min = max(0.0, args.cache_refresh_min)
    cache_deadline = time.time() + cache_min * 60 if cache_min > 0 else None
    deadline = min([d for d in (user_deadline, cache_deadline) if d is not None], default=None)
    cache_cap = (cache_deadline is not None and
                 (user_deadline is None or cache_deadline <= user_deadline))

    def timeout_exit():
        if cache_cap and cache_deadline is not None and time.time() >= cache_deadline:
            print(f"[cache-refresh] {cache_min:g} 分钟到点退出，重挂即可续上下文缓存",
                  file=sys.stderr)
        sys.exit(3)

    if deadline and time.time() >= deadline:
        timeout_exit()
    if not args.chat_id and not args.user_id:
        print("ERROR: 必须给 --chat-id 或 --user-id", file=sys.stderr)
        sys.exit(2)
    if args.chat_id and args.user_id:
        print("ERROR: --chat-id 与 --user-id 只能选一个", file=sys.stderr)
        sys.exit(2)
    by_user = bool(args.user_id)
    target = args.user_id if by_user else args.chat_id

    if args.interval < 2:
        args.interval = 2
    ensure_private_dir(ENV_DIR)
    ensure_private_dir(STATE_DIR)
    safe_target = target.replace("/", "_")
    state_file = args.state or os.path.join(STATE_DIR, f"{platform}_{safe_target}.pos")
    ln = Listener(platform, adapter)

    self_id = ln.get_self_id()
    if not self_id:
        print(f"ERROR: 无法获取本人 ID（未登录？先运行 bootstrap.py 或 {adapter['cli']} 登录）",
              file=sys.stderr)
        sys.exit(2)

    wm = load_watermark(state_file)
    if wm is None and args.init == "latest":
        ln.window = time_window(args.lookback_min)
        ok, res = ln.fetch_messages(target, by_user)
        if not ok:
            print(f"ERROR: 初始化水位失败: {res}", file=sys.stderr)
            sys.exit(2)
        wm = res[0]["id"] if res else ""
        save_watermark(state_file, wm)

    fail_streak = 0

    while True:
        if deadline and time.time() > deadline:
            timeout_exit()
        ln.window = time_window(args.lookback_min)
        ok, res = ln.fetch_messages(target, by_user)
        if not ok:
            fail_streak += 1
            if fail_streak >= 5:
                print(f"ERROR: 连续 5 轮拉取失败（登录态/权限/schema 漂移）: {res}",
                      file=sys.stderr)
                sys.exit(2)
            sleep_capped(args.interval, deadline)
            continue
        fail_streak = 0

        new_msgs = []
        for m in res:  # 已统一为最新在前
            if m["id"] == wm:
                break
            new_msgs.append(m)

        # 一轮里有多条新消息时只唤醒一次，报最新那条（agent 会自己拉上下文看全）；
        # 水位直接推到最新，避免同一批消息把 agent 连续唤醒多次。
        newest = res[0]["id"] if res and res[0]["id"] else wm
        hit = None
        for m in new_msgs:
            if self_id and m["sender"] == self_id:
                continue  # 防回环
            if args.sender and m["sender"] != args.sender:
                continue
            if args.keyword and args.keyword not in (m["content"] or ""):
                continue
            hit = m
            break

        if hit:
            save_watermark(state_file, newest)  # 命中即推水位，防重复唤醒
            print(json.dumps({
                "hit": True, "platform": platform,
                "chat_id": args.chat_id or "",
                "user_id": args.user_id or "",
                "message_id": hit["id"], "sender": hit["sender"],
                "content": hit["content"], "create_time": hit["ts"],
                "pending_in_burst": max(0, len(new_msgs) - 1),
            }, ensure_ascii=False))
            sys.exit(0)

        if newest and newest != wm:
            wm = newest
            save_watermark(state_file, wm)

        sleep_capped(args.interval, deadline)
