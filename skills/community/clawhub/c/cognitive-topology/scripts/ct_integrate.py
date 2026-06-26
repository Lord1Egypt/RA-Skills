#!/usr/bin/env python3
"""
ct_integrate.py - 整合所有分支L2，生成synthesis
用法: python3 ct_integrate.py [拓扑文件]
"""
import json
import sys
import os
from datetime import datetime

BRANCH_DIR = "/root/.openclaw/workspace/cognitive-topology/branches"

def main():
    topo_file = sys.argv[1] if len(sys.argv) > 1 else "/root/.openclaw/workspace/cognitive-topology/topology_latest.json"
    
    if not os.path.exists(topo_file):
        print(f"❌ 拓扑文件不存在: {topo_file}")
        sys.exit(1)
    
    with open(topo_file, 'r', encoding='utf-8') as f:
        topo = json.load(f)
    
    print(f"📊 整合拓扑: {topo['id']}")
    print(f"📝 主任务: {topo['task']}")
    print()
    
    all_l2 = []
    done_count = 0
    for branch in topo.get("branches", []):
        l2_file = branch.get("l2_file")
        status = branch.get("status", "unknown")
        
        # 优先读JSON中的status，其次读文件内容
        if status != "done" and l2_file and os.path.exists(l2_file):
            with open(l2_file, 'r', encoding='utf-8') as f:
                content = f.read()
            if "*(待填写)*" not in content:
                status = "done"
        
        icon = '✅' if status == 'done' else '⏳'
        print(f"{icon} {branch['id']} [{status}]")
        
        if status == 'done' and l2_file and os.path.exists(l2_file):
            with open(l2_file, 'r', encoding='utf-8') as f:
                content = f.read()
            all_l2.append({"branch_id": branch["id"], "content": content})
            done_count += 1
        elif status != 'done':
            print(f"   ⚠️ 分支未完成，跳过")
    
    if not all_l2:
        print(f"\n❌ 没有已完成的分支")
        return
    
    print(f"\n📦 已收集 {done_count}/{len(topo['branches'])} 个分支的L2")
    
    # 生成synthesis
    synthesis_file = "/root/.openclaw/workspace/cognitive-topology/synthesis.md"
    with open(synthesis_file, 'w', encoding='utf-8') as f:
        f.write(f"# {topo['task']}\n\n")
        f.write(f"**整合时间**: {datetime.now().isoformat()}\n\n")
        f.write(f"**分支数量**: {len(topo['branches'])} | **已完成**: {len(all_l2)}\n\n")
        f.write("---\n\n")
        
        for item in all_l2:
            f.write(f"\n## 📍 {item['branch_id']}\n\n")
            f.write(item['content'])
            f.write("\n\n---\n\n")
        
        f.write("\n## 🔮 综合洞察\n\n")
        f.write("*(基于以上各分支分析的综合判断)*\n\n")
    
    print(f"\n✅ Synthesis已生成: {synthesis_file}")
    
    # 自动归档到长期记忆
    import subprocess
    try:
        result = subprocess.run(
            ['python3', '/root/.openclaw/workspace/skills/cognitive-topology/scripts/ct_archive.py', topo_file],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            print(result.stdout)
        else:
            print(f"⚠️ 归档提示: {result.stderr}")
    except Exception as e:
        print(f"⚠️ 自动归档失败: {e}")
    
    return synthesis_file

if __name__ == "__main__":
    main()
