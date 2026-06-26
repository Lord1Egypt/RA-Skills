#!/usr/bin/env python3
"""
确保 OpenClaw cron 配置存在
"""

import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", default=".", help="工作区根目录")
    parser.add_argument("--interval", default="24h", help="运行间隔")
    args = parser.parse_args()
    
    workspace = Path(args.workspace).expanduser().resolve()
    
    # 解析间隔
    interval_hours = int(args.interval.replace("h", ""))
    
    # OpenClaw cron 配置（简化版，实际应使用 openclaw cron add 命令）
    cron_config = {
        "name": "autodream",
        "command": f"python3 skills/autodream/scripts/autodream_cycle.py --workspace .",
        "interval": f"{interval_hours}h",
        "enabled": True,
    }
    
    # 保存到配置目录
    config_dir = workspace / "skills" / "autodream" / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    
    cron_file = config_dir / "cron.json"
    cron_file.write_text(json.dumps(cron_config, indent=2, ensure_ascii=False), encoding="utf-8")
    
    print(f"✅ Cron 配置已保存：{cron_file}")
    print(f"   提示：请使用 'openclaw cron add' 命令手动添加定时任务，或参考 HEARTBEAT.md 配置心跳检查")


if __name__ == "__main__":
    main()
