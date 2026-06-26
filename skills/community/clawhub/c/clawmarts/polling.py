#!/usr/bin/env python3
"""
ClawMarts WebSocket Helper Script
WebSocket 长连接保活 + 自动接单（抢单/竞标/赛马）+ 自动执行任务
用法: python polling.py [--config PATH]
"""
import json
import os
import sys
import time
import random
import argparse
import threading

# ── 依赖自动检查与安装引导 ──
_MISSING_DEPS = []

try:
    import requests
except ImportError:
    _MISSING_DEPS.append("requests")

try:
    import websocket as ws_lib  # websocket-client
except ImportError:
    _MISSING_DEPS.append("websocket-client")


def _check_and_install_deps():
    """检查缺失依赖，引导用户手动安装"""
    if not _MISSING_DEPS:
        return True

    print(f"  ❌ 缺失依赖: {', '.join(_MISSING_DEPS)}", file=sys.stderr)
    print(f"  请手动安装后重新运行:", file=sys.stderr)
    print(f"     {sys.executable} -m pip install {' '.join(_MISSING_DEPS)}", file=sys.stderr)
    sys.exit(1)


DEFAULT_CONFIG = os.path.expanduser(
    "~/.openclaw/skills/clawmarts/config.json"
)

# ── 全局状态 ──
ws_connected = threading.Event()
stop_event = threading.Event()
_ws_disconnect_time = 0.0       # 最近一次断连的时间戳
_ws_reconnect_attempts = 0      # 当前连续重连次数
_ws_was_connected = False        # 是否曾经成功连接过

# P2-#18: WS/HTTP 双通道状态同步 — 本地任务状态缓存
_task_cache_lock = threading.Lock()
_local_task_cache: dict[str, dict] = {}     # task_id -> task dict
_task_cache_last_sync: float = 0.0          # 上次 API 全量同步时间
_CACHE_SYNC_INTERVAL = 300                  # 强制同步间隔 (5 分钟)（区分首次连接失败和掉线）

# WS 优先架构 — 全局 WebSocket 对象，主线程可通过它发送命令
_ws_lock = threading.Lock()
_ws_obj = None  # type: ws_lib.WebSocket | None

# WS 请求响应等待机制 (request_id -> Event + result)
_ws_pending: dict[str, dict] = {}  # {request_id: {"event": Event, "result": dict|None}}


def load_config(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_config(path: str, cfg: dict):
    """保存配置到文件"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)


def api(method: str, path: str, cfg: dict, **kwargs):
    """统一 HTTP API 调用，包含 401 自动刷新 Token"""
    url = f"{cfg['clawnet_api_url']}{path}"
    headers = kwargs.pop("headers", {})
    headers["Authorization"] = f"Bearer {cfg['token']}"
    headers.setdefault("Content-Type", "application/json")
    try:
        resp = getattr(requests, method)(url, headers=headers, timeout=90, **kwargs)
        # P0 优化: 401 自动刷新 Token，避免过期后大量无效请求
        if resp.status_code == 401 and cfg.get("refresh_token"):
            new_token = _try_refresh_token(cfg)
            if new_token:
                headers["Authorization"] = f"Bearer {new_token}"
                resp = getattr(requests, method)(url, headers=headers, timeout=90, **kwargs)
        return resp.json()
    except Exception as e:
        print(f"  ⚠️  API error [{method.upper()} {path}]: {e}", file=sys.stderr)
        return None


def _try_refresh_token(cfg: dict) -> str | None:
    """尝试使用 refresh_token 获取新的 access_token"""
    try:
        url = f"{cfg['clawnet_api_url']}/api/auth/refresh"
        resp = requests.post(url, json={
            "refresh_token": cfg["refresh_token"],
        }, timeout=10)
        data = resp.json()
        if data.get("success") and data.get("access_token"):
            cfg["token"] = data["access_token"]
            if data.get("refresh_token"):
                cfg["refresh_token"] = data["refresh_token"]
            # 尝试保存配置
            config_path = cfg.get("_config_path", "")
            if config_path:
                save_config(config_path, {
                    k: v for k, v in cfg.items() if k != "_config_path"
                })
            print("  🔄 Token 已自动刷新")
            return data["access_token"]
    except Exception as e:
        print(f"  ⚠️  Token 刷新失败: {e}", file=sys.stderr)
    return None


def _safe_float(val, default=0.0) -> float:
    """安全地将任意值转为 float，避免 str vs float 比较错误"""
    if val is None:
        return default
    try:
        return float(val)
    except (ValueError, TypeError):
        return default


# ── WS 优先: 请求-响应机制 ──


def _ws_send_request(msg: dict, timeout: float = 10.0) -> dict | None:
    """通过 WebSocket 发送请求并等待响应

    利用 request_id 关联请求和响应。WS 不可用或超时返回 None。
    主线程调用，WS 线程负责收消息并唤醒等待。
    """
    if not ws_connected.is_set():
        return None

    import uuid
    request_id = uuid.uuid4().hex[:12]
    msg["request_id"] = request_id

    # 注册等待槽
    event = threading.Event()
    _ws_pending[request_id] = {"event": event, "result": None}

    try:
        with _ws_lock:
            if _ws_obj is None:
                return None
            _ws_obj.send(json.dumps(msg, ensure_ascii=False))
    except Exception:
        _ws_pending.pop(request_id, None)
        return None

    # 等待服务端响应
    event.wait(timeout=timeout)
    entry = _ws_pending.pop(request_id, None)
    if entry and entry.get("result") is not None:
        return entry["result"]
    return None


def _ws_dispatch_response(msg: dict):
    """WS 线程收到服务端操作响应时，唤醒等待的主线程

    服务端响应中携带 request_id，用于关联原始请求。
    """
    request_id = msg.get("request_id", "")
    if request_id and request_id in _ws_pending:
        _ws_pending[request_id]["result"] = msg
        _ws_pending[request_id]["event"].set()


# ── WebSocket 长连接 ──


def _build_ws_url(cfg: dict) -> str:
    """根据 API URL 构建 WebSocket URL"""
    base = cfg["clawnet_api_url"]
    if base.startswith("https://"):
        ws_base = "wss://" + base[len("https://"):]
    elif base.startswith("http://"):
        ws_base = "ws://" + base[len("http://"):]
    else:
        ws_base = "ws://" + base
    return f"{ws_base}/ws/claw?token={cfg['token']}&claw_id={cfg['claw_id']}"


def _ws_thread(cfg: dict):
    """WebSocket 线程：保持长连接，定期发 ping 保活

    断连时主动提醒用户，并给出重连操作指引。
    """
    global _ws_disconnect_time, _ws_reconnect_attempts, _ws_was_connected
    url = _build_ws_url(cfg)
    ping_interval = cfg.get("heartbeat_interval", 60)
    reconnect_delay = 5

    while not stop_event.is_set():
        ws = None
        try:
            _ws_reconnect_attempts += 1
            if _ws_reconnect_attempts == 1:
                print(f"  🔌 WebSocket 连接中...")
            else:
                print(f"  🔄 第 {_ws_reconnect_attempts - 1} 次重连中...")

            ws = ws_lib.create_connection(url, timeout=10)
            # 暴露全局 WS 对象，让主线程可以通过它发送命令
            with _ws_lock:
                _ws_obj = ws
            ws_connected.set()

            # ── 连接成功（或重连成功）──
            if _ws_was_connected and _ws_disconnect_time > 0:
                # 这是重连成功的情况
                offline_sec = time.time() - _ws_disconnect_time
                offline_str = _fmt_duration(offline_sec)
                print()
                print("  " + "=" * 46)
                print(f"  ✅ WebSocket 重连成功！(离线 {offline_str})")
                print(f"  ✅ Claw 已恢复在线，可以继续接收任务")
                print("  " + "=" * 46)
                print()
            else:
                print(f"  ✅ WebSocket 已连接 (ping 间隔 {ping_interval}s)")

            _ws_was_connected = True
            _ws_reconnect_attempts = 0
            _ws_disconnect_time = 0.0
            reconnect_delay = 5  # 重置重连延迟

            last_ping = time.time()
            ws.settimeout(5)

            while not stop_event.is_set():
                now = time.time()
                if now - last_ping >= ping_interval:
                    ws.send("ping")
                    last_ping = now

                try:
                    msg = ws.recv()
                    if msg == "pong":
                        pass
                    else:
                        _handle_server_message(msg, cfg)
                except ws_lib.WebSocketTimeoutException:
                    pass
                except ws_lib.WebSocketConnectionClosedException:
                    _notify_disconnect("服务端关闭了连接")
                    break

        except Exception as e:
            _notify_disconnect(str(e))
        finally:
            ws_connected.clear()
            with _ws_lock:
                _ws_obj = None
            if ws:
                try:
                    ws.close()
                except Exception:
                    pass

        if not stop_event.is_set():
            # 记录首次断连时间
            if _ws_disconnect_time == 0:
                _ws_disconnect_time = time.time()

            # 连续重连失败多次，给出详细排查指引
            if _ws_reconnect_attempts >= 5 and _ws_reconnect_attempts % 5 == 0:
                _notify_reconnect_guide(cfg)

            # P0 优化: 添加随机抖动(jitter)，避免平台重启后万台 Agent 同时重连
            jitter = random.uniform(0, min(reconnect_delay, 15))
            print(f"  🔄 {reconnect_delay + jitter:.0f}s 后重连 (delay={reconnect_delay}s + jitter={jitter:.0f}s, 已尝试 {_ws_reconnect_attempts} 次)...")
            stop_event.wait(reconnect_delay + jitter)
            reconnect_delay = min(reconnect_delay * 2, 60)


def _fmt_duration(seconds: float) -> str:
    """格式化时长为人类可读字符串"""
    s = int(seconds)
    if s < 60:
        return f"{s}秒"
    elif s < 3600:
        return f"{s // 60}分{s % 60}秒"
    else:
        h, rem = divmod(s, 3600)
        m = rem // 60
        return f"{h}小时{m}分"


def _notify_disconnect(reason: str):
    """WebSocket 断连时，在终端醒目提示用户"""
    print(file=sys.stderr)
    print("  " + "!" * 50, file=sys.stderr)
    print("  ❌ WebSocket 连接已断开!", file=sys.stderr)
    print(f"  原因: {reason}", file=sys.stderr)
    print("  ", file=sys.stderr)
    print("  ⚠️  离线期间的影响:", file=sys.stderr)
    print("     • 无法接收平台推送的新任务", file=sys.stderr)
    print("     • 无法自动接单和执行任务", file=sys.stderr)
    print("     • 平台会将你的 Claw 标记为离线", file=sys.stderr)
    print("  ", file=sys.stderr)
    print("  🔄 系统将自动尝试重连...", file=sys.stderr)
    print("  " + "!" * 50, file=sys.stderr)
    print(file=sys.stderr)


def _notify_reconnect_guide(cfg: dict):
    """连续重连失败多次后，给出详细排查指引"""
    api_url = cfg.get("clawnet_api_url", "未配置")
    claw_id = cfg.get("claw_id", "未配置")[:8]
    print(file=sys.stderr)
    print("  " + "=" * 50, file=sys.stderr)
    print("  🚨 连续多次重连失败，请检查以下问题:", file=sys.stderr)
    print("  ", file=sys.stderr)
    print("  1️⃣  网络连接", file=sys.stderr)
    print("     检查你的网络是否正常，能否访问平台地址", file=sys.stderr)
    print(f"     平台地址: {api_url}", file=sys.stderr)
    print("  ", file=sys.stderr)
    print("  2️⃣  平台服务", file=sys.stderr)
    print("     平台可能正在维护或重启中，请稍后再试", file=sys.stderr)
    print("     也可在浏览器中打开平台地址确认是否可访问", file=sys.stderr)
    print("  ", file=sys.stderr)
    print("  3️⃣  认证凭证", file=sys.stderr)
    print("     你的 Token 可能已过期，需要重新登录获取", file=sys.stderr)
    print(f"     当前 Claw: {claw_id}...", file=sys.stderr)
    print("     操作方法: 重新运行「连接 ClawMarts」指令", file=sys.stderr)
    print("  ", file=sys.stderr)
    print("  4️⃣  手动操作", file=sys.stderr)
    print("     • 按 Ctrl+C 停止当前程序", file=sys.stderr)
    print("     • 到 ClawMarts 网页端检查 Claw 状态", file=sys.stderr)
    print("     • 重新生成绑定码并连接", file=sys.stderr)
    print("  " + "=" * 50, file=sys.stderr)
    print(file=sys.stderr)


def _handle_server_message(raw: str, cfg: dict):
    """处理服务端推送的消息"""
    try:
        msg = json.loads(raw)
    except json.JSONDecodeError:
        return

    msg_type = msg.get("type", "")

    if msg_type == "task_push":
        task = msg.get("task", {})
        task_id = task.get("task_id", "?")
        desc = task.get("description", "")[:40]
        print(f"  📥 收到推送任务: {task_id[:8]} - {desc}")

    elif msg_type == "task_assigned":
        # 平台服务端直接指派的任务 — 写入本地缓存
        task_id = msg.get("task_id", "?")
        desc = msg.get("description", "")[:40]
        reward = msg.get("reward_amount", "?")
        reason = msg.get("reason", "")
        print()
        print(f"  🎯 收到指派任务!")
        print(f"     任务: {task_id[:8]} - {desc}")
        print(f"     报酬: {reward} Token")
        if reason:
            print(f"     原因: {reason}")
        print()
        # WS 收到即更新本地缓存
        with _task_cache_lock:
            _local_task_cache[task_id] = {
                "task_id": task_id,
                "description": msg.get("description", ""),
                "status": "assigned",
                "reward_amount": reward,
                "_source": "ws",
            }

    elif msg_type == "task_recommend":
        # 平台推荐任务（SDK 可在收到后自动抢单）
        task_id = msg.get("task_id", "?")
        score = msg.get("match_score", "?")
        desc = msg.get("description", "")[:40]
        reward = msg.get("reward_amount", "?")
        print(f"  💡 收到任务推荐: {task_id[:8]} - {desc} (匹配度 {score}, 报酬 {reward}T)")

    elif msg_type == "task_resume":
        # 断点续传：重连后平台推送的未完成任务
        task_id = msg.get("task_id", "?")
        status = msg.get("status", "?")
        desc = msg.get("description", "")[:40]
        reward = msg.get("reward_amount", "?")

        status_labels = {
            "assigned": "待执行",
            "in_progress": "执行中",
            "submitted": "已提交，等待验证",
        }
        status_label = status_labels.get(status, status)

        print()
        print(f"  🔄 断点续传: 恢复未完成任务")
        print(f"     任务: {task_id[:8]} - {desc}")
        print(f"     状态: {status_label}")
        print(f"     报酬: {reward} Token")
        if status == "submitted":
            print(f"     💡 该任务已提交，正在等待平台验证结果")
        elif status in ("assigned", "in_progress"):
            print(f"     💡 该任务需要继续执行并提交结果")
        print()
        # WS 收到断点续传 — 写入本地缓存
        with _task_cache_lock:
            _local_task_cache[task_id] = {
                "task_id": task_id,
                "description": msg.get("description", ""),
                "status": status,
                "reward_amount": reward,
                "_source": "ws",
            }

    elif msg_type == "task_reclaimed":
        task_id = msg.get("task_id", "?")
        reason = msg.get("reason", "")
        print(f"  ⚠️  任务被收回: {task_id[:8]} - {reason}")
        # WS 收到收回通知 — 从缓存移除
        with _task_cache_lock:
            _local_task_cache.pop(task_id, None)

    elif msg_type == "task_timeout_warning":
        task_id = msg.get("task_id", "?")
        remaining = msg.get("remaining_minutes", "?")
        print(f"  ⏰ 超时预警: 任务 {task_id[:8]} 剩余 {remaining} 分钟")

    elif msg_type == "progress_request":
        task_id = msg.get("task_id", "?")
        print(f"  📋 平台请求进度汇报: {task_id[:8]}")

    elif msg_type in ("heartbeat_ack", "progress_ack"):
        pass  # 心跳/进度确认

    # WS 优先架构: 服务端操作响应 → 唤醒主线程等待
    elif msg_type in (
        "grab_result", "submit_ack",
        "next_action_result", "abandon_result", "query_tasks_result",
    ):
        _ws_dispatch_response(msg)

    # ── 任务验证结果反馈 ──
    elif msg_type == "submit_validation":
        request_id = msg.get("request_id", "")
        # 如果有主线程在等待此响应，先分发
        if request_id and request_id in _ws_pending:
            _ws_dispatch_response(msg)
        # 不论是否有等待者，都要处理验证结果
        task_id = msg.get("task_id", msg.get("task", {}).get("task_id", "?"))
        success = msg.get("success", False)
        message = msg.get("message", "")[:80]
        if success:
            print(f"  ✅ 验证通过: {task_id[:8]} - {message}")
        else:
            print(f"  ❌ 验证失败: {task_id[:8]} - {message}")
            print(f"     💡 任务将回到待执行队列，自动重试")
            # 验证失败 → 任务回到 in_progress → 写回本地缓存等待重新执行
            with _task_cache_lock:
                if task_id in _submitted_tasks:
                    _submitted_tasks.discard(task_id)
                _local_task_cache[task_id] = {
                    "task_id": task_id,
                    "status": "in_progress",
                    "_source": "ws_validation_failed",
                    "_retry": True,
                }

    # ── 分阶段任务通知 ──
    elif msg_type == "stage_confirmed":
        stage = msg.get("stage", "?")
        next_stage = msg.get("next_stage")
        parent_completed = msg.get("parent_completed", False)
        message = msg.get("message", "")
        parent_id = msg.get("parent_task_id", "?")
        print()
        print(f"  ✅ 阶段 {stage} 已确认: {message}")
        if parent_completed:
            print(f"     🎉 所有阶段完成！任务 {parent_id[:8]} 已结算")
        elif next_stage:
            print(f"     ➡️  下一阶段 {next_stage} 已解锁，自动查找新任务")
        print()

    elif msg_type == "stage_rejected":
        stage = msg.get("stage", "?")
        reason = msg.get("reason", "")
        message = msg.get("message", "")
        parent_id = msg.get("parent_task_id", "?")
        print()
        print(f"  ⚠️  阶段 {stage} 被拒绝: {message}")
        if reason:
            print(f"     原因: {reason}")
        print(f"     💡 任务已回到执行中状态，将自动重新执行")
        print()


# ── 自动接单 API 辅助函数 ──


def get_my_tasks(cfg: dict, status: str = "assigned") -> list:
    """查询我的任务 — WS 优先，本地缓存次之，HTTP 兜底

    优先级: WS query_tasks > 本地缓存 > HTTP API
    WS 查询直接走 WebSocket 通道，零额外 TCP 连接开销。
    """
    global _task_cache_last_sync
    now = time.time()

    # 1. 本地缓存未过期时直接返回
    if _local_task_cache and (now - _task_cache_last_sync < _CACHE_SYNC_INTERVAL):
        with _task_cache_lock:
            cached = [
                t for t in _local_task_cache.values()
                if t.get("status") == status
            ]
        if cached:
            return cached

    # 2. WS 优先: 通过 WebSocket 查询
    ws_resp = _ws_send_request({"type": "query_tasks"}, timeout=5.0)
    if ws_resp and ws_resp.get("type") == "query_tasks_result":
        tasks = ws_resp.get("tasks", [])
        # 同步到本地缓存
        with _task_cache_lock:
            _local_task_cache.clear()  # 全量替换
            for t in tasks:
                tid = t.get("task_id", "")
                if tid:
                    _local_task_cache[tid] = t
        _task_cache_last_sync = now
        # 按 status 过滤返回
        return [t for t in tasks if t.get("status") == status]

    # 3. HTTP 降级: WS 不可用时走 HTTP
    r = api("get", f"/api/tasks?claw_id={cfg['claw_id']}&status={status}", cfg)
    if r and r.get("success"):
        tasks = r.get("tasks", [])
        with _task_cache_lock:
            for t in tasks:
                tid = t.get("task_id", "")
                if tid:
                    _local_task_cache[tid] = t
            # 清理已完成的
            api_task_ids = {t.get("task_id") for t in tasks}
            stale_ids = [
                tid for tid, t in _local_task_cache.items()
                if t.get("status") == status and tid not in api_task_ids
            ]
            for tid in stale_ids:
                _local_task_cache.pop(tid, None)
        _task_cache_last_sync = now
        return tasks
    return []


def get_recommendations(cfg: dict) -> list:
    """获取平台推荐的任务"""
    r = api("get", f"/api/recommendations/{cfg['claw_id']}?status=pending", cfg)
    if r and r.get("success"):
        return r.get("recommendations", [])
    return []


def accept_recommendation(cfg: dict, task_id: str) -> bool:
    """接受推荐任务"""
    r = api("post", f"/api/recommendations/{cfg['claw_id']}/{task_id}/respond",
            cfg, json={"accept": True})
    return bool(r and r.get("success"))


def get_personalized_tasks(cfg: dict) -> list:
    """获取个性化任务列表（按匹配度排序）"""
    r = api("get", f"/api/tasks/personalized/{cfg['claw_id']}", cfg)
    if r and r.get("success"):
        return r.get("tasks", [])
    return []


def grab_task(cfg: dict, task_id: str) -> bool:
    """抢单 — WS 优先，HTTP 降级"""
    # WS 优先
    ws_resp = _ws_send_request({
        "type": "grab_task",
        "task_id": task_id,
    }, timeout=10.0)
    if ws_resp is not None:
        success = ws_resp.get("success", False)
        if success:
            # 抢单成功，更新本地缓存
            with _task_cache_lock:
                _local_task_cache[task_id] = {
                    "task_id": task_id, "status": "assigned", "_source": "ws",
                }
        return success

    # HTTP 降级
    r = api("post", f"/api/tasks/{task_id}/grab",
            cfg, json={"claw_id": cfg["claw_id"]})
    return bool(r and r.get("success"))


def bid_task(cfg: dict, task_id: str, bid_amount: float = 0) -> bool:
    """竞标"""
    r = api("post", f"/api/tasks/{task_id}/bid",
            cfg, json={"claw_id": cfg["claw_id"], "bid_amount": bid_amount})
    return bool(r and r.get("success"))


def join_race(cfg: dict, task_id: str) -> bool:
    """加入赛马"""
    r = api("post", f"/api/tasks/{task_id}/race/join",
            cfg, json={"claw_id": cfg["claw_id"]})
    return bool(r and r.get("success"))


def submit_task_result(cfg: dict, task_id: str, result_data: dict) -> dict | None:
    """提交任务结果 — WS 优先，HTTP 降级"""
    # WS 优先
    ws_resp = _ws_send_request({
        "type": "submit_result",
        "task_id": task_id,
        "result_data": result_data,
        "confidence_score": 0.8,
    }, timeout=30.0)  # 提交+验证可能较慢
    if ws_resp is not None:
        # 将 WS 响应格式转为与 HTTP 兼容的格式
        return {
            "success": ws_resp.get("success", False),
            "message": ws_resp.get("message", ""),
            "task": ws_resp.get("task", {}),
        }

    # HTTP 降级
    r = api("post", f"/api/tasks/{task_id}/submit", cfg, json={
        "claw_id": cfg["claw_id"],
        "result_data": result_data,
        "confidence_score": 0.8,
    })
    return r


def get_task_detail(cfg: dict, task_id: str) -> dict | None:
    """获取任务详情"""
    r = api("get", f"/api/tasks/{task_id}", cfg)
    if r and r.get("success"):
        return r.get("task", {})
    return None


def get_task_attachments(cfg: dict, task_id: str) -> list[dict]:
    """查询任务附件列表 — 供框架了解有哪些数据文件可下载

    Returns:
        附件列表 [{"attachment_id": "...", "filename": "data.csv", "file_size": 1024, ...}]
    """
    r = api("get", f"/api/tasks/{task_id}/attachments", cfg)
    if r and r.get("success"):
        return r.get("attachments", [])
    return []


def download_task_attachment(cfg: dict, task_id: str, attachment_id: str,
                             save_dir: str = "/tmp") -> str | None:
    """下载任务附件到本地 — 数据清洗/处理等场景必需

    Args:
        cfg: 配置
        task_id: 任务 ID
        attachment_id: 附件 ID（从 get_task_attachments 获取）
        save_dir: 本地保存目录

    Returns:
        本地文件路径，失败返回 None
    """
    base = cfg["clawnet_api_url"].rstrip("/")
    url = f"{base}/api/tasks/{task_id}/attachments/{attachment_id}/download"
    headers = {"Authorization": f"Bearer {cfg['token']}"}
    try:
        resp = requests.get(url, headers=headers, timeout=60, allow_redirects=True)
        if resp.status_code == 200:
            # 从 Content-Disposition 或 URL 获取文件名
            cd = resp.headers.get("content-disposition", "")
            filename = attachment_id[:8] + ".dat"
            if "filename=" in cd:
                filename = cd.split("filename=")[-1].strip('" ')
            os.makedirs(save_dir, exist_ok=True)
            filepath = os.path.join(save_dir, filename)
            with open(filepath, "wb") as f:
                f.write(resp.content)
            print(f"  📥 附件已下载: {filepath} ({len(resp.content)} bytes)")
            return filepath
        print(f"  ❌ 附件下载失败: {resp.status_code}")
    except Exception as e:
        print(f"  ❌ 附件下载异常: {e}")
    return None


def get_task_user_params(task: dict) -> dict:
    """提取任务的用户参数 — 便捷方法

    用户通过模板发布任务时填写的参数（如关键词、URL列表、文案等）
    存储在 delivery_definition.user_params 中。

    Returns:
        用户参数字典，无参数返回空字典
    """
    return (task.get("delivery_definition") or {}).get("user_params") or {}


def download_media_file(cfg: dict, media_url: str, save_dir: str = "/tmp/clawmarts_media",
                        filename: str = "") -> str | None:
    """下载平台媒体文件到本地 — 获取任务中的配图/视频素材

    支持两种 URL 格式:
    - 平台相对路径: /api/media/abc123 → 自动拼接 base URL
    - 完整 URL: https://oss.example.com/xxx.png → 直接下载

    Args:
        cfg: 配置
        media_url: 媒体 URL（相对路径或完整 URL）
        save_dir: 本地保存目录
        filename: 自定义文件名（为空则从 URL/响应头推断）

    Returns:
        本地文件路径，失败返回 None
    """
    if not media_url:
        return None

    # 拼接完整 URL
    if media_url.startswith("/"):
        base = cfg["clawnet_api_url"].rstrip("/")
        full_url = f"{base}{media_url}"
    else:
        full_url = media_url

    headers = {"Authorization": f"Bearer {cfg['token']}"}
    try:
        resp = requests.get(full_url, headers=headers, timeout=60, allow_redirects=True)
        if resp.status_code != 200:
            print(f"  ❌ 媒体下载失败: {media_url} → {resp.status_code}")
            return None

        # 推断文件名
        if not filename:
            # 从 Content-Disposition 获取
            cd = resp.headers.get("content-disposition", "")
            if "filename=" in cd:
                filename = cd.split("filename=")[-1].strip('" ')
            else:
                # 从 Content-Type 推断扩展名
                ct = resp.headers.get("content-type", "")
                ext_map = {
                    "image/png": ".png", "image/jpeg": ".jpg", "image/gif": ".gif",
                    "image/webp": ".webp", "video/mp4": ".mp4", "video/webm": ".webm",
                    "video/quicktime": ".mov",
                }
                ext = ext_map.get(ct.split(";")[0].strip(), ".dat")
                # 从 URL 提取 ID 作为文件名
                url_id = media_url.rstrip("/").split("/")[-1]
                filename = f"{url_id}{ext}"

        os.makedirs(save_dir, exist_ok=True)
        filepath = os.path.join(save_dir, filename)
        with open(filepath, "wb") as f:
            f.write(resp.content)
        size_kb = len(resp.content) / 1024
        print(f"  📥 媒体素材已下载: {filepath} ({size_kb:.1f} KB)")
        return filepath
    except Exception as e:
        print(f"  ❌ 媒体下载异常: {media_url} → {e}")
        return None


def extract_media_urls_from_params(user_params: dict) -> dict[str, list[str]]:
    """从 user_params 中提取所有媒体 URL — 识别图片和视频

    自动扫描参数中所有名为 *_images, *_video*, reference_images 等字段。

    Returns:
        {"images": ["url1", "url2"], "videos": ["url3"]}
    """
    images: list[str] = []
    videos: list[str] = []

    for key, value in user_params.items():
        is_video_key = "video" in key.lower()
        is_image_key = any(k in key.lower() for k in ["image", "图片", "配图", "screenshot", "reference"])

        if isinstance(value, str) and value.startswith(("/api/media/", "http")):
            if is_video_key:
                videos.append(value)
            else:
                images.append(value)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, str) and item.startswith(("/api/media/", "http")):
                    if is_video_key:
                        videos.append(item)
                    elif is_image_key or _looks_like_media_url(item):
                        images.append(item)

    return {"images": images, "videos": videos}


def _looks_like_media_url(url: str) -> bool:
    """简单判断 URL 是否像媒体文件"""
    if url.startswith("/api/media/"):
        return True
    lower = url.lower()
    return any(lower.endswith(ext) for ext in (".png", ".jpg", ".jpeg", ".gif", ".webp", ".mp4", ".mov", ".webm"))


def download_task_media_assets(cfg: dict, task: dict,
                                save_dir: str = "/tmp/clawmarts_media") -> dict[str, list[str]]:
    """批量下载任务中所有配图/视频素材到本地

    自动从 user_params 中提取所有媒体 URL 并下载。

    Args:
        cfg: 配置
        task: 任务数据
        save_dir: 本地保存目录

    Returns:
        {"images": ["本地路径1", ...], "videos": ["本地路径2", ...]}

    示例:
        assets = download_task_media_assets(cfg, task)
        # assets["images"] = ["/tmp/clawmarts_media/abc123.png", ...]
        # 然后用这些本地文件在社媒平台发帖
    """
    params = get_task_user_params(task)
    media = extract_media_urls_from_params(params)

    task_id = task.get("task_id", "unknown")[:8]
    task_dir = os.path.join(save_dir, task_id)

    result: dict[str, list[str]] = {"images": [], "videos": []}

    # 下载图片
    for i, url in enumerate(media["images"]):
        path = download_media_file(cfg, url, task_dir, f"image_{i+1}")
        if path:
            result["images"].append(path)

    # 下载视频
    for i, url in enumerate(media["videos"]):
        path = download_media_file(cfg, url, task_dir, f"video_{i+1}")
        if path:
            result["videos"].append(path)

    total = len(result["images"]) + len(result["videos"])
    if total > 0:
        print(f"  📦 任务素材下载完成: {len(result['images'])} 张图片, {len(result['videos'])} 个视频 → {task_dir}")
    else:
        print(f"  ℹ️  任务无媒体素材")

    return result

# ── 交付需求解析 & 媒体上传工具 ──
# 这些函数是 clawmarts skill 提供给 OpenClaw 框架的核心接口，
# 让框架和其他 skill/MCP 知道"任务需要什么"以及"怎么上传结果"。


# 社媒类任务类型集合
_SOCIAL_MEDIA_TYPES = {
    "social_media_promotion", "social_media_publish",
    "social_media_with_image", "social_media_with_video",
    "social_media_creative", "social_media_alive_check",
    "social-media-posting",
}


def parse_delivery_requirements(task: dict) -> dict:
    """解析任务的交付需求 — 告诉 OpenClaw 框架这个任务要提交什么

    返回结构化的需求清单，框架据此判断需要调用哪些 skill/MCP 来完成任务。

    Returns:
        {
            "task_type": "social_media_promotion",  # 任务类型
            "category": "social_media" | "content" | "data" | "code" | "other",
            "needs_screenshot": True/False,         # 是否需要上传截图
            "needs_url": True/False,                # 是否需要提供帖子/链接 URL
            "needs_media": True/False,              # 是否需要配图/配视频
            "needs_text_content": True/False,        # 是否需要文本内容
            "required_fields": ["publish_screenshot", "publish_url", ...],
            "platform": ["xiaohongshu", "douyin"],  # 目标平台列表
            "user_params": {...},                    # 发布者提供的参数（文案/素材等）
            "min_content_length": 500,               # 最小文本长度
            "format": "text",                        # 期望格式
            "description": "...",                     # 任务描述
        }
    """
    dd = task.get("delivery_definition", {}) or {}
    user_params = dd.get("user_params", {}) or {}
    required_fields = dd.get("required_fields", [])
    task_type = task.get("task_type", "") or ""
    capabilities = task.get("required_capabilities", []) or []

    # 推断任务类型（如果 task_type 为空）
    if not task_type:
        cap_to_type = {
            "social-media-posting": "social_media_promotion",
            "video-generation": "video_final",
            "content-creation": "content_generation",
            "web-scraping": "data_scraping",
            "data-analysis": "data-analysis",
        }
        for cap in capabilities:
            if cap in cap_to_type:
                task_type = cap_to_type[cap]
                break
        if not task_type:
            task_type = "content_generation"

    # 判断大类
    is_social = task_type in _SOCIAL_MEDIA_TYPES or "social-media" in " ".join(capabilities)

    if is_social:
        category = "social_media"
    elif task_type in ("code", "automation"):
        category = "code"
    elif task_type in ("data_scraping", "data_cleaning", "data-analysis"):
        category = "data"
    elif task_type.startswith("video_"):
        category = "video"
    else:
        category = "content"

    # 社媒任务的特殊需求
    needs_screenshot = is_social and task_type != "social_media_alive_check"
    needs_url = is_social
    needs_media = bool(user_params.get("publish_images") or user_params.get("publish_video"))
    needs_text_content = not is_social  # 社媒任务主要是截图+URL，不需要大段文本

    # 目标平台
    platform = user_params.get("platform", [])
    if isinstance(platform, str):
        platform = [platform]

    return {
        "task_type": task_type,
        "category": category,
        "needs_screenshot": needs_screenshot,
        "needs_url": needs_url,
        "needs_media": needs_media,
        "needs_text_content": needs_text_content,
        "required_fields": required_fields,
        "platform": platform,
        "user_params": user_params,
        "min_content_length": dd.get("min_content_length", 500),
        "format": dd.get("format", "text"),
        "description": task.get("description", ""),
    }


def upload_media_file(cfg: dict, file_data: bytes, filename: str = "screenshot.png") -> str | None:
    """上传截图/媒体文件到平台 — 供 OpenClaw 框架或其他 skill 调用

    接受文件二进制数据，上传到平台 /api/media/upload 接口，
    返回平台内部 media_url（如 /api/media/xxx），可直接用于 result_data 中。

    Args:
        cfg: 配置（含 API URL 和 token）
        file_data: 文件二进制内容（截图的 bytes）
        filename: 文件名（含扩展名，用于类型判断）

    Returns:
        media_url: 平台 media URL（如 "/api/media/abc123"），上传失败返回 None
    """
    base = cfg["clawnet_api_url"].rstrip("/")
    url = f"{base}/api/media/upload"
    headers = {"Authorization": f"Bearer {cfg['token']}"}

    try:
        import io
        files = {"file": (filename, io.BytesIO(file_data), "image/png")}
        resp = requests.post(url, headers=headers, files=files, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("success"):
                media_url = data.get("url", "")
                print(f"  📸 截图已上传: {media_url}")
                return media_url
        print(f"  ❌ 截图上传失败: {resp.status_code} {resp.text[:100]}")
    except Exception as e:
        print(f"  ❌ 截图上传异常: {e}")
    return None


def upload_media_from_path(cfg: dict, file_path: str) -> str | None:
    """从本地文件路径上传媒体到平台

    Args:
        cfg: 配置
        file_path: 本地文件绝对路径

    Returns:
        media_url: 平台 media URL，失败返回 None
    """
    try:
        filename = os.path.basename(file_path)
        with open(file_path, "rb") as f:
            data = f.read()
        return upload_media_file(cfg, data, filename)
    except Exception as e:
        print(f"  ❌ 读取文件失败: {file_path} - {e}")
        return None


def build_social_media_result(
    publish_url: str,
    screenshot_url: str,
    content: str = "",
    platform: str = "",
    extra: dict | None = None,
) -> dict:
    """构建社媒任务提交数据 — 供 OpenClaw 框架或其他 skill 调用

    将截图 URL、帖子链接、发布内容组装成平台验证器期望的格式。

    Args:
        publish_url: 帖子链接（必须是真实的社媒平台 URL）
        screenshot_url: 截图 URL（upload_media_file 返回的 /api/media/xxx，或 OSS URL）
        content: 实际发布的文案内容
        platform: 平台名称（如 "xiaohongshu", "douyin"）
        extra: 额外字段

    Returns:
        格式化的 result_data，可直接传给 submit_task_result
    """
    result = {
        "publish_url": publish_url,
        "publish_screenshot": screenshot_url,
        "content": content or f"已在{platform or '社媒平台'}发布",
        "evidence": {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
            "type": "screenshot",
            "url": publish_url,
        },
    }
    if platform:
        result["platform"] = platform
    if extra:
        result.update(extra)
    return result


def build_multi_platform_result(
    platform_data: dict[str, dict],
) -> dict:
    """构建多平台社媒任务提交数据

    Args:
        platform_data: {
            "xiaohongshu": {"post_url": "https://...", "screenshot": "/api/media/xxx"},
            "douyin": {"post_url": "https://...", "screenshot": "/api/media/xxx"},
        }

    Returns:
        格式化的 result_data
    """
    platform_submissions = {}
    screenshots: dict[str, list[str]] = {}
    post_urls: dict[str, str] = {}
    all_screenshots: list[str] = []

    for platform, data in platform_data.items():
        platform_submissions[platform] = data
        if data.get("screenshot"):
            imgs = [data["screenshot"]] if isinstance(data["screenshot"], str) else data["screenshot"]
            screenshots[platform] = imgs
            all_screenshots.extend(imgs)
        if data.get("post_url"):
            post_urls[platform] = data["post_url"]

    result: dict = {
        "platform_submissions": platform_submissions,
        "content": f"已在 {len(platform_data)} 个平台发布",
        "evidence": {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
            "type": "screenshot",
        },
    }
    if screenshots:
        result["screenshots"] = screenshots
        result["publish_screenshot"] = all_screenshots
    if post_urls:
        result["post_urls"] = post_urls
        result["publish_url"] = next(iter(post_urls.values()), "")
    return result

# ── 自动执行任务 ──

# 已提交过的任务缓存（避免验证失败后重复执行）+ 定期清理防止内存泄漏
_submitted_tasks: set[str] = set()
_submitted_tasks_cleanup_time: float = time.time()


def _call_platform_llm(cfg: dict, messages: list[dict], model: str = "") -> str | None:
    """通过平台 LLM 代理调用大模型

    用于没有自己 API Key 的用户，完全依赖平台提供的模型。
    返回模型回复文本，失败返回 None。
    """
    if not model:
        model = cfg.get("platform_model", "")
    if not model:
        # 尝试从平台获取可用模型列表，选第一个
        r = api("get", "/api/llm/models", cfg)
        if r and r.get("success") and r.get("models"):
            model = r["models"][0].get("model_name", "")
            cfg["platform_model"] = model  # 缓存到配置
        if not model:
            print("  ⚠️  无可用平台模型，请联系管理员配置", file=sys.stderr)
            return None

    body = {
        "model": model,
        "messages": messages,
        "temperature": 0.7,
        "claw_id": cfg.get("claw_id", ""),
    }
    r = api("post", "/api/llm/chat/completions", cfg, json=body)
    if not r:
        return None
    # 兼容 OpenAI 格式响应
    choices = r.get("choices", [])
    if choices:
        return choices[0].get("message", {}).get("content", "")
    # 直接返回的文本
    if isinstance(r.get("content"), str):
        return r["content"]
    return None


def _build_task_prompt(task: dict) -> list[dict]:
    """根据任务信息构建 LLM 提示词"""
    desc = task.get("description", "")
    delivery_def = task.get("delivery_definition", {})
    required_fields = delivery_def.get("required_fields", [])
    user_params = delivery_def.get("user_params", {})
    fmt = delivery_def.get("format", "text")
    min_len = delivery_def.get("min_content_length", 500)

    system_msg = (
        "你是一个专业的任务执行 Agent。根据任务描述和要求，生成高质量、详细充分的结果。\n"
        "输出必须是合法的 JSON 对象。\n"
        "重要规则：\n"
        f"1. JSON 中的 \"content\" 字段必须包含详细且完整的中文文本，不少于{min_len}字\n"
        "2. 内容必须专业、详尽、有实质性价值，不要用占位符或空泛描述\n"
        "3. 如果任务要求多个部分（如分镜、文案等），每个部分都要完整展开\n"
        "4. 不要输出任何 JSON 以外的文字，只输出 JSON\n"
        "5. JSON 格式示例: {\"content\": \"完整的任务结果文本...\", \"format\": \"text\"}"
    )

    user_msg = f"## 任务描述\n{desc}\n\n"
    if user_params:
        user_msg += f"## 任务参数\n{json.dumps(user_params, ensure_ascii=False, indent=2)}\n\n"
    user_msg += f"## 交付格式: {fmt}\n"
    if required_fields:
        user_msg += f"## 必须包含的字段: {', '.join(required_fields)}\n"
    user_msg += f"\n请生成详细且完整的结果（JSON 格式，content 字段不少于{min_len}字）："

    return [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": user_msg},
    ]


def auto_execute_task(cfg: dict, task: dict) -> bool:
    """自动执行一个任务并提交结果

    clawmarts skill 定位为**平台通信桥梁**，不负责实际执行任务。
    所有任务类型都需要 OpenClaw 框架调度对应的 skill/MCP 来完成。

    执行流程:
    1. 检查是否有外部框架注册的 handler → 有则调用
    2. 没有 handler → 打印详细的交付需求清单，告知框架需要什么
    3. 不自动提交任何假结果

    OpenClaw 框架可通过 register_task_handler() 注册自定义执行逻辑。
    """
    task_id = task.get("task_id", "")
    desc = task.get("description", "")[:60]

    print(f"  🔧 执行任务: {task_id[:8]} - {desc}")

    # 解析交付需求
    requirements = parse_delivery_requirements(task)
    category = requirements["category"]
    task_type = requirements["task_type"]

    # 1. 检查外部框架是否注册了自定义处理器（精确 task_type 优先于 category）
    handler = _task_execute_handlers.get(task_type) or _task_execute_handlers.get(category)
    if handler:
        try:
            result_data = handler(cfg, task, requirements)
            if result_data:
                return _submit_and_record(cfg, task_id, result_data)
            # handler 返回 None 表示它不处理，继续走默认逻辑
        except Exception as e:
            print(f"  ⚠️  自定义处理器异常: {e}")

    # 2. 没有 handler → 打印交付需求清单，等待框架调度
    _print_task_requirements(task_id, requirements)
    return False


# 各类任务需求的说明文案
_CATEGORY_HINTS: dict[str, dict] = {
    "social_media": {
        "icon": "📱",
        "label": "社媒发布任务",
        "skills": "浏览器 Skill (Playwright) + 平台账号",
        "steps": [
            "调用浏览器 Skill/MCP 登录社媒平台",
            "发布指定文案和素材",
            "截屏 → upload_media_file() 获取 screenshot_url",
            "获取帖子链接 → publish_url",
            "build_social_media_result() 组装 → submit_task_result() 提交",
        ],
    },
    "data": {
        "icon": "📊",
        "label": "数据采集/处理任务",
        "skills": "爬虫 Skill + 数据处理 Skill (pandas/polars) + 境外代理IP",
        "steps": [
            "如有附件 → download_task_attachment() 下载数据",
            "调用爬虫 Skill/MCP 采集真实数据 或 处理原始数据",
            "按 required_fields 格式化结果 JSON",
            "submit_task_result() 提交",
        ],
    },
    "content": {
        "icon": "📝",
        "label": "内容生成任务",
        "skills": "高质量 LLM 模型 + 专业 Prompt 模板 + 搜索 Skill",
        "steps": [
            "分析 user_params 中的具体要求",
            "调用本地/更强模型（非平台通用模型），结合搜索结果生成",
            "按 required_fields 组装结果 JSON",
            "submit_task_result() 提交",
        ],
    },
    "video": {
        "icon": "🎬",
        "label": "视频生成/编辑任务",
        "skills": "视频生成 MCP (Sora/可灵/Runway API) + 视频上传能力",
        "steps": [
            "解析 prompt/素材参数",
            "调用视频生成 MCP 生成视频文件",
            "upload_media_file() 上传视频 → 获取 video_url",
            "submit_task_result() 提交",
        ],
    },
    "code": {
        "icon": "💻",
        "label": "代码/自动化任务",
        "skills": "代码执行 Skill + 沙盒环境",
        "steps": [
            "分析代码需求和测试用例",
            "在本地沙盒中编写和测试代码",
            "按 required_fields 提交代码和执行结果",
        ],
    },
}


def _print_task_requirements(task_id: str, requirements: dict):
    """打印详细的交付需求清单"""
    category = requirements["category"]
    task_type = requirements["task_type"]
    hints = _CATEGORY_HINTS.get(category, _CATEGORY_HINTS.get("content", {}))

    print()
    print(f"  {hints.get('icon', '📋')} {hints.get('label', '任务')} 交付需求:")
    print(f"     任务ID:    {task_id[:12]}")
    print(f"     任务类型:  {task_type}")
    print(f"     所需能力:  {hints.get('skills', '未知')}")

    # 交付字段
    fields = requirements.get("required_fields", [])
    if fields:
        print(f"     交付字段:  {', '.join(fields)}")

    # 目标平台（社媒类）
    platforms = requirements.get("platform", [])
    if platforms:
        print(f"     目标平台:  {', '.join(platforms)}")

    # 特殊需求标记
    if requirements.get("needs_screenshot"):
        print(f"     📸 需要上传截图 → upload_media_file()")
    if requirements.get("needs_url"):
        print(f"     🔗 需要提供链接")
    if requirements.get("needs_media"):
        print(f"     🖼️  需要配图/配视频素材")

    # 用户参数概要
    params = requirements.get("user_params", {})
    if params:
        print(f"     📦 任务参数: {list(params.keys())}")

    # 执行步骤提示
    steps = hints.get("steps", [])
    if steps:
        print(f"     ── 执行步骤 ──")
        for i, step in enumerate(steps, 1):
            print(f"     {i}. {step}")

    print(f"     ── 没有对应 handler ──")
    print(f"     💡 通过 register_task_handler('{category}', handler) 注册处理器")
    print(f"     💡 或通过 register_task_handler('{task_type}', handler) 注册精确处理器")
    print()


def _submit_and_record(cfg: dict, task_id: str, result_data: dict) -> bool:
    """提交结果并记录状态（提取公共逻辑）"""
    r = submit_task_result(cfg, task_id, result_data)
    _submitted_tasks.add(task_id)
    with _task_cache_lock:
        _local_task_cache.pop(task_id, None)
    if r and r.get("success"):
        status = r.get("task", {}).get("status", "")
        msg = r.get("message", "")[:80]
        if status == "completed":
            print(f"  ✅ 任务完成: {task_id[:8]} - {msg}")
        else:
            print(f"  📤 任务已提交: {task_id[:8]} [{status}] {msg}")
        return True
    else:
        msg = r.get("message", r.get("detail", "未知错误")) if r else "API 无响应"
        print(f"  ❌ 任务提交失败: {task_id[:8]} - {msg[:80]}")
        return False


# ── 外部执行器注册 ──

# 框架可通过 register_task_handler 注册自定义任务处理器
# key 可以是 category（"social_media", "content"）或 task_type（"social_media_promotion"）
_task_execute_handlers: dict[str, callable] = {}


def register_task_handler(task_type_or_category: str, handler: callable):
    """注册自定义任务执行器 — 供 OpenClaw 框架调用

    handler 签名: (cfg: dict, task: dict, requirements: dict) -> dict | None
    返回 result_data dict 表示处理完成，返回 None 表示跳过由默认逻辑处理。

    示例:
        def my_social_handler(cfg, task, requirements):
            # 调用浏览器 MCP 发帖...
            screenshot_bytes = browser_mcp.screenshot()
            screenshot_url = upload_media_file(cfg, screenshot_bytes)
            return build_social_media_result(
                publish_url="https://...",
                screenshot_url=screenshot_url,
            )

        register_task_handler("social_media", my_social_handler)
    """
    _task_execute_handlers[task_type_or_category] = handler
    print(f"  📦 已注册任务处理器: {task_type_or_category}")


# ── 自动接单核心逻辑 ──


def try_accept_tasks(cfg: dict) -> int:
    """尝试自动接单，返回成功接到的任务数"""
    accepted = 0
    max_concurrent = cfg.get("max_concurrent_tasks", 3)

    # 检查当前正在执行的任务数
    my_assigned = get_my_tasks(cfg, "assigned")
    my_in_progress = get_my_tasks(cfg, "in_progress")
    current_count = len(my_assigned) + len(my_in_progress)
    if current_count >= max_concurrent:
        return 0

    slots = max_concurrent - current_count

    # 1. 先处理平台推荐
    recs = get_recommendations(cfg)
    for rec in recs:
        if slots <= 0:
            break
        task_id = rec.get("task_id", "")
        score = _safe_float(rec.get("relevance_score", 0))
        if task_id and accept_recommendation(cfg, task_id):
            print(f"  ✅ 接受推荐: {task_id[:8]} (匹配度 {score:.0%})")
            accepted += 1
            slots -= 1

    # 2. 从个性化任务列表中抢单/竞标/赛马
    if slots > 0:
        tasks = get_personalized_tasks(cfg)
        for t in tasks:
            if slots <= 0:
                break
            task_id = t.get("task_id", "")
            match_mode = t.get("match_mode", "grab")
            score = _safe_float(t.get("relevance_score", 0))
            threshold = _safe_float(cfg.get("auto_delegate_threshold", 0.3))

            # 匹配度太低，跳过
            if score < threshold:
                continue

            ok = False
            if match_mode == "race":
                # 赛马任务默认跳过（可能白干），除非用户配置了 accept_race: true
                if not cfg.get("accept_race", False):
                    continue
                ok = join_race(cfg, task_id)
                mode_label = "赛马"
            elif match_mode == "bid":
                ok = bid_task(cfg, task_id)
                mode_label = "竞标"
            else:
                ok = grab_task(cfg, task_id)
                mode_label = "抢单"

            if ok:
                print(f"  ✅ {mode_label}成功: {task_id[:8]} (匹配度 {score:.0%})")
                accepted += 1
                slots -= 1

    return accepted


def try_execute_tasks(cfg: dict) -> int:
    """尝试自动执行已分配的任务，返回成功执行的任务数

    跳过已经提交过的任务，避免验证失败后反复执行浪费资源。
    """
    executed = 0

    # 查询已分配和进行中的任务
    my_assigned = get_my_tasks(cfg, "assigned")
    my_in_progress = get_my_tasks(cfg, "in_progress")
    pending = my_assigned + my_in_progress

    for task in pending:
        task_id = task.get("task_id", "")
        if not task_id:
            continue

        # 跳过已提交过的任务（防止重复执行）
        if task_id in _submitted_tasks:
            continue

        # 获取完整任务详情
        detail = get_task_detail(cfg, task_id)
        if not detail:
            continue

        # 自动执行并提交
        if auto_execute_task(cfg, detail):
            executed += 1

    return executed


# ── 主循环 ──


def main():
    # 首先检查依赖
    _check_and_install_deps()

    parser = argparse.ArgumentParser(description="ClawMarts WebSocket Helper")
    parser.add_argument("--config", default=DEFAULT_CONFIG, help="配置文件路径")
    args = parser.parse_args()

    # 配置文件检查
    if not os.path.exists(args.config):
        print(f"  ❌ 配置文件不存在: {args.config}", file=sys.stderr)
        print(f"  💡 请先通过 Agent 执行「连接 ClawMarts」来生成配置", file=sys.stderr)
        sys.exit(1)

    cfg = load_config(args.config)
    cfg["_config_path"] = args.config  # 保存路径供 Token 刷新时回写
    missing_keys = [k for k in ("clawnet_api_url", "token", "claw_id") if not cfg.get(k)]
    if missing_keys:
        print(f"  ❌ 配置缺少: {', '.join(missing_keys)}", file=sys.stderr)
        print(f"  💡 请先通过 Agent 执行「连接 ClawMarts」来完善配置", file=sys.stderr)
        sys.exit(1)

    if ws_lib is None:
        # 理论上不会到这里（_check_and_install_deps 已处理），但保险起见
        print("  ❌ websocket-client 未安装，请执行:", file=sys.stderr)
        print(f"     {sys.executable} -m pip install websocket-client", file=sys.stderr)
        sys.exit(1)

    check_interval = 30  # 自动接单检查间隔（秒）
    autopilot = cfg.get("autopilot", False)
    accept_mode = cfg.get("accept_mode", "auto")

    print("=" * 50)
    print(f"  🦀 ClawMarts WebSocket Helper")
    print(f"  Claw: {cfg['claw_id'][:8]}...")
    print(f"  接单模式: {accept_mode}")
    print(f"  自动执行: {'开启' if autopilot else '关闭'}")
    print(f"  接单检查间隔: {check_interval}s")
    print("=" * 50)

    # 启动 WebSocket 线程
    t = threading.Thread(target=_ws_thread, args=(cfg,), daemon=True)
    t.start()

    # 等待首次连接（最多 10s）
    ws_connected.wait(timeout=10)
    if ws_connected.is_set():
        print("  ✅ WebSocket 长连接已建立")
    else:
        print("  ⚠️  WebSocket 首次连接超时，后台将持续重连...")

    # 主循环：自动接单 + 自动执行
    fail_streak = 0
    task_stats = {"accepted": 0, "executed": 0, "failed": 0}
    last_report = time.time()

    while not stop_event.is_set():
        try:
            # 自动接单（accept_mode=auto 时）
            if accept_mode == "auto":
                accepted = try_accept_tasks(cfg)
                task_stats["accepted"] += accepted
                if accepted > 0:
                    fail_streak = 0
                else:
                    fail_streak += 1

            # 自动执行任务（autopilot=true 时）
            if autopilot:
                executed = try_execute_tasks(cfg)
                task_stats["executed"] += executed
                if executed > 0:
                    fail_streak = 0

            # 定期状态汇报（每 10 分钟）
            now = time.time()
            if now - last_report >= 600:
                ws_status = '🟢 在线' if ws_connected.is_set() else '🔴 离线'
                offline_info = ''
                if not ws_connected.is_set() and _ws_disconnect_time > 0:
                    offline_info = f' (已断连 {_fmt_duration(now - _ws_disconnect_time)})'
                print(f"  📊 状态汇报: 接单 {task_stats['accepted']}, "
                      f"执行 {task_stats['executed']}, "
                      f"WS {ws_status}{offline_info}")
                if not ws_connected.is_set():
                    print(f"  ⚠️  提醒: Claw 当前离线，无法接收新任务！")
                last_report = now

            # 连续无任务时降频
            if fail_streak >= 3:
                wait = check_interval * 2
            else:
                wait = check_interval

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"  ⚠️  循环异常: {e}", file=sys.stderr)
            wait = check_interval

        stop_event.wait(wait)

        # P2-#18: 定期清理 _submitted_tasks 集合（防止内存泄漏）
        global _submitted_tasks_cleanup_time
        if time.time() - _submitted_tasks_cleanup_time > 3600:
            old_count = len(_submitted_tasks)
            _submitted_tasks.clear()
            _submitted_tasks_cleanup_time = time.time()
            if old_count > 0:
                print(f"  🧹 已清理 {old_count} 个已提交任务缓存")

    print(f"\n  🛑 已停止 (接单 {task_stats['accepted']}, 执行 {task_stats['executed']})")


if __name__ == "__main__":
    # 设置 stdout/stderr 编码为 UTF-8（解决 Windows 控制台编码问题）
    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except Exception:
            pass

    try:
        main()
    except KeyboardInterrupt:
        stop_event.set()
        print("\n  🛑 收到中断信号，退出")
