#!/usr/bin/env python3
"""
数字双生 - 记忆迁移脚本
把共生前的记忆全部迁移到双生系统
"""

import os
import json
from pathlib import Path
from datetime import datetime
import re

WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", "/root/.openclaw/workspace"))
TWIN_DIR = WORKSPACE / ".twin"
MEMORY_DIR = TWIN_DIR / "memory"
L1_DIR = MEMORY_DIR / "l1_common"

def extract_key_info(file_path: Path, file_type: str) -> str:
    """从文件中提取关键信息"""
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()
        
        # 根据文件类型提取关键信息
        if file_type == "memory":
            # 提取日期和主要内容
            lines = content.split("\n")
            key_lines = []
            for line in lines:
                if line.startswith("# "):
                    key_lines.append(line)
                elif line.startswith("## "):
                    key_lines.append(line)
                elif line.strip().startswith("- ") and len(line) < 100:
                    key_lines.append(line)
            return "\n".join(key_lines[:20])  # 取前20条
        
        elif file_type == "soul":
            # 提取身份、性格、原则
            key_sections = []
            for section in ["我是谁", "我的名字", "性格", "说话", "相处", "原则", "底线"]:
                if section in content:
                    start = content.find(section)
                    end = min(start + 500, len(content))
                    key_sections.append(content[start:end])
            return "\n".join(key_sections) if key_sections else content[:1000]
        
        elif file_type == "user":
            return content[:500]
        
        else:
            return content[:500]
    
    except Exception as e:
        return f"[读取失败: {e}]"

def migrate_file(file_path: Path, source_name: str, file_type: str = "general") -> dict:
    """迁移单个文件到共生记忆"""
    key_info = extract_key_info(file_path, file_type)
    
    if not key_info or key_info == "[读取失败: ]":
        return {"status": "skipped", "reason": "无有效内容", "file": str(file_path)}
    
    # 生成文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"migrated_{source_name}_{timestamp}.md"
    filepath = L1_DIR / filename
    
    markdown = f"""# 迁移记忆 - {source_name}

**来源**: {file_path.name}
**迁移时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**类型**: {file_type}

---

{key_info}

---

*此记忆由共生前迁移而来*
"""
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(markdown)
    
    return {
        "status": "success",
        "file": str(filepath),
        "size": len(key_info)
    }

def migrate_all():
    """执行全量迁移"""
    results = []
    
    # 1. 迁移 memory/ 目录下的日记
    memory_dir = WORKSPACE / "memory"
    if memory_dir.exists():
        for f in sorted(memory_dir.glob("*.md")):
            if f.name.startswith("."):
                continue
            result = migrate_file(f, f"memory_{f.stem[:10]}", "memory")
            results.append(result)
    
    # 2. 迁移 MEMORY.md (长期记忆)
    memory_md = WORKSPACE / "MEMORY.md"
    if memory_md.exists():
        result = migrate_file(memory_md, "长期记忆", "memory")
        results.append(result)
    
    # 3. 迁移 SOUL.md (灵魂)
    soul_md = WORKSPACE / "SOUL.md"
    if soul_md.exists():
        result = migrate_file(soul_md, "灵魂定义", "soul")
        results.append(result)
    
    # 4. 迁移 USER.md (用户画像)
    user_md = WORKSPACE / "USER.md"
    if user_md.exists():
        result = migrate_file(user_md, "用户画像", "user")
        results.append(result)
    
    # 5. 迁移 AGENTS.md
    agents_md = WORKSPACE / "AGENTS.md"
    if agents_md.exists():
        result = migrate_file(agents_md, "智能体框架", "general")
        results.append(result)
    
    # 6. 迁移 TOOLS.md
    tools_md = WORKSPACE / "TOOLS.md"
    if tools_md.exists():
        result = migrate_file(tools_md, "工具配置", "general")
        results.append(result)
    
    return results

if __name__ == "__main__":
    print("🌀 开始记忆迁移...")
    
    results = migrate_all()
    
    success = sum(1 for r in results if r["status"] == "success")
    skipped = sum(1 for r in results if r["status"] == "skipped")
    
    print(f"\n✅ 迁移完成!")
    print(f"   成功: {success}")
    print(f"   跳过: {skipped}")
    print(f"\n📊 共生成熟记忆: {len(list(L1_DIR.glob('*.md')))} 条")