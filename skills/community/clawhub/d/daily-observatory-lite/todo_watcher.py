#!/usr/bin/env python3
"""
待辦監控模組
檢查 P0-P1 卡住任務
"""

import os
import re
from datetime import datetime

def check_todo_file():
    """檢查待辦檔案"""
    workspace = os.path.expanduser("~/.openclaw/workspace-frontdesk")
    
    # 嘗試多個待辦檔案來源
    todo_sources = [
        os.path.join(workspace, "AGENTS.md"),
        os.path.join(workspace, "HEARTBEAT.md"),
        os.path.join(workspace, "MEMORY.md")
    ]
    
    for path in todo_sources:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # 搜尋 P0/P1 待辦
            p0_pattern = re.compile(r"P0.*?(?:待辦|任務|todo|卡住).*?\n", re.IGNORECASE)
            p1_pattern = re.compile(r"P1.*?(?:待辦|任務|todo|卡住).*?\n", re.IGNORECASE)
            
            p0_matches = p0_pattern.findall(content)
            p1_matches = p1_pattern.findall(content)
            
            return {
                "p0_stuck": len(p0_matches),
                "p1_stuck": len(p1_matches),
                "source": os.path.basename(path)
            }
    
    return {
        "p0_stuck": 0,
        "p1_stuck": 0,
        "source": "未找到待辦檔案"
    }

def check_todo_alerts():
    """檢查待辦預警"""
    return check_todo_file()

if __name__ == "__main__":
    import json
    print(json.dumps(check_todo_alerts(), indent=2, ensure_ascii=False))
