# -*- coding: utf-8 -*-
"""
曙光 可观测性审计引擎 v1.0 (RagaAI-Inspired Observability)

记录每次策略执行的完整审计追踪：输入数据 -> 推理过程 -> 决策输出 -> 执行结果
================================================================
"""
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

WORKSPACE = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AUDIT_DIR = WORKSPACE / "data" / "audit"


def log(m): print(f"[AUDIT] {m}")


def _safe_path(date_str: str) -> Path:
    p = AUDIT_DIR / date_str
    p.mkdir(parents=True, exist_ok=True)
    return p


def record_decision(
    decision_id: str,
    step: str,
    input_data: Dict,
    reasoning: str,
    output: Dict,
    metadata: Optional[Dict] = None,
):
    """记录一次决策的完整审计追踪"""
    today = datetime.now().strftime("%Y%m%d")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    record = {
        "decision_id": decision_id,
        "timestamp": now,
        "step": step,
        "input": _safe_truncate(input_data),
        "reasoning": reasoning,
        "output": _safe_truncate(output),
        "metadata": metadata or {},
    }
    
    log(f"记录决策: {decision_id} | {step}")
    
    # 写入当月审计文件
    filepath = _safe_path(today) / f"{decision_id}.json"
    filepath.write_text(
        json.dumps(record, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    
    # 更新索引
    index_path = _safe_path(today) / "_index.json"
    index = {}
    if index_path.exists():
        try:
            index = json.loads(index_path.read_text(encoding="utf-8"))
        except:
            pass
    
    entries = index.get("entries", [])
    entries.append({
        "id": decision_id,
        "time": now,
        "step": step,
        "summary": reasoning[:80] if reasoning else "",
    })
    
    if len(entries) > 1000:
        entries = entries[-1000:]
    
    index["entries"] = entries
    index["updated"] = now
    index_path.write_text(
        json.dumps(index, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    
    return record


def _safe_truncate(d: Dict, max_len: int = 2000) -> Dict:
    """截断过大的字段"""
    result = {}
    for k, v in d.items():
        s = json.dumps(v, ensure_ascii=False)
        if len(s) > max_len:
            result[k] = f"[TRUNCATED {len(s)} chars -> first {max_len}] {s[:max_len]}"
        else:
            result[k] = v
    return result


def compare_plan_vs_actual(plan: Dict, actual: Dict) -> Dict:
    """对比计划调仓与实际执行，计算偏差"""
    diff = {
        "matched": [],
        "deviated": [],
        "unplanned": [],
        "missed": [],
    }
    
    plan_actions = {a.get("code", ""): a for a in plan.get("recommendations", [])}
    actual_actions = {a.get("code", ""): a for a in actual.get("actions", [])}
    
    for code, pa in plan_actions.items():
        aa = actual_actions.get(code)
        if not aa:
            diff["missed"].append({"code": code, "plan": pa.get("action")})
        elif pa.get("action") == aa.get("action"):
            diff["matched"].append({"code": code, "action": pa.get("action")})
        else:
            diff["deviated"].append({
                "code": code,
                "plan": pa.get("action"),
                "actual": aa.get("action"),
            })
    
    for code, aa in actual_actions.items():
        if code not in plan_actions:
            diff["unplanned"].append({"code": code, "action": aa.get("action")})
    
    return diff


def get_recent_decisions(days: int = 7) -> List[Dict]:
    """获取近期决策历史"""
    from datetime import timedelta
    
    today = datetime.now()
    results = []
    
    for i in range(days):
        date_str = (today - timedelta(days=i)).strftime("%Y%m%d")
        index_path = AUDIT_DIR / date_str / "_index.json"
        if index_path.exists():
            try:
                index = json.loads(index_path.read_text(encoding="utf-8"))
                results.extend(index.get("entries", []))
            except:
                pass
    
    return sorted(results, key=lambda x: x.get("time", ""), reverse=True)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--recent", type=int, default=7, help="查看最近N天决策记录")
    ap.add_argument("--show", type=str, default="", help="查看指定决策ID详情")
    args = ap.parse_args()
    
    if args.show:
        today = datetime.now().strftime("%Y%m%d")
        fp = AUDIT_DIR / today / f"{args.show}.json"
        if fp.exists():
            print(fp.read_text(encoding="utf-8"))
        else:
            print(f"未找到: {args.show}")
    
    if args.recent:
        entries = get_recent_decisions(args.recent)
        print(f"近{args.recent}天共 {len(entries)} 条决策记录")
        for e in entries[:20]:
            print(f"  {e['time']} | {e['step']:20s} | {e.get('summary', '')[:60]}")
