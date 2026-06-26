#!/usr/bin/env python3
"""
数字双生 - 记忆桥梁
处理三层记忆的存取：共生记忆、反向记忆、预言记忆
"""

import json
import os
import re
from pathlib import Path
from datetime import datetime

WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", "/root/.openclaw/workspace"))
TWIN_DIR = WORKSPACE / ".twin"
MEMORY_DIR = TWIN_DIR / "memory"

L1_DIR = MEMORY_DIR / "l1_common"   # 共生记忆
L2_DIR = MEMORY_DIR / "l2_reverse"  # 反向记忆
L3_DIR = MEMORY_DIR / "l3_predict"  # 预言记忆

def ensure_dirs():
    """确保目录存在"""
    for d in [L1_DIR, L2_DIR, L3_DIR]:
        d.mkdir(parents=True, exist_ok=True)

def save_memory(layer: int, content: str, tags: list = None) -> dict:
    """
    保存记忆
    
    layer: 1=共生, 2=反向, 3=预言
    content: 记忆内容
    tags: 标签（可选）
    """
    ensure_dirs()
    
    if layer == 1:
        target_dir = L1_DIR
    elif layer == 2:
        target_dir = L2_DIR
    else:
        target_dir = L3_DIR
    
    # 生成文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}.md"
    filepath = target_dir / filename
    
    # 构建内容
    tag_str = ", ".join(tags) if tags else "无标签"
    markdown = f"""# 记忆 - {datetime.now().strftime("%Y-%m-%d %H:%M")}

**层级**: {"共生记忆" if layer==1 else "反向记忆" if layer==2 else "预言记忆"}
**标签**: {tag_str}

---

{content}

---

*自动记录于 {datetime.now().isoformat()}*
"""
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(markdown)
    
    return {
        "status": "saved",
        "layer": layer,
        "layer_name": ["", "共生记忆", "反向记忆", "预言记忆"][layer],
        "file": str(filepath),
        "size": len(content)
    }

def load_memories(layer: int = None, limit: int = 10) -> dict:
    """
    读取记忆
    
    layer: None=全部, 1/2/3=指定层级
    limit: 返回数量
    """
    ensure_dirs()
    
    result = {}
    
    for lvl, dir_path in [(1, L1_DIR), (2, L2_DIR), (3, L3_DIR)]:
        if layer and layer != lvl:
            continue
        
        memories = []
        if dir_path.exists():
            for f in sorted(dir_path.glob("*.md"), reverse=True)[:limit]:
                with open(f, encoding="utf-8") as file:
                    content = file.read()
                    # 提取标题和前100字
                    lines = content.split("\n")
                    title = lines[0].replace("# 记忆 - ", "") if lines else "无标题"
                    preview = content[100:200] if len(content) > 100 else content[100:]
                    memories.append({
                        "file": f.name,
                        "title": title,
                        "preview": preview.strip()
                    })
        
        result[lvl] = {
            "name": ["", "共生记忆", "反向记忆", "预言记忆"][lvl],
            "count": len(memories),
            "items": memories
        }
    
    return result

def detect_conflicts(new_content: str) -> list:
    """
    检测记忆冲突（污染检测）
    检查新记忆是否与已有记忆矛盾
    """
    # 简单的关键词冲突检测
    # 实际使用时可以用更复杂的语义分析
    
    conflict_patterns = [
        (["喜欢", "爱"], ["讨厌", "恨", "不喜欢"]),
        (["可以", "会"], ["不可以", "不会", "不能"]),
        (["是"], ["不是"]),
    ]
    
    conflicts = []
    existing_memories = list(L1_DIR.glob("*.md"))
    
    for memory_file in existing_memories[:5]:  # 检查最近5条
        with open(memory_file, encoding="utf-8") as f:
            existing = f.read()
            
            # 简单的冲突检测
            for pos, neg in conflict_patterns:
                has_pos = any(p in new_content for p in pos)
                has_neg = any(n in new_content for n in neg)
                
                if has_pos and has_neg:
                    # 检查是否存在于同一条记忆
                    if (any(p in existing for p in pos) and 
                        any(n in existing for n in neg)):
                        conflicts.append(f"可能与 {memory_file.name} 冲突")
    
    return conflicts

def invoke(query: str) -> dict:
    """主入口"""
    query = query.strip().lower()
    
    # 存记忆
    if "记住" in query or "存记忆" in query:
        # 简单解析：从query中提取要记住的内容
        # 实际应该从上下文获取
        content = query.replace("记住", "").replace("存记忆", "").strip()
        
        if not content:
            return {"status": "need_content", "message": "告诉我你要记住什么？"}
        
        # 检测冲突
        conflicts = detect_conflicts(content)
        
        # 默认存到共生记忆
        result = save_memory(1, content)
        
        if conflicts:
            result["warnings"] = conflicts
            result["message"] = f"⚠️ 记下了，但检测到可能冲突：{conflicts[0]}"
        else:
            result["message"] = f"✅ 记住了：{content[:50]}..."
        
        return result
    
    # 读记忆
    elif "查看记忆" in query or "我的记忆" in query:
        memories = load_memories()
        
        summary = []
        for lvl, data in memories.items():
            if data["count"] > 0:
                summary.append(f"{data['name']}: {data['count']}条")
        
        if summary:
            return {
                "status": "ok",
                "message": "🧠 " + " | ".join(summary),
                "details": memories
            }
        else:
            return {"status": "empty", "message": "我们还没有记忆呢"}
    
    # 预言记忆
    elif "预测" in query or "预言" in query:
        predictions = list(L3_DIR.glob("*.md"))
        return {
            "status": "ok",
            "count": len(predictions),
            "predictions": [p.stem for p in predictions[:5]]
        }
    
    else:
        return {
            "status": "ready",
            "message": "🧠 记忆系统就绪。说'记住XXX'来存记忆，或'查看记忆'来浏览"
        }

if __name__ == "__main__":
    import sys
    query = sys.argv[1] if len(sys.argv) > 1 else ""
    result = invoke(query)
    print(json.dumps(result, ensure_ascii=False, indent=2))