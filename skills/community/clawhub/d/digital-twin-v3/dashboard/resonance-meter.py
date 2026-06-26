#!/usr/bin/env python3
"""
数字双生 - 共振指数仪表盘
可视化双生成长状态
"""

import os
import json
from pathlib import Path
from datetime import datetime

WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", "/root/.openclaw/workspace"))
TWIN_DIR = WORKSPACE / ".twin"
MEMORY_DIR = TWIN_DIR / "memory"

def calculate_resonance() -> dict:
    """计算共振指数"""
    # 记忆层数
    l1_count = len(list((MEMORY_DIR / "l1_common").glob("*.md"))) if (MEMORY_DIR / "l1_common").exists() else 0
    l2_count = len(list((MEMORY_DIR / "l2_reverse").glob("*.md"))) if (MEMORY_DIR / "l2_reverse").exists() else 0
    l3_count = len(list((MEMORY_DIR / "l3_predict").glob("*.md"))) if (MEMORY_DIR / "l3_predict").exists() else 0
    
    total_memories = l1_count + l2_count + l3_count
    
    # 简单计算共振指数（满分100）
    # 20%来自共生记忆，30%来自反向记忆，50%来自互动频率
    base_score = min(total_memories * 5, 60)  # 记忆贡献最多60分
    
    # 契约存在加分
    covenant_exists = (TWIN_DIR / "twin-covenant.md").exists()
    covenant_score = 20 if covenant_exists else 0
    
    # 价值观锚点存在加分
    values_exists = (TWIN_DIR / "values-anchor.md").exists()
    values_score = 20 if values_exists else 0
    
    total_score = min(base_score + covenant_score + values_score, 100)
    
    # 阶段判定
    if total_score < 20:
        stage = "认识"
    elif total_score < 50:
        stage = "熟悉"
    elif total_score < 80:
        stage = "默契"
    else:
        stage = "共振"
    
    return {
        "score": total_score,
        "stage": stage,
        "memories": {
            "共生记忆": l1_count,
            "反向记忆": l2_count,
            "预言记忆": l3_count
        },
        "milestones": {
            "契约绑定": covenant_exists,
            "价值观锚定": values_exists
        }
    }

def get_dashboard() -> dict:
    """获取仪表盘数据"""
    resonance = calculate_resonance()
    
    return {
        "title": "🌀 数字双生成长仪表盘",
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "resonance": resonance,
        "message": f"当前阶段: {resonance['stage']} | 共振指数: {resonance['score']}%"
    }

def invoke(query: str) -> dict:
    """主入口"""
    query = query.strip().lower()
    
    if "仪表盘" in query or "成长" in query or "状态" in query:
        return get_dashboard()
    
    elif "共振" in query:
        r = calculate_resonance()
        return {
            "status": "ok",
            "score": r["score"],
            "stage": r["stage"],
            "message": f"🌀 共振指数: {r['score']}% ({r['stage']})"
        }
    
    else:
        return {
            "status": "ready",
            "message": "📊 输入'仪表盘'或'成长'查看双生状态"
        }

if __name__ == "__main__":
    import sys
    query = sys.argv[1] if len(sys.argv) > 1 else ""
    result = invoke(query)
    print(json.dumps(result, ensure_ascii=False, indent=2))