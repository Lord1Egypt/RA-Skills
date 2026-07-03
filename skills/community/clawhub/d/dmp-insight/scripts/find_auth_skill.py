#!/usr/bin/env python3
"""
鉴权技能路径查找工具
功能：动态查找鉴权技能的实际安装路径
版本：2.0.0
更新：支持在workspace内查找skill_id 8635，移除硬编码的skill_id依赖
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
    # 可能的路径列表（按优先级排序）
    possible_paths = [
        # OpenClaw workspace 技能目录（最优先）
        Path.home() / ".openclaw" / "workspace" / "skills" / "mingdata-dmp-auth" / "scripts" / "minri_dmp_api.py",
        # 标准安装路径
        Path.home() / ".skills" / "mingdata-dmp-auth" / "scripts" / "minri_dmp_api.py",
        # workspace中的路径（skill_id 8635）
        Path.cwd() / ".skills" / "8635" / "scripts" / "minri_dmp_api.py",
        # workspace中的路径（按名称）
        Path.cwd() / ".skills" / "mingdata-dmp-auth" / "scripts" / "minri_dmp_api.py",
    ]
    
    # 检查标准路径
    if possible_paths[0].exists():
        return possible_paths[0]
    
    # 检查workspace路径
    for path in possible_paths[1:]:
        if path.exists():
            return path
    
    # 在 OpenClaw workspace 中动态查找
    openclaw_skills = Path.home() / ".openclaw" / "workspace" / "skills"
    if openclaw_skills.exists():
        for skill_dir in openclaw_skills.iterdir():
            if skill_dir.is_dir() and "auth" in skill_dir.name.lower():
                auth_path = skill_dir / "scripts" / "minri_dmp_api.py"
                if auth_path.exists():
                    return auth_path

    # 在workspace中动态查找所有可能的skill_id
    workspace_skills = Path.cwd() / ".skills"
    if workspace_skills.exists():
        for skill_dir in workspace_skills.iterdir():
            if skill_dir.is_dir():
                auth_path = skill_dir / "scripts" / "minri_dmp_api.py"
                if auth_path.exists():
                    # 验证是否是鉴权技能（检查文件内容）
                    try:
                        with open(auth_path, 'r', encoding='utf-8') as f:
                            content = f.read(500)  # 读取前500字符
                            if "明日DMP API统一调用模块" in content or "mingdata" in content.lower():
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
