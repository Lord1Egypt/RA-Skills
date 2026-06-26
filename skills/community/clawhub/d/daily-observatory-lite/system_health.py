#!/usr/bin/env python3
"""
系統健康檢查模組
"""

import subprocess
import os

def check_gateway():
    """檢查 Gateway 狀態"""
    try:
        result = subprocess.run(
            ["openclaw", "gateway", "status"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            return "正常"
        else:
            return "異常"
    except Exception as e:
        return f"錯誤: {str(e)}"

def check_memory_structure():
    """檢查記憶結構"""
    workspace = os.path.expanduser("~/.openclaw/workspace-frontdesk")
    memory_dir = os.path.join(workspace, "memory")
    
    if not os.path.exists(memory_dir):
        return "缺失"
    
    # 檢查必要檔案
    required_files = ["MEMORY.md", "EMOJI-JOURNAL.md"]
    missing = []
    
    for file in required_files:
        path = os.path.join(workspace, file)
        if not os.path.exists(path):
            missing.append(file)
    
    if missing:
        return f"缺失: {', '.join(missing)}"
    
    return "完整"

def check_skills():
    """檢查技能狀態"""
    try:
        result = subprocess.run(
            ["openclaw", "agents", "list"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            lines = result.stdout.split("\n")
            skill_count = len([l for l in lines if l.strip().startswith("-")])
            return f"{skill_count} 個正常"
        else:
            return "檢查失敗"
    except Exception as e:
        return f"錯誤: {str(e)}"

def check_system_health():
    """檢查系統健康（三合一）"""
    return {
        "gateway_status": check_gateway(),
        "memory_status": check_memory_structure(),
        "skills_status": check_skills()
    }

if __name__ == "__main__":
    import json
    print(json.dumps(check_system_health(), indent=2, ensure_ascii=False))
