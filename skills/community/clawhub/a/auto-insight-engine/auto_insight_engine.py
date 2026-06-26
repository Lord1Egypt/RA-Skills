"""
auto_insight_engine.py — 本地化技能: 自动洞察引擎
从6个来源采集洞察并追踪趋势
"""
import sys, os, json
from pathlib import Path

_SRC = Path(__file__).parent.parent.parent / "db"


def run(query: str = "status") -> dict:
    """执行洞察引擎
    Args:
        query: run | status | trends
    Returns:
        dict: 操作结果
    """
    sys.path.insert(0, str(_SRC))
    try:
        from auto_insight_engine import run_cycle, get_engine_status
    except ImportError as e:
        return {"ok": False, "error": f"导入 auto_insight_engine 模块失败: {e}"}

    q = query.strip().lower()

    if q == "run":
        result = run_cycle()
        return {"ok": True, "action": "run", "result": result}

    if q == "trends":
        trends_path = _SRC / "insight_data" / "trends.json"
        if trends_path.exists():
            data = json.loads(trends_path.read_text(encoding="utf-8"))
            return {"ok": True, "action": "trends", "trends": data}
        return {"ok": True, "action": "trends", "message": "暂无趋势数据"}

    if q == "status" or q == "":
        status = get_engine_status()
        return {"ok": True, "action": "status", "status": status}

    return {"ok": False, "error": f"未知操作: {query}"}


if __name__ == "__main__":
    q = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "status"
    result = run(q)
    print(json.dumps(result, ensure_ascii=False, indent=2))
