#!/usr/bin/env python3
"""
ct_status.py - 查看当前拓扑状态
用法: python3 ct_status.py
"""
import json
import os
import glob

BRANCH_DIR = "/root/.openclaw/workspace/cognitive-topology/branches"
TOPO_FILE = "/root/.openclaw/workspace/cognitive-topology/topology_latest.json"

def main():
    print("🌐 Cognitive Topology 状态\n")
    
    if not os.path.exists(TOPO_FILE):
        print("📭 暂无活跃拓扑")
        return
    
    with open(TOPO_FILE, 'r', encoding='utf-8') as f:
        topo = json.load(f)
    
    print(f"拓扑ID: {topo['id']}")
    print(f"主任务: {topo['task']}")
    print(f"创建时间: {topo['created']}")
    print(f"分支数: {len(topo['branches'])}")
    print()
    
    done = 0
    for b in topo['branches']:
        l2_file = b.get('l2_file', '')
        status = b.get('status', 'unknown')
        
        if os.path.exists(l2_file):
            with open(l2_file, 'r') as f:
                content = f.read()
            if "*(待填写)*" in content:
                status = "⏳ 进行中"
            else:
                status = "✅ 已完成"
                done += 1
        else:
            status = "❌ 无文件"
        
        print(f"  {status} {b['id']}")
    
    print(f"\n进度: {done}/{len(topo['branches'])} 分支已完成")
    
    # 显示最新synthesis
    synth_file = "/root/.openclaw/workspace/cognitive-topology/synthesis.md"
    if os.path.exists(synth_file):
        print(f"\n📄 Synthesis文件已生成，可用 ct_integrate.py 读取")

if __name__ == "__main__":
    main()
