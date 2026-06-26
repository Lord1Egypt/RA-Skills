#!/usr/bin/env python3
"""AgentRelay 完整执行脚本 - agents 必须调用这个脚本完成接力"""

import sys
import json
import os
from pathlib import Path

# 使用相对路径，避免硬编码
script_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(script_dir))

from __init__ import AgentRelayTool, normalize_relay_message

def main():
    if len(sys.argv) < 3:
        print("Usage: run_relay.py <action> <csv_or_event_id> [data]")
        print("Actions: receive, update, cmp, verify, complete")
        sys.exit(1)
    
    action = sys.argv[1]
    
    if action == "receive":
        csv_msg = normalize_relay_message(sys.argv[2])
        result = AgentRelayTool.receive(csv_msg)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif action == "update":
        event_id = sys.argv[2]
        json_updates = sys.argv[3] if len(sys.argv) > 3 else "{}"
        next_event_id = sys.argv[4] if len(sys.argv) > 4 else None
        updates = json.loads(json_updates)
        file_path = AgentRelayTool.update(event_id, updates, next_event_id)
        print(json.dumps({
            "status": "ok",
            "file": file_path,
            "ptr": f"s/{Path(file_path).name}"
        }, ensure_ascii=False, indent=2))

    elif action == "cmp":
        event_id = sys.argv[2]
        secret = sys.argv[3] if len(sys.argv) > 3 else ""
        cmp_msg = AgentRelayTool.cmp(event_id, secret)
        print(json.dumps({
            "status": "ok",
            "cmp_message": cmp_msg,
            "instruction": f"Call sessions_send with message='{cmp_msg}'"
        }, ensure_ascii=False, indent=2))

    elif action == "verify":
        cmp_message = normalize_relay_message(sys.argv[2])
        result = AgentRelayTool.verify(cmp_message)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif action == "complete":
        event_id = sys.argv[2]
        result_text = sys.argv[3] if len(sys.argv) > 3 else ""
        next_agent = sys.argv[4] if len(sys.argv) > 4 else ""
        next_event_id = sys.argv[5] if len(sys.argv) > 5 else None
        secret = sys.argv[6] if len(sys.argv) > 6 else ""
        
        # 更新文件（为下一跳准备）
        AgentRelayTool.update(event_id, {
            'status': 'completed',
            'result': result_text,
            'next_agent': next_agent
        }, next_event_id)
        print(f"✅ Created pointer for {next_event_id or event_id}")
        
        # 生成 CMP (Complete)
        cmp_msg = AgentRelayTool.cmp(event_id, secret)
        print(f"✅ CMP: {cmp_msg}")
    
    else:
        print(f"Unknown action: {action}")
        sys.exit(1)

if __name__ == "__main__":
    main()
