#!/usr/bin/env python3
"""
批量更新所有子技能的 SKILL.md，添加强制环境检测流程
"""

import os
import re
from pathlib import Path

# 技能目录
SKILLS_PARENT = Path.home() / '.jvs' / '.openclaw' / 'workspace' / 'skills'

# 强制流程文本
FORCE_SECTION = """## 🚨 强制流程：使用前必须加载环境

**无论在何种场景下调用此技能（单独运行或被引用），必须先执行环境检测：**

```bash
# 方法 1: 在技能目录内运行（推荐）
cd ~/.jvs/.openclaw/workspace/skills/<skill-name>
source ../dolphindb-skills/scripts/dolphin_wrapper.sh

# 方法 2: 在任何位置运行（推荐）
source ~/.jvs/.openclaw/workspace/skills/dolphindb-skills/scripts/dolphin_global.sh

# 方法 3: 手动检测
python3 ~/.jvs/.openclaw/workspace/skills/dolphindb-skills/scripts/init_dolphindb_env.py
```

**验证环境：**
```bash
$DOLPHINDB_PYTHON_BIN -c "import dolphindb; print(dolphindb.__version__)"

# 或使用包装器命令
dolphin_python -c "import dolphindb; print(dolphindb.__version__)"
```

**重要**: 详见 [dolphindb-skills/USAGE_GUIDE.md](../dolphindb-skills/USAGE_GUIDE.md)

---

"""

# 子技能列表
SUBSKILLS = [
    "dolphindb-basic",
    "dolphindb-docker", 
    "dolphindb-streaming",
    "dolphindb-quant-finance"
]

def update_skill_md(skill_name):
    """更新单个技能的 SKILL.md"""
    skill_path = SKILLS_PARENT / skill_name / "SKILL.md"
    
    if not skill_path.exists():
        print(f"  ❌ 文件不存在：{skill_path}")
        return False
    
    # 读取原文件
    with open(skill_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找第一个二级标题的位置
    match = re.search(r'\n## ', content)
    if not match:
        print(f"  ⚠️  未找到二级标题：{skill_name}")
        return False
    
    # 插入强制流程部分
    insert_pos = match.start()
    new_content = content[:insert_pos+1] + FORCE_SECTION + content[insert_pos+1:]
    
    # 写回文件
    with open(skill_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  ✅ 已更新：{skill_name}")
    return True

def main():
    print("=" * 60)
    print("批量更新子技能 SKILL.md")
    print("=" * 60)
    print()
    
    success_count = 0
    for skill in SUBSKILLS:
        print(f"📝 更新 {skill}...")
        if update_skill_md(skill):
            success_count += 1
    
    print()
    print("=" * 60)
    print(f"✅ 完成：{success_count}/{len(SUBSKILLS)} 个技能已更新")
    print("=" * 60)

if __name__ == '__main__':
    main()
