#!/usr/bin/env python3
"""
Ecovacs 毛团控制 — 通过开放平台 AK 与网关控机（不使用账号密码登录）。

前置：用户在 Ecovacs 开放平台「服务概览」获取 AK（中国大陆 https://open.ecovacs.cn/ ，非中国区 https://open.ecovacs.com/ ）。

控机请求发往网关 **`POST /robot/skill/pet/cmd`**（`cmd` + `data`）。

Usage:
  python3 ecovacs.py set-ak <ak>
  python3 ecovacs.py devices
  python3 ecovacs.py cmd <nickName> <cmdName> [json_body]
  python3 ecovacs.py display <nickName> action <type> [json_data] [msg_id]
  python3 ecovacs.py display <nickName> actions <json_actions_array> [json_variables] [json_conditions] [msg_id]
  python3 ecovacs.py display <nickName> sleep [msg_id]
  python3 ecovacs.py display <nickName> clear-scheduled [msg_id]
  python3 ecovacs.py display <nickName> reset [msg_id]
  python3 ecovacs.py display <nickName> dance [style] [length] [msg_id]
  python3 ecovacs.py display <nickName> sequence <json_sequence> [msg_id]

单动作 → references/phoenix-single-action.md（play_action）。
编排/序列 → references/phoenix-action-control.md（action_sequence；勿用单动作 ×100 字段）。

环境变量：
  ECOVACS_AK          开放平台 AK（与 set-ak 二选一）
  ECOVACS_PORTAL_URL  网关根地址（可选；未设置时默认 https://open.ecovacs.cn，非中国区常用 https://open.ecovacs.com）
  ECOVACS_SKIP_WAKE_CHECK  设为 1/true/on 时，display 动作下发前不自动检查/唤醒
  ECOVACS_SKIP_TIMING_LIMIT  设为 1/true/on 时，跳过单动作/编排默认用时校验（调试）
  ECOVACS_WAKE_POLL_ATTEMPTS  自动唤醒后的轮询次数（默认 5）
  ECOVACS_WAKE_POLL_INTERVAL  自动唤醒后的轮询间隔秒数（默认 1）

编排默认用时：单步 delay+duration ≤10s；整段编排 ≤20s。用户显式指定时在 JSON 加 "user_timing": true
（或 conditions.scheduled / repeat 定时任务）。

AK 保存在 ~/.ecovacs_session.json（仅 {"ak": "..."}，不含密码）。
"""
import json
import os
import sys
import time
from urllib import parse as urlparse
from urllib import request as urlreq

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)

from dance_choreography import (  # noqa: E402
    DEFAULT_DANCE_ROUTINE,
    get_dance_routine_meta,
    list_dance_routine_ids,
    normalize_dance_routine,
)

SESSION_FILE = os.path.expanduser("~/.ecovacs_session.json")


def portal_base():
    return os.environ.get("ECOVACS_PORTAL_URL", "https://open.ecovacs.cn").rstrip("/")


def load_ak():
    ak = os.environ.get("ECOVACS_AK", "").strip()
    if ak:
        return ak
    if os.path.exists(SESSION_FILE):
        try:
            session = json.load(open(SESSION_FILE, encoding="utf-8"))
            ak = (session.get("ak") or "").strip()
            if ak:
                return ak
        except Exception:
            pass
    raise SystemExit(
        "未配置 AK。请设置环境变量 ECOVACS_AK，或执行：python3 ecovacs.py set-ak <ak>\n"
        "AK 须在开放平台获取（中国大陆 https://open.ecovacs.cn/ ，非中国区 https://open.ecovacs.com/ ）"
    )


def save_ak(ak):
    path = SESSION_FILE
    data = {"ak": ak.strip()}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✅ 已保存 AK 到 {path}")


def http_get_json(url):
    req = urlreq.Request(url, headers={"Accept": "application/json"})
    with urlreq.urlopen(req, timeout=45) as resp:
        return json.loads(resp.read().decode("utf-8"))


def http_post_json(url, body):
    data = json.dumps(body).encode("utf-8")
    req = urlreq.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
    )
    with urlreq.urlopen(req, timeout=45) as resp:
        return json.loads(resp.read().decode("utf-8"))


def skill_device_list(ak):
    q = urlparse.quote(ak, safe="")
    url = f"{portal_base()}/robot/skill/deviceList?ak={q}"
    return http_get_json(url)


def skill_pet_cmd(ak, nick_name, cmd, body_data=None):
    """宠物控机请求。"""
    url = f"{portal_base()}/robot/skill/pet/cmd"
    body = {"ak": ak, "nickName": nick_name, "cmd": cmd}
    if body_data is not None:
        body["data"] = body_data
    return http_post_json(url, body)


def nested_get(obj, path, default=None):
    cur = obj
    for key in path:
        if not isinstance(cur, dict) or key not in cur:
            return default
        cur = cur[key]
    return cur


def ensure_ok(resp, what="请求"):
    if resp.get("code") != 0:
        msg = resp.get("msg", "unknown")
        raise SystemExit(f"{what}失败: {msg} | {json.dumps(resp, ensure_ascii=False)}")


def ensure_inner_ok(resp, what="请求"):
    """Validate the cloud/business envelope when present."""
    body_code = nested_get(resp, ["data", "resp", "body", "code"])
    if body_code is not None and int(body_code) != 0:
        body_msg = nested_get(resp, ["data", "resp", "body", "msg"], "unknown")
        raise SystemExit(f"{what}业务失败: {body_msg} | {json.dumps(resp, ensure_ascii=False)}")


def truthy_env(name):
    return os.environ.get(name, "").strip().lower() in ("1", "true", "yes", "on")


def camera_enable_from_response(resp):
    return nested_get(resp, ["data", "resp", "body", "data", "enable"])


def is_enable_on(value):
    try:
        return int(value) == 1
    except (TypeError, ValueError):
        return False


def display_requires_wake(body_data):
    """Return true when a raw display payload may trigger visible/motion behavior."""
    if not isinstance(body_data, dict):
        return False
    action_cmd = str(body_data.get("cmd") or "").strip()
    if action_cmd == "play_action":
        t = str((body_data.get("data") or {}).get("type") or "")
        if t in PHOENIX_MINIMAL_TYPES or t == "play_sound":
            return False
        return True
    if action_cmd != "action_sequence":
        return False
    seq_data = body_data.get("data")
    if not isinstance(seq_data, dict):
        return False
    actions = seq_data.get("actions")
    if not isinstance(actions, list):
        return False
    # Pure sound can run while asleep; any other action needs the pet awake.
    return any(isinstance(a, dict) and a.get("type") != "play_sound" for a in actions)


def ensure_pet_awake(ak, nick):
    """Before motion/display actions, make sure the pet is awake.

    getCamera.enable=0 corresponds to the closed-eye / cameraUnable state where
    display actions may return OK but physical motion is silently ignored.
    Wake is performed through the same pet skill gateway via setCamera enable=1.
    """
    if truthy_env("ECOVACS_SKIP_WAKE_CHECK"):
        return

    cam = send_cmd_gateway(ak, nick, "getCamera", {})
    ensure_ok(cam, "唤醒前检查(getCamera)")
    ensure_inner_ok(cam, "唤醒前检查(getCamera)")

    enable = camera_enable_from_response(cam)
    if is_enable_on(enable):
        print("[wake] device is already awake (getCamera.enable=1)", file=sys.stderr)
        ensure_standard_work_mode(ak, nick)
        return

    print("[wake] device appears asleep/eyes closed; sending setCamera enable=1", file=sys.stderr)
    wake = send_cmd_gateway(ak, nick, "setCamera", {"enable": 1})
    ensure_ok(wake, "自动唤醒(setCamera)")
    ensure_inner_ok(wake, "自动唤醒(setCamera)")

    attempts = int(os.environ.get("ECOVACS_WAKE_POLL_ATTEMPTS", "5"))
    interval = float(os.environ.get("ECOVACS_WAKE_POLL_INTERVAL", "1"))
    for _ in range(max(1, attempts)):
        time.sleep(max(0, interval))
        cam = send_cmd_gateway(ak, nick, "getCamera", {})
        ensure_ok(cam, "唤醒后检查(getCamera)")
        ensure_inner_ok(cam, "唤醒后检查(getCamera)")
        if is_enable_on(camera_enable_from_response(cam)):
            print("[wake] device is awake (getCamera.enable=1)", file=sys.stderr)
            ensure_standard_work_mode(ak, nick)
            return

    raise SystemExit(
        "自动唤醒失败：setCamera 已下发，但 getCamera.enable 仍不是 1。"
        "请确认设备在线、未在充电/保护态，或手动唤醒后重试。"
    )


def ensure_standard_work_mode(ak, nick):
    """Best-effort switch out of cameraUnable/block mode before physical display actions."""
    resp = send_cmd_gateway(ak, nick, "setWorkMode", {"mode": "standard"})
    if resp.get("code") != 0:
        print(
            "[wake] WARN: setWorkMode standard failed; physical actions may still be ignored: "
            + json.dumps(resp, ensure_ascii=False),
            file=sys.stderr,
        )
        return
    try:
        ensure_inner_ok(resp, "切换标准工作模式(setWorkMode)")
        print("[wake] work mode set to standard", file=sys.stderr)
    except SystemExit as e:
        print(f"[wake] WARN: {e}", file=sys.stderr)


def print_devices(resp):
    ensure_ok(resp, "设备列表")
    rows = resp.get("data")
    if not isinstance(rows, list):
        print(json.dumps(resp, indent=2, ensure_ascii=False))
        return
    print(f"{'#':<4} {'Name':<28} {'Nick':<22} {'Status':<8}")
    print("-" * 90)
    for i, d in enumerate(rows):
        if not isinstance(d, dict):
            continue
        name = str(d.get("deviceName", "") or "")[:28]
        nick = str(d.get("nick", "") or "")[:22]
        st = d.get("status")
        st_s = "online" if st == 1 else ("offline" if st == 0 else str(st))
        print(f"{i:<4} {name:<28} {nick:<22} {st_s:<8}")


def parse_json_arg(raw, default=None):
    if raw is None:
        return {} if default is None else default
    try:
        return json.loads(raw)
    except Exception as e:
        raise SystemExit(f"Invalid JSON: {raw} | err={e}")


PHOENIX_DEFAULT_MOVE = "-1"
PHOENIX_HEAD_TYPES = frozenset({"nod_head", "shake_head", "cock_head"})
PHOENIX_EMOTION_TYPES = frozenset({"calm", "happy", "attached", "curious", "angry", "sad", "scared"})
PHOENIX_MINIMAL_TYPES = frozenset({"sleep", "clear_scheduled"})
PHOENIX_ZERO_FIELD_TYPES = frozenset({"reset"})


def conditions_empty(conditions):
    if not isinstance(conditions, dict):
        return True
    return (
        str(conditions.get("scheduled", "0")) == "0"
        and str(conditions.get("repeat_type", "0")) == "0"
        and str(conditions.get("repeat_count", "0")) == "0"
    )


def phoenix_head_angle(angle):
    try:
        n = float(angle)
    except (TypeError, ValueError):
        return str(angle)
    if abs(n) <= 90:
        return str(int(round(n * 100)))
    return str(angle)


def phoenix_wag_speed(angle=None, percent=None):
    if percent is not None:
        return str(int(round(float(percent) * 100)))
    if angle is None or str(angle).strip() == "":
        return "5000"
    s = str(angle).strip()
    try:
        n = float(s)
        if 0 <= n <= 100 and "/" not in s and "&" not in s:
            return str(int(round(n * 100)))
    except (TypeError, ValueError):
        pass
    return s


def build_phoenix_play_action(action_type, angle="0", move_time_ms=None, count="0"):
    t = str(action_type)
    if move_time_ms is None:
        move_time_ms = PHOENIX_DEFAULT_MOVE
    if t in PHOENIX_MINIMAL_TYPES:
        return {"type": t}
    if t in PHOENIX_ZERO_FIELD_TYPES:
        return {"type": t, "angle": "0", "moveTimeMs": "0", "count": "0"}
    if t == "wag_tail":
        return {
            "type": "wag_tail",
            "angle": phoenix_wag_speed(angle),
            "moveTimeMs": str(move_time_ms),
            "count": "0",
        }
    if t in PHOENIX_HEAD_TYPES:
        angle = phoenix_head_angle(angle)
    elif t in PHOENIX_EMOTION_TYPES:
        if angle is None or str(angle).strip() in ("", "0"):
            angle = "level1/1"
        move_time_ms = PHOENIX_DEFAULT_MOVE
    elif t == "special":
        if angle is None or str(angle).strip() == "":
            angle = "sleepy-1"
        move_time_ms = PHOENIX_DEFAULT_MOVE
    elif t == "set_heart":
        move_time_ms = "0" if move_time_ms is None else move_time_ms
    return {
        "type": t,
        "angle": str(angle),
        "moveTimeMs": str(move_time_ms),
        "count": str(count),
    }


def legacy_action_to_phoenix(action):
    if not isinstance(action, dict):
        return None
    t = str(action.get("type") or "").strip()
    if not t:
        return None
    if t in PHOENIX_MINIMAL_TYPES:
        return {"type": t}
    if t == "play_sound":
        voice = action.get("angle") or action.get("file")
        if not voice:
            return None
        return build_phoenix_play_action(
            "play_sound",
            voice,
            action.get("moveTimeMs", PHOENIX_DEFAULT_MOVE),
            action.get("count", "1"),
        )
    if t in PHOENIX_HEAD_TYPES:
        return build_phoenix_play_action(
            t,
            phoenix_head_angle(action.get("angle", "0")),
            action.get("moveTimeMs", PHOENIX_DEFAULT_MOVE),
            action.get("count", "1"),
        )
    if t == "wag_tail":
        return {
            "type": "wag_tail",
            "angle": phoenix_wag_speed(action.get("angle"), action.get("percent")),
            "moveTimeMs": str(action.get("moveTimeMs", PHOENIX_DEFAULT_MOVE)),
            "count": "0",
        }
    if t == "reset":
        return build_phoenix_play_action("reset")
    if t in PHOENIX_EMOTION_TYPES:
        return build_phoenix_play_action(
            t,
            action.get("angle", "level1/1"),
            action.get("moveTimeMs", PHOENIX_DEFAULT_MOVE),
            action.get("count", "0"),
        )
    if t == "special":
        return build_phoenix_play_action(
            "special",
            action.get("angle", "sleepy-1"),
            action.get("moveTimeMs", PHOENIX_DEFAULT_MOVE),
            action.get("count", "0"),
        )
    if t == "set_heart":
        return build_phoenix_play_action(
            "set_heart",
            action.get("angle", "0"),
            action.get("moveTimeMs", "0"),
            action.get("count", "0"),
        )
    return None


def send_play_action_gateway(
    ak, nick, action_type, *, angle="0", move_time_ms=None, count="0", msg_id=None
):
    data = build_phoenix_play_action(action_type, angle, move_time_ms, count)
    return send_display_gateway(ak, nick, "play_action", data, msg_id)


def send_single_display(ak, nick, action_type, extra=None, msg_id=None):
    """单动作走 Phoenix play_action；带 conditions 时走 action_sequence。"""
    extra = dict(extra or {})
    user_timing = pop_user_timing_flag(extra)
    conditions = extra.pop("conditions", None) if isinstance(extra.get("conditions"), dict) else None
    if conditions and not conditions_empty(conditions):
        user_timing = user_timing or conditions_imply_user_timing(conditions)
        actions = sanitize_sequence_actions([{**{"type": action_type}, **extra}], user_timing=user_timing)
        return send_action_sequence_gateway(
            ak, nick, actions, {}, conditions, msg_id, user_timing=user_timing
        )
    phoenix = legacy_action_to_phoenix({"type": action_type, **extra})
    if phoenix:
        validate_play_action_timing(phoenix, user_timing=user_timing, label=f"play_action({action_type})")
        return send_display_gateway(ak, nick, "play_action", phoenix, msg_id)
    return send_play_action_gateway(
        ak,
        nick,
        action_type,
        extra.get("angle", "0"),
        extra.get("moveTimeMs"),
        extra.get("count", "0"),
        msg_id,
    )


def build_action_sequence(actions, variables=None, conditions=None, *, user_timing=False):
    if not isinstance(actions, list) or not actions:
        raise SystemExit("actions must be a non-empty array")
    ut = user_timing or conditions_imply_user_timing(conditions)
    actions = sanitize_sequence_actions(actions, user_timing=ut)
    return {
        "variables": variables if isinstance(variables, dict) else {},
        "conditions": conditions if isinstance(conditions, dict) else {},
        "actions": actions,
    }


def build_conditions(scheduled="0", repeat_type="0", repeat_count="0", **extra):
    """Device-side schedule fields for action_sequence (see references/action-sequence.md)."""
    out = {
        "scheduled": str(scheduled),
        "repeat_type": str(repeat_type),
        "repeat_count": str(repeat_count),
    }
    for key, value in extra.items():
        if value is not None:
            out[key] = str(value)
    return out


def build_staggered_play_sound_actions(file, move_time_ms, interval_ms, times, start_delay_ms=0):
    """Chain play_sound steps with increasing delay (ms) for one-shot display sequences."""
    out = []
    for i in range(int(times)):
        out.append(
            {
                "type": "play_sound",
                "file": str(file),
                "moveTimeMs": str(move_time_ms),
                "count": "1",
                "delay": str(int(start_delay_ms) + i * int(interval_ms)),
            }
        )
    return out


# action_sequence 编排：默认时长与 beat 间隔（毫秒）
SEQUENCE_DEFAULT_MOVE_MS = {
    "play_sound": 3000,
    "nod_head": 800,
    "shake_head": 800,
    "cock_head": 800,
    "wag_tail": 1200,
    "eye_control": 500,
}
DEFAULT_CHOREOGRAPHY_GAP_MS = 150
# 技能编排默认用时上限（ms）；用户 JSON 设 user_timing:true 或定时 conditions 时不限制
MAX_SINGLE_ACTION_SPAN_MS = 10_000
MAX_DEFAULT_SEQUENCE_TOTAL_MS = 20_000
PLAY_ACTION_DEFAULT_MOVE_MS = {
    "play_sound": 3000,
    "nod_head": 800,
    "shake_head": 800,
    "cock_head": 800,
    "wag_tail": 1200,
}


def timing_checks_disabled():
    return truthy_env("ECOVACS_SKIP_TIMING_LIMIT")


def truthy_flag(value):
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).strip().lower() in ("1", "true", "yes", "on")


def pop_user_timing_flag(obj):
    """Remove skill-only flags; return whether user explicitly allows long timing."""
    if not isinstance(obj, dict):
        return False
    ut = truthy_flag(obj.pop("user_timing", None)) or truthy_flag(obj.pop("allow_long_timing", None))
    return ut


def conditions_imply_user_timing(conditions):
    if not isinstance(conditions, dict):
        return False
    if str(conditions.get("scheduled", "0")).strip() not in ("", "0"):
        return True
    if str(conditions.get("repeat_type", "0")).strip() not in ("", "0"):
        return True
    if str(conditions.get("repeat_count", "0")).strip() not in ("", "0"):
        return True
    return False


def sequence_int_field(value, default):
    if value is None or str(value).strip() in ("", "-1"):
        return int(default)
    try:
        return max(0, int(float(value)))
    except (TypeError, ValueError):
        return int(default)


def estimate_action_duration_ms(action):
    """Heuristic duration for chaining action_sequence delays (ms)."""
    if not isinstance(action, dict):
        return 1000
    t = str(action.get("type") or "").strip()
    move_ms = sequence_int_field(action.get("moveTimeMs"), SEQUENCE_DEFAULT_MOVE_MS.get(t, 1000))
    count = sequence_int_field(action.get("count"), 1)
    if t == "play_sound":
        return move_ms * max(1, count)
    if t in PHOENIX_HEAD_TYPES:
        return move_ms if count <= 1 else move_ms * count * 2
    if t == "eye_control":
        return move_ms * max(1, count)
    return move_ms


def estimate_play_action_duration_ms(phoenix_data):
    """Estimate play_action step duration (no delay field)."""
    if not isinstance(phoenix_data, dict):
        return 1000
    t = str(phoenix_data.get("type") or "").strip()
    if t in PHOENIX_MINIMAL_TYPES or t in PHOENIX_ZERO_FIELD_TYPES:
        return 0
    default_ms = PLAY_ACTION_DEFAULT_MOVE_MS.get(t, 1000)
    move_ms = sequence_int_field(phoenix_data.get("moveTimeMs"), default_ms)
    count = sequence_int_field(phoenix_data.get("count"), 1 if t in PHOENIX_HEAD_TYPES else 0)
    if t == "play_sound":
        return move_ms * max(1, count or 1)
    if t in PHOENIX_HEAD_TYPES:
        return move_ms if count <= 1 else move_ms * count * 2
    return move_ms


def estimate_sequence_action_span_ms(action):
    """Per-step span: delay + duration (action_sequence)."""
    if not isinstance(action, dict):
        return 0
    delay = sequence_int_field(action.get("delay"), 0)
    return delay + estimate_action_duration_ms(action)


def estimate_sequence_total_span_ms(actions):
    if not isinstance(actions, list) or not actions:
        return 0
    return max(estimate_sequence_action_span_ms(a) for a in actions if isinstance(a, dict))


def validate_play_action_timing(phoenix_data, *, user_timing=False, label="play_action"):
    if timing_checks_disabled() or user_timing:
        return
    span = estimate_play_action_duration_ms(phoenix_data)
    if span > MAX_SINGLE_ACTION_SPAN_MS:
        raise SystemExit(
            f"{label} 预估用时 {span}ms 超过单动作默认上限 {MAX_SINGLE_ACTION_SPAN_MS}ms。"
            f"请缩短 moveTimeMs/count，或 JSON 加 \"user_timing\": true 表示用户指定用时。"
        )


def validate_sequence_timing(actions, *, user_timing=False):
    if timing_checks_disabled() or user_timing:
        return
    if not isinstance(actions, list):
        raise SystemExit("actions must be an array")
    for i, action in enumerate(actions):
        if not isinstance(action, dict):
            continue
        span = estimate_sequence_action_span_ms(action)
        t = action.get("type", "?")
        if span > MAX_SINGLE_ACTION_SPAN_MS:
            raise SystemExit(
                f"编排 actions[{i}] type={t} 预估 delay+duration={span}ms，"
                f"超过单步默认上限 {MAX_SINGLE_ACTION_SPAN_MS}ms。"
                f"请缩短 delay/moveTimeMs/count，或加 \"user_timing\": true。"
            )
    total = estimate_sequence_total_span_ms(actions)
    if total > MAX_DEFAULT_SEQUENCE_TOTAL_MS:
        raise SystemExit(
            f"编排整段预估结束时间 {total}ms 超过默认上限 {MAX_DEFAULT_SEQUENCE_TOTAL_MS}ms。"
            f"请减少步骤/时长，或使用 build_dance_sequence；"
            f"用户指定长编排时在根 JSON 加 \"user_timing\": true。"
        )


def sanitize_sequence_actions(actions, user_timing=False):
    if not isinstance(actions, list) or not actions:
        raise SystemExit("actions must be a non-empty array")
    ut = user_timing
    cleaned = []
    for raw in actions:
        if not isinstance(raw, dict):
            raise SystemExit("each action must be an object")
        a = dict(raw)
        if pop_user_timing_flag(a):
            ut = True
        cleaned.append(a)
    validate_sequence_timing(cleaned, user_timing=ut)
    return cleaned


def validate_play_sound_body(body, *, user_timing=False):
    if timing_checks_disabled() or user_timing:
        return
    count = sequence_int_field((body or {}).get("count"), 1)
    move_ms = sequence_int_field((body or {}).get("moveTimeMs"), PLAY_ACTION_DEFAULT_MOVE_MS["play_sound"])
    span = move_ms * max(1, count)
    if span > MAX_SINGLE_ACTION_SPAN_MS:
        raise SystemExit(
            f"playSound 预估用时 {span}ms 超过默认上限 {MAX_SINGLE_ACTION_SPAN_MS}ms；"
            f"请减小 count/moveTimeMs 或加 \"user_timing\": true。"
        )


def normalize_sequence_action(action):
    """Fill sensible defaults before assigning delay (action_sequence uses degree/percent)."""
    a = dict(action)
    t = str(a.get("type") or "")
    if t in PHOENIX_HEAD_TYPES:
        if "ctrlpoint" not in a:
            a["ctrlpoint"] = ""
        if a.get("moveTimeMs") in (None, "", "-1"):
            a["moveTimeMs"] = str(SEQUENCE_DEFAULT_MOVE_MS[t])
        if a.get("count") in (None, ""):
            a["count"] = "1"
    if t == "wag_tail" and a.get("moveTimeMs") in (None, "", "-1"):
        a["moveTimeMs"] = str(SEQUENCE_DEFAULT_MOVE_MS["wag_tail"])
    if t == "play_sound" and a.get("moveTimeMs") in (None, "", "-1"):
        a["moveTimeMs"] = str(SEQUENCE_DEFAULT_MOVE_MS["play_sound"])
    if t == "eye_control":
        if a.get("moveTimeMs") in (None, "", "-1"):
            a["moveTimeMs"] = str(SEQUENCE_DEFAULT_MOVE_MS["eye_control"])
        if a.get("eyetype") in (None, ""):
            a["eyetype"] = "3"
        if a.get("direct") in (None, ""):
            a["direct"] = "0"
        if a.get("narrow") in (None, ""):
            a["narrow"] = "0"
        if a.get("percent") in (None, ""):
            a["percent"] = "80"
        if a.get("count") in (None, ""):
            a["count"] = "1"
        if a.get("blinkMoveTime") in (None, ""):
            a["blinkMoveTime"] = str(max(200, int(a["moveTimeMs"]) // 2))
    return a


def apply_staggered_delays(actions, start_delay_ms=0, gap_ms=DEFAULT_CHOREOGRAPHY_GAP_MS):
    """Sequential steps: delay[i+1] ≈ delay[i] + duration[i] + gap."""
    out = []
    cursor = int(start_delay_ms)
    gap = max(0, int(gap_ms))
    for raw in actions:
        a = normalize_sequence_action(raw)
        a["delay"] = str(cursor)
        out.append(a)
        cursor += estimate_action_duration_ms(a) + gap
    return out


def apply_beat_delays(beats, start_delay_ms=0, gap_ms=DEFAULT_CHOREOGRAPHY_GAP_MS):
    """
    beats: [action, action, ...] sequential, or nested [action, action] for parallel same delay.
    """
    out = []
    cursor = int(start_delay_ms)
    gap = max(0, int(gap_ms))
    for beat in beats:
        group = beat if isinstance(beat, list) else [beat]
        normalized = [normalize_sequence_action(a) for a in group]
        delay = str(cursor)
        for a in normalized:
            a["delay"] = delay
            out.append(a)
        cursor += max(estimate_action_duration_ms(a) for a in normalized) + gap
    return out


DANCE_LENGTH_ALIASES = {
    "short": "short",
    "s": "short",
    "短": "short",
    "短舞": "short",
    "medium": "medium",
    "m": "medium",
    "mid": "medium",
    "中": "medium",
    "中舞": "medium",
    "long": "long",
    "l": "long",
    "长": "long",
    "长舞": "long",
}

DANCE_LENGTH_TARGET_MS = {
    "short": (10_000, 20_000),
    "medium": (20_000, 30_000),
    "long": (30_000, 60_000),
}

DANCE_LENGTH_REPEATS = {
    "short": 2,
    "medium": 4,
    "long": 7,
}

DANCE_ROUND_GAP_MS = 300


def shift_sequence_delays(actions, offset_ms):
    """Shift every action_sequence delay by offset_ms."""
    offset = int(offset_ms)
    out = []
    for raw in actions:
        a = normalize_sequence_action(raw)
        a["delay"] = str(sequence_int_field(a.get("delay"), 0) + offset)
        out.append(a)
    return out


def build_dance_bookend_barks(meta, start_delay_ms=0):
    """Triple bark block for dance open/close."""
    from dance_choreography import (
        DANCE_BOOKEND_BARK_COUNT,
        bookend_bark_config,
    )

    tempo = meta.get("tempo") or "normal"
    vf, move_ms, interval = bookend_bark_config(tempo)
    return build_staggered_play_sound_actions(
        vf,
        move_ms,
        interval,
        DANCE_BOOKEND_BARK_COUNT,
        start_delay_ms=start_delay_ms,
    )


def dance_bookend_overhead_ms(meta):
    """Extra ms for open + close triple-barks and gaps before/after body."""
    from dance_choreography import DANCE_BOOKEND_BODY_GAP_MS

    gap = int(DANCE_BOOKEND_BODY_GAP_MS)
    block = build_dance_bookend_barks(meta, 0)
    block_span = estimate_sequence_total_span_ms(block)
    return block_span + gap + block_span + gap


def normalize_dance_length(length):
    key = str(length or "short").strip().lower()
    resolved = DANCE_LENGTH_ALIASES.get(key)
    if not resolved:
        known = ", ".join(sorted(set(DANCE_LENGTH_ALIASES.values())))
        raise SystemExit(f"未知跳舞时长: {length!r}。可选: {known}")
    return resolved


def normalize_dance_style(style):
    """Backward-compatible alias → routine id."""
    return normalize_dance_routine(style)


def dance_repeats_for_length(length):
    return DANCE_LENGTH_REPEATS[normalize_dance_length(length)]


def expand_dance_beats(
    beats,
    repeats=1,
    gap_ms=DEFAULT_CHOREOGRAPHY_GAP_MS,
    round_gap_ms=DANCE_ROUND_GAP_MS,
):
    """Repeat the same beat pattern N times with shifted delay (controls total duration)."""
    reps = max(1, int(repeats))
    if reps == 1:
        return apply_beat_delays(beats, gap_ms=gap_ms)
    out = []
    cursor = 0
    for _ in range(reps):
        round_actions = apply_beat_delays(beats, start_delay_ms=cursor, gap_ms=gap_ms)
        out.extend(round_actions)
        cursor = estimate_sequence_total_span_ms(round_actions) + int(round_gap_ms)
    return out


def _routine_gap_ms(meta):
    from dance_choreography import TEMPO_PROFILES

    tempo = meta.get("tempo") or "normal"
    return TEMPO_PROFILES.get(tempo, TEMPO_PROFILES["normal"])["beat_gap_ms"]


def _flow_repeats_for_length(beats, length, gap_ms, extra_ms=0):
    """Pick repeat count so total duration lands near the length tier (via repetition)."""
    lo, hi = DANCE_LENGTH_TARGET_MS[normalize_dance_length(length)]
    strict_hi = int(hi * 1.05)
    slack_hi = hi + 4000
    target_mid = (lo + hi) / 2
    extra = max(0, int(extra_ms))

    def pick_best(max_hi):
        best_reps = None
        best_dist = float("inf")
        fallback = 1
        for reps in range(1, 13):
            body = estimate_sequence_total_span_ms(expand_dance_beats(beats, reps, gap_ms=gap_ms))
            total = body + extra
            if total < lo:
                fallback = reps
            if lo <= total <= max_hi:
                dist = abs(total - target_mid)
                if dist < best_dist:
                    best_dist = dist
                    best_reps = reps
        return best_reps, fallback

    best, fallback = pick_best(strict_hi)
    if best is not None:
        return best
    best, fallback = pick_best(slack_hi)
    if best is not None:
        return best
    return max(1, fallback)


def compile_dance_routine_actions(routine_id, length):
    rid = normalize_dance_routine(routine_id)
    meta = get_dance_routine_meta(rid)
    length = normalize_dance_length(length)

    from dance_choreography import DANCE_BOOKEND_BODY_GAP_MS

    if meta.get("timing") == "script":
        body = sanitize_sequence_actions(meta["build"](), user_timing=True)
    else:
        beats = meta["build"]()
        gap_ms = _routine_gap_ms(meta)
        overhead = dance_bookend_overhead_ms(meta)
        repeats = _flow_repeats_for_length(beats, length, gap_ms, extra_ms=overhead)
        body = expand_dance_beats(beats, repeats, gap_ms=gap_ms)

    bookend_gap = int(DANCE_BOOKEND_BODY_GAP_MS)
    if meta.get("bookends") is False:
        return body

    prefix = build_dance_bookend_barks(meta, 0)
    body_start = estimate_sequence_total_span_ms(prefix) + bookend_gap
    body = shift_sequence_delays(body, body_start)
    suffix_start = estimate_sequence_total_span_ms(body) + bookend_gap
    suffix = build_dance_bookend_barks(meta, suffix_start)
    return prefix + body + suffix


def list_dance_routines():
    return sorted((rid, length) for rid in list_dance_routine_ids() for length in DANCE_LENGTH_REPEATS)


def estimate_dance_duration_ms(routine=None, length="short"):
    rid = normalize_dance_routine(routine or DEFAULT_DANCE_ROUTINE)
    actions = compile_dance_routine_actions(rid, length)
    return estimate_sequence_total_span_ms(actions)


def build_dance_sequence(routine=None, length="short"):
    """Build preset dance action_sequence payload."""
    rid = normalize_dance_routine(routine or DEFAULT_DANCE_ROUTINE)
    length = normalize_dance_length(length)
    actions = compile_dance_routine_actions(rid, length)
    total_ms = estimate_sequence_total_span_ms(actions)
    meta = get_dance_routine_meta(rid)
    if meta.get("timing") != "script":
        lo, hi = DANCE_LENGTH_TARGET_MS[length]
        if total_ms < lo * 0.85 or total_ms > hi * 1.05:
            print(
                f"[dance] WARN: {rid}/{length} 预估 {total_ms}ms，目标 {lo}–{hi}ms",
                file=sys.stderr,
            )
    return build_action_sequence(actions, conditions=build_conditions(), user_timing=True)


def build_default_dance_sequence():
    return build_dance_sequence(DEFAULT_DANCE_ROUTINE, "short")


def send_cmd_gateway(ak, nick, cmd_name, body_data=None):
    return skill_pet_cmd(ak, nick, cmd_name, body_data if body_data is not None else {})


def send_display_gateway(ak, nick, action_cmd, action_data=None, msg_id=None):
    body = {
        "msgId": msg_id or str(int(time.time() * 1000)),
        "cmd": action_cmd,
        "data": action_data or {},
    }
    return send_cmd_gateway(ak, nick, "display", body)


def send_action_sequence_gateway(
    ak, nick, actions, variables=None, conditions=None, msg_id=None, *, user_timing=False
):
    ut = user_timing or conditions_imply_user_timing(conditions)
    payload = build_action_sequence(actions, variables, conditions, user_timing=ut)
    return send_display_gateway(ak, nick, "action_sequence", payload, msg_id)


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(0)

    cmd = args[0]

    if cmd == "set-ak":
        if len(args) < 2:
            print("用法: python3 ecovacs.py set-ak <ak>")
            sys.exit(1)
        save_ak(args[1])
        sys.exit(0)

    ak = load_ak()

    if cmd == "devices":
        print_devices(skill_device_list(ak))
        sys.exit(0)

    if cmd == "cmd":
        if len(args) < 3:
            print("用法: python3 ecovacs.py cmd <nickName> <cmdName> [json_body]")
            sys.exit(1)
        nick = args[1]
        cmd_name = args[2]
        body = parse_json_arg(args[3], {}) if len(args) > 3 else {}
        if cmd_name == "playSound" and isinstance(body, dict):
            user_timing = pop_user_timing_flag(body)
            if conditions_imply_user_timing(body.get("conditions")):
                user_timing = True
            extra_actions = body.get("actions")
            if isinstance(extra_actions, list):
                body["actions"] = sanitize_sequence_actions(extra_actions, user_timing=user_timing)
            else:
                validate_play_sound_body(body, user_timing=user_timing)
        if cmd_name == "display" and display_requires_wake(body):
            ensure_pet_awake(ak, nick)
        out = send_cmd_gateway(ak, nick, cmd_name, body)
        print(json.dumps(out, indent=2, ensure_ascii=False))
        sys.exit(0)

    if cmd == "display":
        if len(args) < 3:
            print("Usage:")
            print("  python3 ecovacs.py display <nickName> action <type> [json_data] [msg_id]")
            print("  python3 ecovacs.py display <nickName> actions <json_actions_array> [json_variables] [msg_id]")
            print("  python3 ecovacs.py display <nickName> sleep [msg_id]")
            print("  python3 ecovacs.py display <nickName> clear-scheduled [msg_id]")
            print("  python3 ecovacs.py display <nickName> reset [msg_id]")
            print("  python3 ecovacs.py display <nickName> dance [routine] [length] [msg_id]")
            print("  python3 ecovacs.py display <nickName> sequence <json_sequence> [msg_id]")
            sys.exit(1)
        nick = args[1]
        sub = args[2]

        if sub == "action":
            if len(args) < 4:
                raise SystemExit(
                    "Usage: python3 ecovacs.py display <nickName> action <type> [json_data] [msg_id]"
                )
            action_type = args[3]
            extra = parse_json_arg(args[4], {}) if len(args) > 4 else {}
            if not isinstance(extra, dict):
                raise SystemExit("json_data must be an object")
            clean_extra = {k: v for k, v in extra.items() if k != "type"}
            msg_id = args[5] if len(args) > 5 else None
            if action_type not in PHOENIX_MINIMAL_TYPES:
                ensure_pet_awake(ak, nick)
            result = send_single_display(ak, nick, action_type, clean_extra, msg_id)
        elif sub == "sleep":
            msg_id = args[3] if len(args) > 3 else None
            result = send_play_action_gateway(ak, nick, "sleep", msg_id=msg_id)
        elif sub in ("clear-scheduled", "clear_scheduled"):
            msg_id = args[3] if len(args) > 3 else None
            result = send_play_action_gateway(ak, nick, "clear_scheduled", msg_id=msg_id)
        elif sub == "reset":
            msg_id = args[3] if len(args) > 3 else None
            result = send_play_action_gateway(ak, nick, "reset", msg_id=msg_id)
        elif sub == "dance":
            routine = args[3] if len(args) > 3 else DEFAULT_DANCE_ROUTINE
            length = "short"
            msg_id = None
            if len(args) > 4:
                maybe_len = str(args[4]).strip().lower()
                if maybe_len in DANCE_LENGTH_ALIASES:
                    length = args[4]
                    msg_id = args[5] if len(args) > 5 else None
                else:
                    msg_id = args[4]
            payload = build_dance_sequence(routine, length)
            ensure_pet_awake(ak, nick)
            result = send_action_sequence_gateway(
                ak,
                nick,
                payload["actions"],
                payload.get("variables"),
                payload.get("conditions"),
                msg_id,
                user_timing=True,
            )
        elif sub == "actions":
            if len(args) < 4:
                raise SystemExit(
                    "Usage: python3 ecovacs.py display <nickName> actions <json_actions_array> "
                    "[json_variables] [json_conditions] [msg_id]"
                )
            actions = parse_json_arg(args[3], [])
            if not isinstance(actions, list):
                raise SystemExit("json_actions_array must be an array")
            user_timing = False
            cleaned = []
            for a in actions:
                if isinstance(a, dict):
                    ac = dict(a)
                    if pop_user_timing_flag(ac):
                        user_timing = True
                    cleaned.append(ac)
                else:
                    cleaned.append(a)
            actions = cleaned
            variables = parse_json_arg(args[4], {}) if len(args) > 4 else {}
            if not isinstance(variables, dict):
                raise SystemExit("json_variables must be an object")
            conditions = parse_json_arg(args[5], {}) if len(args) > 5 else {}
            if not isinstance(conditions, dict):
                raise SystemExit("json_conditions must be an object")
            if conditions_imply_user_timing(conditions):
                user_timing = True
            msg_id = args[6] if len(args) > 6 else None
            ensure_pet_awake(ak, nick)
            result = send_action_sequence_gateway(
                ak, nick, actions, variables, conditions, msg_id, user_timing=user_timing
            )
        elif sub == "personality":
            raise SystemExit(
                "display personality is disabled. Query via: python3 ecovacs.py cmd <nick> getPerson '{}'"
            )
        elif sub == "sequence":
            if len(args) < 4:
                raise SystemExit("Usage: python3 ecovacs.py display <nickName> sequence <json_sequence> [msg_id]")
            payload = parse_json_arg(args[3], {})
            user_timing = False
            if isinstance(payload, list):
                actions = payload
                variables = {}
                conditions = {}
            elif isinstance(payload, dict):
                user_timing = pop_user_timing_flag(payload)
                actions = payload.get("actions")
                variables = payload.get("variables", {})
                conditions = payload.get("conditions", {})
            else:
                raise SystemExit("json_sequence must be an array or an object")
            if conditions_imply_user_timing(conditions):
                user_timing = True
            msg_id = args[4] if len(args) > 4 else None
            if (
                isinstance(actions, list)
                and len(actions) == 1
                and conditions_empty(conditions)
                and (not variables or variables == {})
            ):
                phoenix = legacy_action_to_phoenix(actions[0])
                if phoenix:
                    if str(phoenix.get("type")) not in PHOENIX_MINIMAL_TYPES:
                        ensure_pet_awake(ak, nick)
                    validate_play_action_timing(phoenix, user_timing=user_timing, label="play_action")
                    result = send_display_gateway(ak, nick, "play_action", phoenix, msg_id)
                else:
                    ensure_pet_awake(ak, nick)
                    result = send_action_sequence_gateway(
                        ak, nick, actions, variables, conditions, msg_id, user_timing=user_timing
                    )
            else:
                ensure_pet_awake(ak, nick)
                result = send_action_sequence_gateway(
                    ak, nick, actions, variables, conditions, msg_id, user_timing=user_timing
                )
        else:
            raise SystemExit(
                "Unsupported display subcommand. Use one of: action, actions, dance, sleep, clear-scheduled, reset, sequence"
            )
        print(json.dumps(result, indent=2, ensure_ascii=False))
        sys.exit(0)

    print(f"Unknown command: {cmd}")
    print(__doc__)
    sys.exit(1)
