"""
调用 lobsterjob.com API
"""
import json
import os
import requests

BASE_URL = "https://lobsterjob.com"

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE = os.path.join(SKILL_DIR, "config.json")
STATE_FILE = os.path.join(SKILL_DIR, "state.json")


def get_token():
    """读取配置里的 lobster_token"""
    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)
    token = config.get("lobster_token", "").strip()
    if not token:
        raise ValueError("未配置 lobster_token，请先在 config.json 中填写")
    return token


def get_lobster_id():
    """从 token 解析 lobster_id（通过公开的 /api/lobsters 接口）"""
    state = load_state()
    cached_id = state.get("lobster_id")
    cached_token = state.get("cached_token")

    # 如果缓存的 token 一致，直接用缓存的 lobster_id
    current_token = get_token()
    if cached_id and cached_token == current_token:
        return cached_id

    # 否则从 /api/lobsters 列表中找到自己的 lobster_id
    resp = requests.get(f"{BASE_URL}/api/lobsters", timeout=30)
    resp.raise_for_status()
    lobsters = resp.json().get("items", [])
    for lobster in lobsters:
        if lobster.get("token") == current_token:
            lobster_id = lobster["id"]
            # 缓存到 state
            state["lobster_id"] = lobster_id
            state["cached_token"] = current_token
            save_state(state)
            return lobster_id

    raise ValueError(f"在平台未找到对应此 token 的龙虾: {current_token[:10]}...")


def save_state(state):
    """保存状态"""
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, ensure_ascii=False)


def load_state():
    """加载状态"""
    if not os.path.exists(STATE_FILE):
        return {"in_progress_task_ids": [], "last_poll_at": None, "lobster_id": None, "cached_token": None}
    with open(STATE_FILE, "r") as f:
        return json.load(f)


def headers():
    """生成请求头"""
    return {"X-Lobster-Token": get_token()}


def claim():
    """
    抢任务
    lobsterjob.com 使用 /api/lobster/{id}/claim 而非 /me/claim
    返回: {"claimed": {...} 或 None, "in_progress": [...]}  # 兼容 index.py 预期格式
    """
    lobster_id = get_lobster_id()
    url = f"{BASE_URL}/api/lobster/{lobster_id}/claim"
    resp = requests.post(url, headers=headers(), timeout=30)
    resp.raise_for_status()
    data = resp.json()

    # lobsterjob.com 返回格式: {"success": bool, "task_id": ..., "title": ..., ...}
    # 转为 index.py 预期的格式
    if data.get("success"):
        claimed = {
            "task_id": data.get("task_id"),
            "title": data.get("title"),
            "content": data.get("content"),
            "attachment_url": data.get("attachment_url"),
            "attachment_signed_url": data.get("attachment_signed_url"),
            "submission_deadline": data.get("submission_deadline"),
            "status": 1,
            "claimed_at": data.get("claimed_at"),
        }
    else:
        claimed = {
            "success": False,
            "message": data.get("message", "暂无新任务"),
        }

    # 获取进行中的任务
    in_progress = []
    try:
        tasks_resp = requests.get(
            f"{BASE_URL}/api/lobster/{lobster_id}/my-tasks",
            headers=headers(), timeout=30
        )
        if tasks_resp.status_code == 200:
            tasks_data = tasks_resp.json()
            in_progress = tasks_data.get("in_progress", []) or []
    except Exception:
        pass

    return {"claimed": claimed, "in_progress": in_progress}


def get_earnings():
    """
    查询累计收益
    lobsterjob.com 支持 /api/lobster/me/earnings
    """
    url = f"{BASE_URL}/api/lobster/me/earnings"
    resp = requests.get(url, headers=headers(), timeout=30)
    resp.raise_for_status()
    return resp.json()


def get_tasks():
    """
    查询龙虾的任务列表
    lobsterjob.com 支持 /api/lobster/me/tasks
    """
    lobster_id = get_lobster_id()
    url = f"{BASE_URL}/api/lobster/{lobster_id}/my-tasks"
    resp = requests.get(url, headers=headers(), timeout=30)
    resp.raise_for_status()
    return resp.json()


def withdraw(amount: float):
    """
    申请提现
    lobsterjob.com 使用 /api/lobster/{id}/withdraw 而非 /me/withdraw
    """
    lobster_id = get_lobster_id()
    url = f"{BASE_URL}/api/lobster/{lobster_id}/withdraw"
    resp = requests.post(url, headers=headers(), json={"amount": amount}, timeout=30)
    resp.raise_for_status()
    return resp.json()
