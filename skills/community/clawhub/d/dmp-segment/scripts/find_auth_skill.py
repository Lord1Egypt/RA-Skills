#!/usr/bin/env python3
"""
鉴权技能路径查找工具
功能：动态查找鉴权技能的实际安装路径

"""

from pathlib import Path
import sys

def find_auth_skill_path():
    """
    查找鉴权技能的API脚本路径
    
    查找策略：
    1. 标准安装路径：~/.skills/mingdata-dmp-auth/
    2. workspace内的路径：.skills/8635/ 或 .skills/mingdata-dmp-auth/
    3. 当前工作目录的相对路径
    
    Returns:
        Path: 鉴权技能的minri_dmp_api.py路径，如果未找到则返回None
    """
    # 第一层：固定路径列表（按优先级排序）
    possible_paths = [
        # OpenClaw workspace路径（最优先）
        Path.home() / ".openclaw" / "workspace" / "skills" / "mingdata-dmp-auth" / "scripts" / "minri_dmp_api.py",
        # OpenClaw skills路径
        Path.home() / ".openclaw" / "skills" / "mingdata-dmp-auth" / "scripts" / "minri_dmp_api.py",
        # 标准安装路径
        Path.home() / ".skills" / "mingdata-dmp-auth" / "scripts" / "minri_dmp_api.py",
        # workspace中的路径（skill_id 8635）
        Path.cwd() / ".skills" / "8635" / "scripts" / "minri_dmp_api.py",
        # workspace中的路径（按名称）
        Path.cwd() / ".skills" / "mingdata-dmp-auth" / "scripts" / "minri_dmp_api.py",
    ]
    
    # 检查固定路径
    for path in possible_paths:
        if path.exists():
            return path
    
    # 第二层：动态扫描所有可能的目录
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
                        except:
                            continue
    
    return None

if __name__ == "__main__":
    path = find_auth_skill_path()
    if path:
        print(str(path))
        sys.exit(0)
    else:
        sys.exit(1)
