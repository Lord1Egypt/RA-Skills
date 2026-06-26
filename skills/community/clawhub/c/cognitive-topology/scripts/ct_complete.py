#!/usr/bin/env python3
"""
ct_complete.py - 标记分支完成并更新拓扑状态
用法: python3 ct_complete.py <branch_id> [l2文件内容]

当分支Agent完成任务后调用此脚本，更新拓扑JSON中的分支状态为done。
"""
import json
import sys
import os
from datetime import datetime

TOPO_FILE = "/root/.openclaw/workspace/cognitive-topology/topology_latest.json"

def main():
    if len(sys.argv) < 2:
        print("用法: python3 ct_complete.py <branch_id>")
        sys.exit(1)
    
    branch_id = sys.argv[1]
    
    if not os.path.exists(TOPO_FILE):
        print(f"❌ 拓扑文件不存在: {TOPO_FILE}")
        sys.exit(1)
    
    with open(TOPO_FILE, 'r', encoding='utf-8') as f:
        topo = json.load(f)
    
    # 找到对应分支
    found = False
    for branch in topo.get('branches', []):
        if branch['id'] == branch_id:
            branch['status'] = 'done'
            branch['completed_at'] = datetime.now().isoformat()
            found = True
            print(f"✅ 分支已标记完成: {branch_id}")
            break
    
    if not found:
        print(f"❌ 未找到分支: {branch_id}")
        print(f"   可用分支: {[b['id'] for b in topo.get('branches', [])]}")
        sys.exit(1)
    
    # 检查是否所有分支都完成
    all_done = all(b.get('status') == 'done' for b in topo['branches'])
    topo['all_done'] = all_done
    topo['updated_at'] = datetime.now().isoformat()
    
    if all_done:
        print(f"🎉 所有分支已完成，拓扑可进行整合")
    
    # 写回拓扑文件
    with open(TOPO_FILE, 'w', encoding='utf-8') as f:
        json.dump(topo, f, ensure_ascii=False, indent=2)
    
    # 打印当前状态
    print(f"\n📊 拓扑状态: {topo['id']}")
    for b in topo['branches']:
        icon = '✅' if b.get('status') == 'done' else '⏳'
        print(f"   {icon} {b['id']} [{b.get('status', 'unknown')}]")

if __name__ == "__main__":
    main()
