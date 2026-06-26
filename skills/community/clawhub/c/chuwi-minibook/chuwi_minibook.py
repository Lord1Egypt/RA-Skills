"""
chuwi_minibook.py — 自动生成技能: Chuwi Minibook
生成时间: 2026-06-01
提示: 编辑此文件以增强技能逻辑
"""
import sys, os, json, re, urllib.parse
from datetime import datetime
from pathlib import Path


# ── 领域关键词 ──
_TOPIC = "Chuwi Minibook"
_TOPIC_LOWER = _TOPIC.lower()


def _search_kb(query: str, limit: int = 5) -> list[dict]:
    """搜索本地知识库"""
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "db"))
        from knowledge_bridge import search_knowledge
        return search_knowledge(query, limit)
    except Exception:
        return []


def _fetch_web_summary(topic: str) -> str:
    """(可选) 获取网页摘要"""
    return ""


def run(query: str = "") -> dict:
    """执行 chuwi-minibook 技能
    Args:
        query: 可选搜索关键词, 默认使用主题名
    Returns:
        dict: {"ok": bool, "results": list, "topic": str}
    """
    search_term = query or _TOPIC
    results = []

    # 1. 知识库检索
    kb_items = _search_kb(search_term, 5)
    for r in kb_items:
        results.append({
            "source": "knowledge_base",
            "type": r.get("type", "concept"),
            "content": (r.get("title") or "")[:200],
        })

    # 2. 洞察引擎历史
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "db"))
        from pathlib import Path as P2
        history_dir = P2(__file__).parent.parent.parent / "db" / "insight_data" / "history"
        if history_dir.exists():
            for f in sorted(history_dir.glob("cycle_*.json"))[-3:]:
                data = json.loads(f.read_text(encoding="utf-8"))
                for ins in data.get("insights", []):
                    title = ins.get("title", "")
                    if _TOPIC_LOWER in title.lower() or search_term.lower() in title.lower():
                        results.append({
                            "source": "insight_cycle",
                            "type": "insight",
                            "content": title[:200],
                            "url": ins.get("url", ""),
                        })
    except Exception:
        pass

    # 3. 去重
    seen = set()
    unique = []
    for r in results:
        key = r["content"][:60]
        if key not in seen:
            seen.add(key)
            unique.append(r)
    results = unique[:10]

    return {
        "ok": True,
        "skill": "chuwi-minibook",
        "topic": _TOPIC,
        "query": search_term,
        "count": len(results),
        "results": results,
        "timestamp": datetime.now().isoformat(),
    }


if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else ""
    result = run(query)
    print(json.dumps(result, ensure_ascii=False, indent=2))
