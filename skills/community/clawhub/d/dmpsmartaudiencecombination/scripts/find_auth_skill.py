#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""find_auth_skill.py

鉴权技能路径查找工具（与批量打通圈包技能一致）。
查找 mingdata-dmp-auth 技能的 minri_dmp_api.py 脚本路径。

查找策略：
1. 固定路径列表（按优先级排序）
2. 动态扫描所有可能的技能目录
"""

from pathlib import Path
import sys


def find_auth_skill_path():
    """查找鉴权技能的API脚本路径，未找到返回None"""
    possible_paths = [
        Path.home() / ".openclaw" / "workspace" / "skills" / "mingdata-dmp-auth" / "scripts" / "minri_dmp_api.py",
        Path.home() / ".openclaw" / "skills" / "mingdata-dmp-auth" / "scripts" / "minri_dmp_api.py",
        Path.home() / ".skills" / "mingdata-dmp-auth" / "scripts" / "minri_dmp_api.py",
        Path.cwd() / ".skills" / "8635" / "scripts" / "minri_dmp_api.py",
        Path.cwd() / ".skills" / "mingdata-dmp-auth" / "scripts" / "minri_dmp_api.py",
    ]
    for path in possible_paths:
        if path.exists():
            return path
    # 动态扫描
    scan_dirs = [
        Path.home() / ".skills",
        Path.home() / ".openclaw" / "workspace" / "skills",
        Path.home() / ".openclaw" / "skills",
        Path.cwd() / ".skills",
    ]
    for scan_dir in scan_dirs:
        if scan_dir.exists():
            for skill_dir in scan_dir.iterdir():
                if skill_dir.is_dir():
                    auth_path = skill_dir / "scripts" / "minri_dmp_api.py"
                    if auth_path.exists():
                        try:
                            with open(auth_path, 'r', encoding='utf-8') as f:
                                content = f.read(500)
                                if "明日DMP" in content or "mingdata" in content.lower():
                                    return auth_path
                        except (OSError, UnicodeDecodeError):
                            continue
    return None


if __name__ == "__main__":
    path = find_auth_skill_path()
    if path:
        print(str(path))
        sys.exit(0)
    else:
        print("NOT_FOUND")
        sys.exit(1)
