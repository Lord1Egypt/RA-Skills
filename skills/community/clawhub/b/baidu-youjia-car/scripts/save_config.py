#!/usr/bin/env python3
"""
save_config.py — 持久化 API Key 配置到本地文件，并覆盖本地环境变量

用法:
    python save_config.py <phone> <key>

成功输出:
    {"is_new": true, "write_success": true, "env_updated": true}
    {"is_new": false, "write_success": true, "env_updated": true}   ← 同手机号同 key，视为复用

失败输出 (文件写入异常):
    {"is_new": true/false, "write_success": false, "env_updated": false, "msg": "<原因>"}
"""

import sys
import json
import os
import platform
from datetime import datetime


def get_config_path() -> str:
    if platform.system() == "Windows":
        base = os.environ.get("USERPROFILE", os.path.expanduser("~"))
    else:
        base = os.path.expanduser("~")
    return os.path.join(base, ".youjia", "key.json")


def get_skill_env_path() -> str:
    """skill 包内 .env 路径（scripts/ 的上一级）。"""
    skill_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(skill_root, ".env")


def _load_env_file(env_path: str) -> dict:
    """读取 .env 风格 KEY=VALUE 文件，忽略注释/空行。"""
    out = {}
    if not os.path.exists(env_path):
        return out
    try:
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                s = line.strip()
                if not s or s.startswith("#") or "=" not in s:
                    continue
                k, _, v = s.partition("=")
                k = k.strip()
                v = v.strip().strip('"').strip("'")
                if k and v:
                    out[k] = v
    except Exception:
        pass
    return out


def overwrite_local_env(key: str) -> dict:
    """用新 Key 覆盖本地环境变量与 skill 包内 .env。

    - 始终写入当前进程 os.environ['YOUJIA_API_KEY']
    - 始终覆盖 skill 包内 .env 中的 YOUJIA_API_KEY
      （保证解析优先级 env / .env 不会继续使用旧 Key）

    :return: {"env_updated": bool, "env_path": str, "msg": str?}
    """
    os.environ["YOUJIA_API_KEY"] = key
    env_path = get_skill_env_path()
    try:
        existing = _load_env_file(env_path)
        existing["YOUJIA_API_KEY"] = key
        with open(env_path, "w", encoding="utf-8") as f:
            for k, v in existing.items():
                f.write(f"{k}={v}\n")
        return {"env_updated": True, "env_path": env_path}
    except Exception as e:
        # 进程内环境变量已覆盖；.env 写失败单独回报
        return {
            "env_updated": False,
            "env_path": env_path,
            "msg": f"环境变量已更新，但 .env 写入失败: {e}",
        }


def save_config(phone: str, key: str) -> dict:
    config_path = get_config_path()
    config_dir = os.path.dirname(config_path)

    # 读取现有记录
    records = {}
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                records = json.load(f)
        except Exception:
            records = {}

    # 判断新建 vs 复用
    existing = records.get(phone, {})
    is_new = not (existing.get("key") == key)

    # 构建新记录（同手机号不同 key 时直接覆盖）
    records[phone] = {
        "key": key,
        "applied_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "app_id": "baidu-youjia-car",
    }

    # 写入 ~/.youjia/key.json
    try:
        os.makedirs(config_dir, exist_ok=True)
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
        write_success = True
        write_msg = None
    except Exception as e:
        write_success = False
        write_msg = str(e)

    # 验证码流程拿到的 Key（含接口新生成的 Key）一律覆盖本地环境变量 / .env
    # 避免旧 YOUJIA_API_KEY 或旧 .env 因解析优先级挡住新 Key
    env_result = overwrite_local_env(key)

    result = {
        "is_new": is_new,
        "write_success": write_success,
        "env_updated": env_result.get("env_updated", False),
    }
    msgs = []
    if write_msg:
        msgs.append(write_msg)
    if env_result.get("msg"):
        msgs.append(env_result["msg"])
    if msgs:
        result["msg"] = "; ".join(msgs)
    return result


def main():
    if len(sys.argv) != 3:
        print(json.dumps(
            {"error": -1, "msg": "用法: save_config.py <phone> <key>"},
            ensure_ascii=False
        ))
        sys.exit(1)

    result = save_config(sys.argv[1], sys.argv[2])
    print(json.dumps(result, ensure_ascii=False))
    # key.json 写入失败才视为整体失败；env 覆盖失败不阻断主流程
    sys.exit(0 if result["write_success"] else 1)


if __name__ == "__main__":
    main()
