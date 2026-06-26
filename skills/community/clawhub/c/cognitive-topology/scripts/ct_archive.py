#!/usr/bin/env python3
"""
ct_archive.py - 归档拓扑结论到长期记忆
用法: python3 ct_archive.py [拓扑文件]

功能：
1. 从拓扑提取所有分支的L2核心结论
2. 追加到 MEMORY.md
3. 追加到 memory/YYYY-MM-DD.md 每日快照
"""
import json
import sys
import os
import re
from datetime import datetime

MEMORY_FILE = "/root/.openclaw/workspace/MEMORY.md"
MEMORY_DIR = "/root/.openclaw/workspace/memory"

def extract_conclusion(l2_content):
    """从L2文件中提取结论摘要"""
    # 提取 ## 结论 部分
    match = re.search(r'## 结论\s*\n\s*(.+?)(?:\n---|\n## |\Z)', l2_content, re.DOTALL)
    if match:
        text = match.group(1).strip()
        # 截断超长结论
        if len(text) > 200:
            text = text[:200] + "..."
        return text
    return None

def extract_tags(l2_content):
    """从L2内容中提取标签"""
    tags = []
    # 匹配 #标签 格式
    for tag in re.findall(r'#(\w+)', l2_content):
        tags.append(f"#{tag}")
    return list(set(tags))[:5]  # 最多5个标签

def get_branch_summary(branch, l2_content):
    """提取分支概要"""
    branch_id = branch['id']
    
    # 从文件名或L2中推断分支主题
    # 格式: ct-0410173826-01 → 从文件名看序号
    seq = branch_id.split('-')[-1]
    
    conclusion = extract_conclusion(l2_content)
    tags = extract_tags(l2_content)
    
    summary = f"- **{branch_id}**: {conclusion or '(无结论)'}"
    if tags:
        summary += f" | 标签:{','.join(tags)}"
    
    return summary, tags

def archive_to_memory(topo, branch_summaries, all_tags):
    """追加到 MEMORY.md"""
    topo_id = topo['id']
    task = topo['task']
    created = datetime.fromisoformat(topo['created']).strftime('%Y-%m-%d %H:%M')
    branch_count = len(topo['branches'])
    
    entry = f"""

## 认知拓扑归档 | {datetime.now().strftime('%Y-%m-%d')}

### 拓扑 {topo_id}
- **任务**: {task}
- **分支数**: {branch_count}
- **完成时间**: {created}
- **分支结论**:
{chr(10).join([s[0] for s in branch_summaries])}
"""
    
    # 追加到 MEMORY.md
    with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 找到最后一个 ## 标题 的位置，在其前插入
    # 或者追加到文件末尾
    with open(MEMORY_FILE, 'a', encoding='utf-8') as f:
        f.write(entry)
    
    return entry

def archive_to_daily(topo, branch_summaries):
    """追加到每日记忆快照"""
    today = datetime.now().strftime('%Y-%m-%d')
    daily_file = f"{MEMORY_DIR}/{today}.md"
    
    # 确保目录存在
    os.makedirs(MEMORY_DIR, exist_ok=True)
    
    # 如果文件不存在，创建基础结构
    if not os.path.exists(daily_file):
        with open(daily_file, 'w', encoding='utf-8') as f:
            f.write(f"# {today} 日记\n\n")
    
    topo_id = topo['id']
    task = topo['task']
    created = datetime.fromisoformat(topo['created']).strftime('%H:%M')
    
    # 简短总结
    short_conclusions = []
    for s, _ in branch_summaries:
        # 提取分支ID和结论
        match = re.search(r'\*\*(\S+)\*\*: (.+)', s)
        if match:
            bid, conc = match.groups()
            # 结论截断
            if len(conc) > 50:
                conc = conc[:50] + "..."
            short_conclusions.append(f"{bid}: {conc}")
    
    entry = f"""
## 认知拓扑

| 时间 | 拓扑ID | 任务 | 分支数 | 核心结论 |
|------|--------|------|--------|----------|
| {created} | {topo_id} | {task[:30]} | {len(topo['branches'])} | {'; '.join(short_conclusions[:3])[:80]} |
"""
    
    with open(daily_file, 'a', encoding='utf-8') as f:
        f.write(entry)

def main():
    topo_file = sys.argv[1] if len(sys.argv) > 1 else "/root/.openclaw/workspace/cognitive-topology/topology_latest.json"
    
    if not os.path.exists(topo_file):
        print(f"❌ 拓扑文件不存在: {topo_file}")
        sys.exit(1)
    
    with open(topo_file, 'r', encoding='utf-8') as f:
        topo = json.load(f)
    
    print(f"📦 归档拓扑: {topo['id']}")
    print(f"📝 任务: {topo['task']}")
    print()
    
    branch_summaries = []
    all_tags = set()
    
    for branch in topo.get('branches', []):
        l2_file = branch.get('l2_file')
        if l2_file and os.path.exists(l2_file):
            with open(l2_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            summary, tags = get_branch_summary(branch, content)
            branch_summaries.append((summary, tags))
            all_tags.update(tags)
            
            status = "✅" if "*(待填写)*" not in content else "⏳"
            print(f"{status} {branch['id']}")
        else:
            print(f"❌ {branch['id']} - 无L2文件")
    
    if not branch_summaries:
        print("\n❌ 没有可归档的分支")
        return
    
    # 归档到 MEMORY.md
    entry = archive_to_memory(topo, branch_summaries, all_tags)
    print(f"\n✅ 已追加到 MEMORY.md")
    
    # 归档到每日快照
    archive_to_daily(topo, branch_summaries)
    print(f"✅ 已追加到 {datetime.now().strftime('%Y-%m-%d')}.md 每日快照")

if __name__ == "__main__":
    main()
