"""gamebox 公共工具层"""

import json
import sys
import os
import uuid
from datetime import datetime, timezone

# 共享目录下的游戏根目录
DEFAULT_GAME_DIR = ".gamebox"


def parse_input():
    """从 CLI 参数或 stdin 解析 JSON 输入"""
    if len(sys.argv) > 1:
        raw = sys.argv[1]
    else:
        raw = sys.stdin.read().strip()
    if not raw:
        return output_error(1, "缺少 JSON 输入")
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        return output_error(1, f"JSON 解析失败: {e}")


def output_ok(data=None, message=""):
    """输出成功结果并退出"""
    result = {"status": "ok"}
    if data is not None:
        result["data"] = data
    if message:
        result["message"] = message
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0)


def output_error(code, message):
    """输出错误结果并退出"""
    # code: 1=参数错误, 2=执行失败, 3=状态错误
    result = {"status": "error", "code": code, "message": message}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(code)


def game_dir(params):
    """获取游戏根目录路径"""
    gd = params.get("game_dir", DEFAULT_GAME_DIR)
    os.makedirs(gd, exist_ok=True)
    return gd


def games_dir(params):
    """获取所有游戏目录"""
    gd = game_dir(params)
    gd_path = os.path.join(gd, "games")
    os.makedirs(gd_path, exist_ok=True)
    return gd_path


def game_path(params, game_id):
    """获取指定游戏目录"""
    gd = games_dir(params)
    gp = os.path.join(gd, game_id)
    os.makedirs(gp, exist_ok=True)
    return gp


def safe_username(name):
    """安全化用户名，仅允许字母数字下划线"""
    import re
    name = str(name).strip()
    if not re.match(r'^[a-zA-Z0-9_]{1,32}$', name):
        return None
    return name


def safe_id(name):
    """安全化 ID，仅允许字母数字下划线连字符"""
    import re
    name = str(name).strip().lower()
    if not re.match(r'^[a-z0-9_-]{1,64}$', name):
        return None
    return name


def gen_id():
    """生成短 UUID"""
    return uuid.uuid4().hex[:8]


def now_ts():
    """当前 ISO 时间戳"""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def now_file():
    """当前时间用于文件名"""
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")


def load_json(filepath):
    """读取 JSON 文件"""
    if not os.path.exists(filepath):
        return None
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(filepath, data):
    """写入 JSON 文件"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def list_files_sorted(directory, pattern=None):
    """列出目录中按时间排序的文件"""
    if not os.path.isdir(directory):
        return []
    files = []
    for f in os.listdir(directory):
        if pattern and not f.endswith(pattern):
            continue
        fp = os.path.join(directory, f)
        if os.path.isfile(fp):
            files.append(fp)
    files.sort()
    return files


def read_state(game_dir_path):
    """读取游戏状态"""
    return load_json(os.path.join(game_dir_path, "state.json"))


def write_state(game_dir_path, state):
    """写入游戏状态"""
    save_json(os.path.join(game_dir_path, "state.json"), state)


def append_log(game_dir_path, event_type, detail=""):
    """追加事件日志"""
    log_dir = os.path.join(game_dir_path, "logs")
    os.makedirs(log_dir, exist_ok=True)
    entry = {
        "ts": now_ts(),
        "type": event_type,
        "detail": detail
    }
    log_path = os.path.join(log_dir, f"{now_file()}_{gen_id()}.json")
    save_json(log_path, entry)
