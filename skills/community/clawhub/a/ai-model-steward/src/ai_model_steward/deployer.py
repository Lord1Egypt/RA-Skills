"""
AI Model Steward - 部署模块

功能:
1. 审批通过后，将新模型加入 OpenClaw 切换链
2. 配置备份与回滚
"""

import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional, List

OPENCLAW_CONFIG = Path.home() / ".openclaw" / "openclaw.json"


def backup_config(suffix: Optional[str] = None) -> Path:
    """备份当前 OpenClaw 配置"""
    ts = suffix or datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = OPENCLAW_CONFIG.with_suffix(f".json.backup_{ts}")
    shutil.copy2(OPENCLAW_CONFIG, backup_path)
    return backup_path


def rollback_config(backup_path: str) -> bool:
    """从备份回滚配置"""
    bp = Path(backup_path)
    if not bp.exists():
        print(f"❌ 备份文件不存在: {backup_path}")
        return False
    shutil.copy2(bp, OPENCLAW_CONFIG)
    print(f"✅ 已从备份回滚: {backup_path}")
    print("⚠️ 需要重启 Gateway 生效: openclaw gateway restart")
    return True


def add_to_fallbacks(model_id: str, position: Optional[int] = None) -> dict:
    """将模型添加到 fallback 链"""
    if not OPENCLAW_CONFIG.exists():
        return {"status": "error", "message": "OpenClaw 配置不存在"}

    backup_path = backup_config()

    config = json.loads(OPENCLAW_CONFIG.read_text())
    model_config = config.get("agents", {}).get("defaults", {}).get("model", {})
    fallbacks = model_config.get("fallbacks", [])

    if model_id in fallbacks:
        return {"status": "warning", "message": f"{model_id} 已在切换链中"}

    if position is None:
        fallbacks.append(model_id)  # 追加到末尾
    else:
        fallbacks.insert(position, model_id)

    model_config["fallbacks"] = fallbacks

    # 确保 models 列表有该模型
    models_list = config.get("agents", {}).get("defaults", {}).get("models", {})
    if model_id not in models_list:
        models_list[model_id] = {}

    OPENCLAW_CONFIG.write_text(json.dumps(config, indent=2, ensure_ascii=False))

    return {
        "status": "success",
        "model": model_id,
        "position": position or len(fallbacks) - 1,
        "total_fallbacks": len(fallbacks),
        "backup": str(backup_path),
        "message": f"✅ {model_id} 已加入切换链，重启 Gateway 生效",
    }


def remove_from_fallbacks(model_id: str) -> dict:
    """从 fallback 链移除模型"""
    if not OPENCLAW_CONFIG.exists():
        return {"status": "error", "message": "OpenClaw 配置不存在"}

    backup_path = backup_config()

    config = json.loads(OPENCLAW_CONFIG.read_text())
    fallbacks = config.get("agents", {}).get("defaults", {}).get("model", {}).get("fallbacks", [])

    if model_id not in fallbacks:
        return {"status": "warning", "message": f"{model_id} 不在切换链中"}

    fallbacks.remove(model_id)

    OPENCLAW_CONFIG.write_text(json.dumps(config, indent=2, ensure_ascii=False))

    return {
        "status": "success",
        "model": model_id,
        "remaining": len(fallbacks),
        "backup": str(backup_path),
        "message": f"✅ {model_id} 已从切换链移除",
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="AI 模型智能管家 - 部署操作")
    parser.add_argument("action", choices=["add", "remove", "rollback", "list"])
    parser.add_argument("--model", help="模型 ID")
    parser.add_argument("--position", type=int, help="插入位置（从 0 开始）")
    parser.add_argument("--backup-path", help="回滚备份文件路径")
    args = parser.parse_args()

    if args.action == "add":
        if not args.model:
            print("❌ 需要指定 --model")
            exit(1)
        result = add_to_fallbacks(args.model, args.position)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif args.action == "remove":
        if not args.model:
            print("❌ 需要指定 --model")
            exit(1)
        result = remove_from_fallbacks(args.model)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif args.action == "rollback":
        if not args.backup_path:
            print("❌ 需要指定 --backup-path")
            exit(1)
        rollback_config(args.backup_path)

    elif args.action == "list":
        config = json.loads(OPENCLAW_CONFIG.read_text())
        fallbacks = config.get("agents", {}).get("defaults", {}).get("model", {}).get("fallbacks", [])
        print(f"当前切换链 ({len(fallbacks)} 个模型):")
        for i, m in enumerate(fallbacks):
            print(f"  {i+1}. {m}")
