# -*- coding: utf-8 -*-
"""
曙光 自进化反射引擎 v1.0 (Hermes-Inspired Self-Improving Loop)

每次策略执行后调用，自动反思决策质量、提取教训、更新学习档案。
下次执行前加载历史教训，注入决策上下文。
================================================================
"""
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

WORKSPACE = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LEARNINGS_DIR = WORKSPACE / ".learnings"
STATE_FILE = WORKSPACE / "session-state.json"


def log(m): print(f"[REFLECT] {m}")
def warn(m): print(f"[WARN] {m}")
def err(m): print(f"[ERROR] {m}")


def load_json(p):
    if p.exists():
        try: return json.loads(p.read_text(encoding="utf-8"))
        except: return None
    return None


def save_json(p, d):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")


# ── 学习记录格式 ──────────────────────────────────────────────

def load_learnings(max_items=10) -> List[Dict]:
    """加载最近的反思记录，用于注入策略prompt"""
    file = LEARNINGS_DIR / "REFLECTIONS.json"
    all_items = load_json(file) or []
    return all_items[-max_items:]


def save_reflection(reflection: Dict):
    """保存一条反思记录"""
    file = LEARNINGS_DIR / "REFLECTIONS.json"
    all_items = load_json(file) or []
    all_items.append(reflection)
    # 最多保留200条
    if len(all_items) > 200:
        all_items = all_items[-200:]
    save_json(file, all_items)
    log(f"已保存反思 #{len(all_items)}")


def load_lessons_for_prompt() -> str:
    """生成可注入到prompt的教训摘要"""
    reflections = load_learnings(10)
    if not reflections:
        return ""
    
    lines = ["\n## 【自进化引擎】历史反思摘要"]
    
    # 提取连续失败的教训
    failures = [r for r in reflections[-5:] if r.get("score", 0) < 0]
    if failures:
        lines.append("\n⚠️ 近期失败教训：")
        seen = set()
        for r in failures:
            for lesson in r.get("lessons", []):
                key = lesson[:30]
                if key not in seen:
                    seen.add(key)
                    lines.append(f"  - {lesson}")
    
    # 提取成功经验
    successes = [r for r in reflections[-5:] if r.get("score", 0) > 0]
    if successes:
        lines.append("\n✅ 近期成功经验：")
        seen = set()
        for r in successes:
            for lesson in r.get("lessons", []):
                key = lesson[:30]
                if key not in seen:
                    seen.add(key)
                    lines.append(f"  - {lesson}")
    
    # 失败模式统计
    pattern_counts = {}
    for r in reflections[-50:]:
        for p in r.get("patterns", []):
            pattern_counts[p] = pattern_counts.get(p, 0) + 1
    
    repeat_offenders = {k: v for k, v in pattern_counts.items() if v >= 3}
    if repeat_offenders:
        lines.append("\n🔁 反复出现的模式（≥3次）：")
        for p, c in sorted(repeat_offenders.items(), key=lambda x: -x[1]):
            lines.append(f"  - {p} (出现{c}次)")
    
    return "\n".join(lines)


# ── 反思引擎核心 ──────────────────────────────────────────────

def reflect(
    strategy_name: str,
    before_state: Dict,
    after_state: Dict,
    actions_taken: List[Dict],
    market_context: Dict,
    expected_outcome: Optional[str] = None,
) -> Dict:
    """
    对一次策略执行进行反思，返回反思记录。
    
    参数：
    - strategy_name: 策略名称
    - before_state: 执行前的持仓/资产状态
    - after_state: 执行后的持仓/资产状态
    - actions_taken: 执行的操作列表 [{"code","action","reason","result"}]
    - market_context: 市场环境上下文
    - expected_outcome: 预期结果（可选）
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # 计算执行结果
    before_val = before_state.get("total_assets", 0) or 0
    after_val = after_state.get("total_assets", 0) or 0
    pnl = after_val - before_val
    pnl_pct = (pnl / before_val * 100) if before_val else 0
    
    # 评分：-2 到 +2
    score = 0
    if pnl_pct > 0.5:
        score = 2
    elif pnl_pct > 0:
        score = 1
    elif pnl_pct > -0.5:
        score = 0
    elif pnl_pct > -1:
        score = -1
    else:
        score = -2
    
    # 分析各操作的结果
    action_results = []
    lessons = []
    patterns = []
    
    for action in actions_taken:
        code = action.get("code", "")
        act = action.get("action", "")
        reason = action.get("reason", "")
        result = action.get("result", "")
        
        ar = {"code": code, "action": act, "reason": reason, "result": result}
        action_results.append(ar)
        
        # 教训提取
        if "亏损" in result or "-3%" in result or "-4%" in result:
            lessons.append(f"{code} {act}: {reason} 导致亏损 {result}，下次需谨慎")
            patterns.append(f"亏损持仓未及时减仓")
        elif "盈利" in result or "+2%" in result or "+3%" in result:
            lessons.append(f"{code} {act}: {reason} 有效，盈利 {result}，可重复此模式")
            patterns.append(f"有效止盈/加仓")
        elif "未成交" in result:
            lessons.append(f"{code} {act}: 未成交（{reason}），检查流动性/价格")
            patterns.append(f"订单未成交")
    
    # 提取通用教训
    if before_val > 0 and pnl < 0:
        lessons.append(f"策略期间总亏损 {pnl:+.0f} ({pnl_pct:+.2f}%)，需检查仓位控制")
        patterns.append("策略期整体亏损")
    elif before_val > 0 and pnl > 0:
        lessons.append(f"策略期间总盈利 {pnl:+.0f} ({pnl_pct:+.2f}%)，策略有效")
        patterns.append("策略期整体盈利")
    
    if len(lessons) > 5:
        lessons = lessons[:5]
    
    reflection = {
        "timestamp": now,
        "strategy": strategy_name,
        "market": market_context.get("bias", "unknown"),
        "score": score,
        "pnl": round(pnl, 2),
        "pnl_pct": round(pnl_pct, 2),
        "before_assets": before_val,
        "after_assets": after_val,
        "actions": action_results,
        "lessons": lessons,
        "patterns": list(set(patterns)),
        "expected": expected_outcome or "",
    }
    
    save_reflection(reflection)
    return reflection


# ── 独立运行入口 ──────────────────────────────────────────────

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="曙光自进化反射引擎")
    ap.add_argument("--reflect", action="store_true", help="执行反思（从session-state.json读取前后状态）")
    ap.add_argument("--lessons", action="store_true", help="输出历史教训摘要")
    args = ap.parse_args()
    
    if args.lessons:
        print(load_lessons_for_prompt())
    
    if args.reflect:
        state = load_json(STATE_FILE) or {}
        
        before = state.get("_reflect_before", {})
        after = state.get("holdings", {}).copy()
        after["total_assets"] = state.get("last_known_assets", 0)
        
        reflection = reflect(
            strategy_name=state.get("strategy", "曙光ETF轮动调仓系统"),
            before_state=before,
            after_state=state,
            actions_taken=state.get("_actions_taken", []),
            market_context=state.get("_market_context", {}),
        )
        
        print(json.dumps(reflection, ensure_ascii=False, indent=2))
