"""
continuous_learner.py — 本地化技能: 持续学习编排器
全自动闭环：洞察→知识→趋势→技能生成→报告
"""
import sys, os, json, time
from pathlib import Path

_SRC = Path(__file__).parent.parent.parent / "db"


def run(query: str = "status") -> dict:
    """执行持续学习流水线
    Args:
        query: run [--max N] | status | daemon
    Returns:
        dict: 操作结果
    """
    sys.path.insert(0, str(_SRC))
    try:
        from continuous_learner import run_pipeline, show_status
    except ImportError as e:
        return {"ok": False, "error": f"导入 continuous_learner 模块失败: {e}"}

    q = query.strip().lower()

    if q == "status":
        result = show_status()
        return {"ok": True, "action": "status", "result": result}

    if q == "daemon":
        return {"ok": True, "action": "daemon", "message": "请使用: py continuous_learner.py --mode daemon --interval 60"}

    if q.startswith("run"):
        parts = q.split()
        max_n = 2
        for i, p in enumerate(parts):
            if p == "--max" and i + 1 < len(parts):
                max_n = int(parts[i + 1])
        result = run_pipeline(verbose=False, max_new_skills=max_n)
        return {"ok": True, "action": "run", "result": result}

    return {"ok": False, "error": f"未知操作: {query}"}


if __name__ == "__main__":
    q = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "status"
    result = run(q)
    print(json.dumps(result, ensure_ascii=False, indent=2))
