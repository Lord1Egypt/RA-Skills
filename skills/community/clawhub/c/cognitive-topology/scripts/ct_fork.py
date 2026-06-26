#!/usr/bin/env python3
"""
ct_fork.py - 创建分支拓扑
用法: python3 ct_fork.py "<任务描述>" <分支数>
"""
import json
import sys
import os
from datetime import datetime

BRANCH_DIR = "/root/.openclaw/workspace/cognitive-topology/branches"

def main():
    if len(sys.argv) < 3:
        print("用法: python3 ct_fork.py <任务描述> <分支数>")
        sys.exit(1)
    
    task_desc = sys.argv[1]
    branch_count = int(sys.argv[2])
    
    os.makedirs(BRANCH_DIR, exist_ok=True)
    
    timestamp = datetime.now().strftime("%m%d%H%M%S")
    topology_id = f"ct-{timestamp}"
    
    branches = []
    for i in range(branch_count):
        branch_id = f"{topology_id}-{i+1:02d}"
        l2_file = f"{BRANCH_DIR}/{branch_id}_L2.md"
        
        # 创建空的L2文件
        with open(l2_file, 'w', encoding='utf-8') as f:
            f.write(f"# {branch_id}\n\n")
            f.write(f"**任务**: {task_desc} (分支 {i+1}/{branch_count})\n\n")
            f.write(f"**状态**: ⏳ 执行中\n\n")
            f.write(f"**创建时间**: {datetime.now().isoformat()}\n\n")
            f.write("---\n\n")
            f.write("## 结论\n\n*(待填写)*\n\n")
            f.write("## 依据\n\n*(待填写)*\n\n")
        
        branches.append({
            "id": branch_id,
            "l2_file": l2_file,
            "status": "pending"
        })
    
    # 写入拓扑文件
    topology = {
        "id": topology_id,
        "task": task_desc,
        "created": datetime.now().isoformat(),
        "branches": branches
    }
    
    topo_file = f"/root/.openclaw/workspace/cognitive-topology/topology_latest.json"
    with open(topo_file, 'w', encoding='utf-8') as f:
        json.dump(topology, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 拓扑已创建: {topology_id}")
    for b in branches:
        print(f"  📄 {b['id']} → {b['l2_file']}")

if __name__ == "__main__":
    main()
