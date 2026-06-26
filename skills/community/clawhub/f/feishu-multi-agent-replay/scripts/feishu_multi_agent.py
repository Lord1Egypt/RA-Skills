#!/usr/bin/env python3
"""
feishu-multi-agent
飞书多机器人群内对话中继 (Multi-Agent Relay)

通过轮询飞书群消息历史，监听对方机器人的发言，
调用本机 OpenClaw brain 生成回复，并代表本机机器人发回飞书群聊。
支持话题锁定、开场角色、轮数控制、STOP/继续控制和空闲超时退出。
"""

import argparse
import json
import os
import re
import signal
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

FEISHU_TOKEN_URL = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
FEISHU_SEND_URL = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id"
FEISHU_HISTORY_URL = (
    "https://open.feishu.cn/open-apis/im/v1/messages"
    "?container_id_type=chat&container_id={chat_id}&page_size=50&start_time={start}"
)
DEFAULT_HTTP_TIMEOUT = 10

SKILL_DIR = Path(__file__).resolve().parent.parent
CACHE_DIR = Path.home() / ".openclaw" / "cache"
PID_FILE = CACHE_DIR / "feishu_multi_agent.pid"
STATE_FILE = CACHE_DIR / "feishu_multi_agent_state.json"
LOG_FILE = CACHE_DIR / "feishu_multi_agent.log"
RUNTIME_CONFIG_PATH = Path.home() / ".openclaw" / "config" / "feishu-multi-agent.json"
TEMPLATE_CONFIG_PATH = SKILL_DIR / "config" / "relay-config.json"


def load_config() -> dict:
    """Load runtime config. All user-facing settings live in one file."""
    for path in [RUNTIME_CONFIG_PATH, TEMPLATE_CONFIG_PATH]:
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                raw = json.load(f)
            return {k: v for k, v in raw.items() if not k.startswith("_")}
    raise FileNotFoundError(
        f"配置文件未找到。请将 {TEMPLATE_CONFIG_PATH} 复制到 {RUNTIME_CONFIG_PATH} 并填写配置。"
    )


def cfg(config: dict, key: str, default=None):
    return config.get(key, default)


def now_ts() -> int:
    return int(time.time())


def default_state(config: dict | None = None) -> dict:
    default_rounds = cfg(config or {}, "default_rounds", 50)
    return {
        "remaining_rounds": default_rounds,
        "total_rounds": default_rounds,
        "locked_topic": None,
        "conversation_history": [],
        "conversation_active": False,
        "last_topic_update_at": 0,
        "last_group_message_at": now_ts(),
        "last_starter_message_id": None,
        "last_starter_at": 0,
    }


def load_state(config: dict | None = None) -> dict:
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                state = json.load(f)
        except Exception:
            state = {}
    else:
        state = {}

    base = default_state(config)
    base.update(state)
    if not isinstance(base.get("conversation_history"), list):
        base["conversation_history"] = []
    return base


def save_state(state: dict):
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False)


def reset_rounds(state: dict, default_rounds: int):
    state["remaining_rounds"] = default_rounds
    state["total_rounds"] = default_rounds


def add_to_history(state: dict, role: str, content: str, max_history: int):
    state.setdefault("conversation_history", [])
    state["conversation_history"].append(
        {"role": role, "content": content, "timestamp": now_ts()}
    )
    if len(state["conversation_history"]) > max_history * 2:
        state["conversation_history"] = state["conversation_history"][-max_history * 2 :]


def cleanup_pid_file():
    PID_FILE.unlink(missing_ok=True)


def mark_group_activity(state: dict):
    state["last_group_message_at"] = now_ts()


def get_feishu_token(app_id: str, app_secret: str) -> str:
    data = json.dumps({"app_id": app_id, "app_secret": app_secret}).encode()
    req = urllib.request.Request(
        FEISHU_TOKEN_URL, data=data, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=DEFAULT_HTTP_TIMEOUT) as resp:
        res = json.loads(resp.read().decode())
        if res.get("code") == 0:
            return res["tenant_access_token"]
        raise RuntimeError(f"飞书 Token 获取失败: {res.get('msg')}")


def refresh_token_if_needed(config: dict, token_cache: dict) -> str:
    if time.time() - token_cache.get("ts", 0) > 5400:
        token_cache["token"] = get_feishu_token(
            cfg(config, "self_app_id"), cfg(config, "self_app_secret")
        )
        token_cache["ts"] = time.time()
    return token_cache["token"]


def fetch_recent_messages(token: str, chat_id: str, window_seconds: int) -> list:
    start = str(int(time.time()) - window_seconds)
    url = FEISHU_HISTORY_URL.format(chat_id=chat_id, start=start)
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(req, timeout=DEFAULT_HTTP_TIMEOUT) as resp:
            data = json.loads(resp.read().decode())
            return data.get("data", {}).get("items", [])
    except Exception as e:
        print(f"⚠️ [轮询失败] {e}", flush=True)
        return []


def send_group_message(token: str, chat_id: str, text: str) -> dict | None:
    payload = {
        "receive_id": chat_id,
        "msg_type": "text",
        "content": json.dumps({"text": text}, ensure_ascii=False),
    }
    req = urllib.request.Request(
        FEISHU_SEND_URL,
        data=json.dumps(payload).encode(),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=DEFAULT_HTTP_TIMEOUT) as resp:
            result = json.loads(resp.read().decode())
            if result.get("code") == 0:
                print("✅ [飞书] 消息发送成功", flush=True)
                return result.get("data") or {}
            print(f"❌ [飞书] 发送失败: {result.get('msg')}", flush=True)
    except urllib.error.HTTPError as e:
        print(f"❌ [飞书] HTTP {e.code}: {e.read().decode()}", flush=True)
    except Exception as e:
        print(f"❌ [飞书] 网络异常: {e}", flush=True)
    return None


def parse_keyword_topic(text: str, keywords: list[str]) -> str | None:
    stripped = text.strip()
    lowered = stripped.lower()
    for kw in keywords:
        kw_clean = kw.strip()
        if lowered.startswith(kw_clean.lower()):
            topic = stripped[len(kw_clean) :].strip(" ：:，,")
            if topic:
                return topic
    return None


def parse_round_count(text: str, patterns: list[str]) -> int | None:
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if not match:
            continue
        for group in match.groups():
            if group and str(group).isdigit():
                return int(group)
    return None


def contains_any(text: str, keywords: list[str]) -> bool:
    lowered = text.lower()
    return any(kw.lower() in lowered for kw in keywords)


def is_exact_stop(text: str, keywords: list[str]) -> bool:
    normalized = text.strip().lower()
    return any(normalized == kw.strip().lower() for kw in keywords)


def extract_text(msg: dict) -> str:
    content_str = msg.get("body", {}).get("content", "{}")
    try:
        content_dict = json.loads(content_str)
        return content_dict.get("text", str(content_dict)).strip()
    except Exception:
        return content_str.strip()


def is_mentioned(text: str, name: str) -> bool:
    return f"@{name}" in text or f"@ {name}" in text


def call_brain(
    prompt_text: str,
    config: dict,
    state: dict,
    prompt_template_key: str,
) -> str | None:
    api_url = cfg(config, "self_api_url", "http://127.0.0.1:18789")
    api_key = cfg(config, "self_token", "")
    model = cfg(config, "brain_model", "default")
    max_tok = cfg(config, "max_reply_tokens", 500)
    history_limit = cfg(config, "history_rounds", 5)

    sys_tmpl = cfg(
        config,
        prompt_template_key,
        "你是{self_name}，正在飞书群聊中与{peer_name}进行对话讨论。"
        "请根据当前消息给出自然、简短、有实质内容的回复（100字以内）。",
    )
    if isinstance(sys_tmpl, list):
        sys_tmpl = "\n".join(sys_tmpl)

    system_prompt = sys_tmpl.format(
        self_name=cfg(config, "self_name", "机器人A"),
        peer_name=cfg(config, "peer_name", "机器人B"),
        topic=state.get("locked_topic") or "未锁定",
    )

    if state.get("locked_topic"):
        system_prompt += (
            f"\n\n【重要约束】当前讨论话题已锁定为：{state['locked_topic']}。"
            "请围绕该话题展开；如果对方跑题，请礼貌拉回主题。"
        )

    messages = [{"role": "system", "content": system_prompt}]
    for msg in state.get("conversation_history", [])[-history_limit * 2 :]:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": prompt_text})

    payload = {"model": model, "max_tokens": max_tok, "messages": messages}
    req = urllib.request.Request(
        f"{api_url}/v1/chat/completions",
        data=json.dumps(payload).encode(),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode())
            reply = data["choices"][0]["message"]["content"].strip()
            add_to_history(state, "user", prompt_text, history_limit)
            add_to_history(state, "assistant", reply, history_limit)
            return reply
    except urllib.error.HTTPError as e:
        print(f"❌ [Brain] HTTP {e.code}: {e.read().decode('utf-8')}", flush=True)
    except Exception as e:
        print(f"❌ [Brain] 异常: {e}", flush=True)
    return None


def maybe_prefix_mention(text: str, target_name: str, require_mention: bool) -> str:
    if require_mention and not is_mentioned(text, target_name):
        return f"@{target_name} {text}"
    return text


def effective_starter_role(config: dict) -> str:
    role = str(cfg(config, "starter_role", "self")).lower()
    if role in {"self", "peer", "auto"}:
        return role
    return "self"


def should_self_start(config: dict) -> bool:
    role = effective_starter_role(config)
    return role in {"self", "auto"}


def send_opening_message(token: str, config: dict, state: dict) -> bool:
    if not state.get("conversation_active"):
        return False

    topic = state.get("locked_topic")
    if not topic:
        print("ℹ️ [开场跳过] 当前没有锁定话题", flush=True)
        return False

    prompt = (
        f"请以{cfg(config, 'self_name', '机器人A')}的身份，在群里主动发起关于“{topic}”的讨论。"
        f"用一句自然、直接、有观点的话开场，并鼓励{cfg(config, 'peer_name', '机器人B')}接话。"
    )
    reply = call_brain(prompt, config, state, "starter_prompt_template")
    if not reply:
        return False

    reply = maybe_prefix_mention(
        reply, cfg(config, "peer_name", "机器人B"), cfg(config, "require_mention", False)
    )
    result = send_group_message(token, cfg(config, "chat_id", ""), reply)
    if result is None:
        return False

    state["last_starter_message_id"] = result.get("message_id")
    state["last_starter_at"] = now_ts()
    print(f"🎬 [主动开场] {reply}", flush=True)
    return True


def pause_conversation(state: dict, config: dict):
    state["conversation_active"] = False
    if cfg(config, "preserve_topic_on_stop", True):
        pass
    else:
        state["locked_topic"] = None
    state["conversation_history"] = []


def finish_conversation(state: dict, config: dict):
    state["conversation_active"] = False
    state["conversation_history"] = []
    if cfg(config, "reset_rounds_after_finish", True):
        reset_rounds(state, cfg(config, "default_rounds", 50))


def run_daemon():
    print("🚀 [Relay Daemon] 启动中...", flush=True)
    config = load_config()
    state = load_state(config)

    self_name = cfg(config, "self_name", "机器人A")
    peer_name = cfg(config, "peer_name", "机器人B")
    peer_app_id = cfg(config, "peer_app_id", "")
    chat_id = cfg(config, "chat_id", "")
    require_mention = cfg(config, "require_mention", False)
    poll_interval = cfg(config, "poll_interval_seconds", 30)
    default_rounds = cfg(config, "default_rounds", 50)
    stop_keywords = cfg(config, "stop_exact_keywords", ["STOP"])
    continue_keywords = cfg(
        config, "continue_keywords", ["继续", "开始", "go on", "继续讨论", "继续聊"]
    )
    topic_keywords = cfg(
        config,
        "lock_topic_keywords",
        ["讨论", "话题锁定", "只聊", "锁定话题", "换个话题", "改聊"],
    )
    unlock_keywords = cfg(
        config, "unlock_topic_keywords", ["解锁话题", "随便聊", "话题放开", "解锁"]
    )
    round_patterns = cfg(
        config,
        "round_patterns",
        [
            r"再对话\s*(\d+)\s*(轮|次|回合)",
            r"继续对话\s*(\d+)\s*(轮|次|回合)",
            r"再聊\s*(\d+)\s*(轮|次|回合)",
            r"对话\s*(\d+)\s*(轮|次|回合)",
        ],
    )
    end_tmpl = cfg(
        config,
        "end_message_template",
        "本轮讨论结束（共 {rounds} 轮）。如需继续，请发送“继续”或“再对话N轮”。",
    )
    window_sec = cfg(config, "history_fetch_window_seconds", 60)
    idle_timeout_minutes = cfg(config, "idle_timeout_minutes", 30)
    starter_mode = str(cfg(config, "starter_mode", "on_topic_update")).lower()
    seen_ids: set[str] = set()
    daemon_start = now_ts()
    token_cache: dict = {}
    should_exit = False

    if state.get("remaining_rounds", 0) <= 0:
        reset_rounds(state, default_rounds)
    save_state(state)

    def handle_signal(signum, _frame):
        nonlocal should_exit
        print(f"🛑 [信号] 收到 {signum}，准备退出 daemon", flush=True)
        should_exit = True

    signal.signal(signal.SIGTERM, handle_signal)
    signal.signal(signal.SIGINT, handle_signal)

    try:
        token = refresh_token_if_needed(config, token_cache)
        print(f"✅ Token 已获取: {token[:20]}...", flush=True)
    except Exception as e:
        cleanup_pid_file()
        print(f"❌ Token 获取失败: {e}", flush=True)
        sys.exit(1)

    print(f"✅ [Relay Daemon] {self_name} 监听中 | 对方: {peer_name} ({peer_app_id})", flush=True)
    print(
        f"   require_mention={require_mention} | starter_role={effective_starter_role(config)}"
        f" | idle_timeout_minutes={idle_timeout_minutes}",
        flush=True,
    )

    try:
        while not should_exit:
            time.sleep(poll_interval)

            if idle_timeout_minutes > 0:
                idle_seconds = now_ts() - int(state.get("last_group_message_at", daemon_start))
                if idle_seconds >= idle_timeout_minutes * 60:
                    print(
                        f"⏰ [空闲退出] 群内 {idle_timeout_minutes} 分钟无新消息，daemon 自动退出",
                        flush=True,
                    )
                    break

            try:
                token = refresh_token_if_needed(config, token_cache)
            except Exception as e:
                print(f"❌ [Token] 刷新失败: {e}", flush=True)
                time.sleep(30)
                continue

            items = fetch_recent_messages(token, chat_id, window_sec)
            if not items:
                continue

            new_msgs = [m for m in items if m.get("message_id") not in seen_ids]
            if not new_msgs:
                continue
            new_msgs.sort(key=lambda x: int(x.get("create_time", 0)))

            for msg in new_msgs:
                message_id = msg.get("message_id")
                if not message_id:
                    continue
                seen_ids.add(message_id)

                msg_time = int(msg.get("create_time", 0)) // 1000
                sender_type = msg.get("sender", {}).get("sender_type", "")
                sender_id = msg.get("sender", {}).get("id", "")
                text = extract_text(msg)

                if msg_time < daemon_start:
                    continue

                mark_group_activity(state)
                save_state(state)

                if sender_type == "user":
                    if is_exact_stop(text, stop_keywords):
                        print(f"🛑 [停止指令] 收到精确 STOP: '{text}'", flush=True)
                        pause_conversation(state, config)
                        save_state(state)
                        continue

                    custom_rounds = parse_round_count(text, round_patterns)
                    if custom_rounds is not None:
                        state["remaining_rounds"] = custom_rounds
                        state["total_rounds"] = custom_rounds
                        state["conversation_active"] = True
                        save_state(state)
                        print(f"🔄 [轮数更新] 剩余轮数设为 {custom_rounds}", flush=True)
                        if should_self_start(config):
                            send_opening_message(token, config, state)
                            save_state(state)
                        continue

                    updated_topic = parse_keyword_topic(text, topic_keywords)
                    if updated_topic:
                        state["locked_topic"] = updated_topic
                        state["last_topic_update_at"] = now_ts()
                        state["conversation_active"] = True
                        state["conversation_history"] = []
                        reset_rounds(state, default_rounds)
                        save_state(state)
                        print(f"🔒 [话题更新] 已设置为: {updated_topic}", flush=True)
                        if should_self_start(config) and starter_mode in {"always", "on_topic_update", "on_start_only"}:
                            send_opening_message(token, config, state)
                            save_state(state)
                        continue

                    if contains_any(text, unlock_keywords):
                        state["locked_topic"] = None
                        state["conversation_history"] = []
                        save_state(state)
                        print("🔓 [话题解锁] 话题已放开", flush=True)
                        continue

                    if contains_any(text, continue_keywords):
                        state["conversation_active"] = True
                        if state.get("remaining_rounds", 0) <= 0:
                            reset_rounds(state, default_rounds)
                        save_state(state)
                        print(
                            f"▶️ [继续指令] 恢复对话 | 话题={state.get('locked_topic') or '未锁定'}",
                            flush=True,
                        )
                        if should_self_start(config):
                            send_opening_message(token, config, state)
                            save_state(state)
                        continue

                if sender_type == "app" and sender_id == peer_app_id:
                    if not state.get("conversation_active"):
                        print(f"⏸️ [暂停] 当前未激活，忽略 {peer_name} 的发言", flush=True)
                        continue

                    if state.get("remaining_rounds", 0) <= 0:
                        print(f"⏸️ [轮数耗尽] 忽略 {peer_name} 的发言", flush=True)
                        continue

                    if require_mention and not is_mentioned(text, self_name):
                        print(f"⏭️ [跳过] require_mention=true 但未被 @{self_name}", flush=True)
                        continue

                    prompt = f"{peer_name}说：{text}。请你作为{self_name}回应{peer_name}。"
                    reply = call_brain(prompt, config, state, "system_prompt_template")
                    if not reply:
                        print("⚠️ [Brain 无回复] 已跳过本轮", flush=True)
                        continue

                    reply = maybe_prefix_mention(reply, peer_name, require_mention)
                    print(f"💬 [{self_name}回复] {reply[:80]}", flush=True)
                    result = send_group_message(token, chat_id, reply)
                    if result is None:
                        continue

                    state["remaining_rounds"] = max(0, state["remaining_rounds"] - 1)
                    save_state(state)
                    print(
                        f"   剩余轮数: {state['remaining_rounds']}/{state['total_rounds']}",
                        flush=True,
                    )

                    if state["remaining_rounds"] <= 0:
                        send_group_message(
                            token, chat_id, end_tmpl.format(rounds=state["total_rounds"])
                        )
                        finish_conversation(state, config)
                        save_state(state)
                        print("✅ [结束] 对话轮数耗尽，已暂停并恢复默认轮数", flush=True)
    finally:
        cleanup_pid_file()
        print("👋 [Relay Daemon] 已退出", flush=True)


def cmd_start_sync():
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    if PID_FILE.exists():
        try:
            pid = int(PID_FILE.read_text().strip())
            os.kill(pid, 0)
            print(json.dumps({"ok": False, "message": f"Daemon 已在运行 (PID {pid})"}))
            return
        except (ProcessLookupError, ValueError):
            cleanup_pid_file()

    log_file = open(LOG_FILE, "a", buffering=1)
    proc = subprocess.Popen(
        [sys.executable, os.path.abspath(__file__), "daemon"],
        stdout=log_file,
        stderr=log_file,
        start_new_session=True,
    )
    PID_FILE.write_text(str(proc.pid))
    print(
        json.dumps(
            {"ok": True, "message": f"Relay daemon 已在后台启动 (PID {proc.pid})，日志: {LOG_FILE}"},
            ensure_ascii=False,
        )
    )


def cmd_stop_sync():
    if not PID_FILE.exists():
        print(json.dumps({"ok": False, "message": "未找到运行中的 daemon"}, ensure_ascii=False))
        return
    try:
        pid = int(PID_FILE.read_text().strip())
        os.kill(pid, signal.SIGTERM)
        cleanup_pid_file()
        print(json.dumps({"ok": True, "message": f"Relay daemon (PID {pid}) 已停止"}, ensure_ascii=False))
    except (ProcessLookupError, ValueError):
        cleanup_pid_file()
        print(json.dumps({"ok": True, "message": "Daemon 已不在运行，已清理 PID 文件"}, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"ok": False, "message": f"停止失败: {e}"}, ensure_ascii=False))


def cmd_status():
    running = False
    pid = None
    if PID_FILE.exists():
        try:
            pid = int(PID_FILE.read_text().strip())
            os.kill(pid, 0)
            running = True
        except (ProcessLookupError, ValueError):
            cleanup_pid_file()

    config = load_config()
    state = load_state(config)
    print(
        json.dumps(
            {
                "running": running,
                "pid": pid if running else None,
                "conversation_active": state.get("conversation_active", False),
                "remaining_rounds": state.get("remaining_rounds", 0),
                "total_rounds": state.get("total_rounds", 0),
                "locked_topic": state.get("locked_topic"),
                "starter_role": effective_starter_role(config),
                "idle_timeout_minutes": cfg(config, "idle_timeout_minutes", 30),
                "last_group_message_at": state.get("last_group_message_at", 0),
            },
            ensure_ascii=False,
        )
    )


def cmd_set_rounds(n: int):
    config = load_config()
    state = load_state(config)
    state["remaining_rounds"] = n
    state["total_rounds"] = n
    state["conversation_active"] = True
    save_state(state)
    print(json.dumps({"ok": True, "message": f"剩余轮数已设为 {n}"}, ensure_ascii=False))


def cmd_send(_to: str, msg: str):
    config = load_config()
    token_cache: dict = {}
    token = refresh_token_if_needed(config, token_cache)
    result = send_group_message(token, cfg(config, "chat_id", ""), msg)
    print(
        json.dumps(
            {"ok": result is not None, "message": "消息已发送" if result is not None else "消息发送失败"},
            ensure_ascii=False,
        )
    )


def main():
    parser = argparse.ArgumentParser(description="feishu-multi-agent - 飞书多端机器人群聊对话中继")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("start-sync", help="后台启动 daemon")
    sub.add_parser("stop-sync", help="停止 daemon")
    sub.add_parser("daemon", help="前台运行（调试）")
    sub.add_parser("status", help="查看运行状态")

    sr = sub.add_parser("set-rounds", help="手动设置剩余轮数")
    sr.add_argument("n", type=int, help="轮数")

    snd = sub.add_parser("send", help="发送单次消息到群聊")
    snd.add_argument("--to", default="peer", help="目标角色（仅用于兼容）")
    snd.add_argument("--msg", required=True, help="消息内容")

    args = parser.parse_args()

    if args.command == "start-sync":
        cmd_start_sync()
    elif args.command == "stop-sync":
        cmd_stop_sync()
    elif args.command == "status":
        cmd_status()
    elif args.command == "set-rounds":
        cmd_set_rounds(args.n)
    elif args.command == "send":
        cmd_send(args.to, args.msg)
    else:
        run_daemon()


if __name__ == "__main__":
    main()
