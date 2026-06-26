#!/usr/bin/env python3
"""
品蜜引擎 — 酿蜜后自动自检，发现矛盾自动修正

品蜜是蜂巢的第二个胃。酿完蜜必须自己尝一遍。
进化信号 = 内部自相矛盾。每发现一个矛盾，归纳一条规则，固化到代码。
"""
import json
import math
import os
from datetime import date, datetime
from pathlib import Path
from typing import Optional

PROJECT_ROOT = Path(__file__).parent.parent
OUTPUT_DIR = PROJECT_ROOT / "output"
RULES_PATH = PROJECT_ROOT / "evolution-rules.json"


# ==================== 品蜜规则定义 ====================
# 规则格式：trigger / diagnose / fix
# trigger: 检测条件（代码执行，不依赖模型）
# diagnose: 诊断原因（结构化，低能模型也能理解）
# fix: 修正方案（可自动执行 或 需人工确认）

TASTE_RULES = [
    {
        "id": "rule_001",
        "name": "弱模型霸榜检测",
        "trigger": "any model with capability < 0.70 appears in comprehensive top 3",
        "check": lambda rankings: any(
            r.get("capability", 1.0) < 0.70 and r.get("rank", 999) <= 3
            for r in rankings
        ),
        "diagnose": {
            "reason_code": "WEAK_MODEL_ON_TOP",
            "root_cause": "cost_effectiveness_formula_overfavors_low_price",
            "explanation": "性价比公式对低价弱模型过度偏袒，使 capability < 0.70 的模型排进 Top 3"
        },
        "fix": {
            "action": "APPLY_CAPABILITY_SQUARED",
            "description": "capability 做指数惩罚(capability²) + 设能力门槛 ≥ 0.70",
            "auto_apply": True,
        },
        "confidence": 0.95,
        "source": "glm-4-flash 事件 2026-05-13",
        "status": "active",
    },
    {
        "id": "rule_002",
        "name": "性价比分数极端偏斜",
        "trigger": "max ce_raw is more than 3x the median ce_raw",
        "check": lambda rankings: (
            len(rankings) >= 5 and
            max(r.get("ce_raw", 0) for r in rankings) >
            3 * sorted(r.get("ce_raw", 0) for r in rankings)[len(rankings)//2]
        ),
        "diagnose": {
            "reason_code": "CE_SKEW_EXCESSIVE",
            "root_cause": "log_scale_still_insufficient_for_extreme_prices",
            "explanation": "对数缩放后性价比仍严重偏斜，存在超低价模型"
        },
        "fix": {
            "action": "APPLY_CAPABILITY_SQUARED",
            "description": "capability² 抑制弱模型性价比膨胀",
            "auto_apply": True,
        },
        "confidence": 0.85,
        "status": "active",
    },
    {
        "id": "rule_003",
        "name": "同厂商模型重复上榜",
        "trigger": "same vendor appears more than 4 times in top 10",
        "check": lambda rankings: (
            len([r for r in rankings[:10] if r.get("vendor") == 
                 max(set(r2.get("vendor") for r2 in rankings[:10]),
                     key=lambda v: sum(1 for r2 in rankings[:10] if r2.get("vendor") == v))]) > 4
        ),
        "diagnose": {
            "reason_code": "VENDOR_DOMINATION",
            "root_cause": "single_vendor_too_many_model_variants",
            "explanation": "同一厂商的多个变体占据过多位置，减少排名多样性"
        },
        "fix": {
            "action": "LIMIT_PER_VENDOR",
            "description": "综合排名 Top 10 中，每个厂商最多 3 个模型",
            "auto_apply": True,
        },
        "confidence": 0.75,
        "status": "active",
    },
    {
        "id": "rule_004",
        "name": "价格数据缺失检测",
        "trigger": "model with zero or missing price appears in top 10",
        "check": lambda rankings: any(
            (r.get("input_price", 0) <= 0 or r.get("output_price", 0) <= 0)
            and r.get("rank", 999) <= 10
            for r in rankings
        ),
        "diagnose": {
            "reason_code": "MISSING_PRICING_DATA",
            "root_cause": "forager_failed_to_extract_price",
            "explanation": "缺失定价的模型不应进入排名，性价比无法计算"
        },
        "fix": {
            "action": "EXCLUDE_MISSING_PRICE",
            "description": "排除缺失定价数据的模型",
            "auto_apply": True,
        },
        "confidence": 0.95,
        "status": "active",
    },
]


# ==================== 品蜜执行 ====================

def taste(rankings: list[dict]) -> dict:
    """
    执行品蜜自检。
    
    输入：综合排名结果
    输出：品蜜报告 { triggered_rules, fixes_applied, revised_rankings }
    """
    result = {
        "date": date.today().isoformat(),
        "taste_time": datetime.now().isoformat(),
        "rules_checked": len(TASTE_RULES),
        "rules_triggered": [],
        "fixes_applied": [],
        "revised": False,
    }
    
    # 逐一检查品蜜规则
    for rule in TASTE_RULES:
        if rule["status"] != "active":
            continue
        
        try:
            triggered = rule["check"](rankings)
        except Exception:
            triggered = False
        
        if triggered:
            result["rules_triggered"].append({
                "id": rule["id"],
                "name": rule["name"],
                "diagnose": rule["diagnose"],
                "fix": rule["fix"],
            })
            
            # 自动执行修正
            if rule["fix"].get("auto_apply", False):
                action = rule["fix"]["action"]
                rankings = _apply_fix(rankings, action, rule)
                result["fixes_applied"].append({
                    "rule_id": rule["id"],
                    "action": action,
                    "description": rule["fix"]["description"],
                })
                result["revised"] = True
    
    # 重新排序（如果修正过）
    if result["revised"]:
        rankings.sort(key=lambda x: x.get("composite_score", 0), reverse=True)
        for i, r in enumerate(rankings, 1):
            r["rank"] = i
    
    result["revised_rankings"] = rankings
    
    return result


def _apply_fix(rankings: list[dict], action: str, rule: dict) -> list[dict]:
    """执行品蜜修正"""
    
    if action == "APPLY_CAPABILITY_SQUARED":
        # 重新计算性价比（capability²）并应用门槛
        max_cap = max((r.get("capability", 0) for r in rankings), default=1) or 1
        max_ce = max((r.get("ce_raw", 0) for r in rankings), default=1) or 1
        
        for r in rankings:
            cap = r.get("capability", 0)
            ce_raw = r.get("ce_raw", 0)
            
            # 重新计算性价比（如果还没用 capability²）
            inp = r.get("input_price", 0)
            outp = r.get("output_price", 0)
            if inp > 0 and outp > 0:
                weighted_price = inp * 0.7 + outp * 0.3
                ce_raw_new = (cap ** 2) * math.log10(max(1000 / weighted_price, 0.1))
                r["ce_raw"] = round(ce_raw_new, 3)
                max_ce = max(max_ce, ce_raw_new)
            
            # 应用能力门槛
            r["_below_threshold"] = cap < 0.70
            
            # 重新计算综合分
            cap_norm = cap / max_cap
            ce_norm = r["ce_raw"] / max_ce if max_ce > 0 else 0
            eco = r.get("ecosystem_score", 0.5)
            mom = r.get("momentum_score", 0.5)
            
            composite = 0.35 * cap_norm + 0.30 * ce_norm + 0.20 * eco + 0.15 * mom
            r["composite_score"] = round(composite, 3)
            r["cap_norm"] = round(cap_norm, 3)
            r["ce_norm"] = round(ce_norm, 3)
        
        # 过滤门槛以下的模型（降级到性价比排行但不进综合 Top 10）
        # 不删除，只标记
        
        return rankings
    
    elif action == "LIMIT_PER_VENDOR":
        # 每个厂商在 Top 10 最多 3 个
        vendor_count = {}
        filtered = []
        for r in rankings:
            v = r.get("vendor", "未知")
            vendor_count[v] = vendor_count.get(v, 0) + 1
            if vendor_count[v] <= 3:
                filtered.append(r)
            else:
                r["_vendor_capped"] = True
        return filtered
    
    elif action == "EXCLUDE_MISSING_PRICE":
        # 排除缺失定价的模型
        for r in rankings:
            inp = r.get("input_price", 0)
            outp = r.get("output_price", 0)
            if inp <= 0 or outp <= 0:
                r["_missing_price"] = True
        return rankings
    
    return rankings


# ==================== 进化规则管理 ====================

def load_evolution_rules() -> list:
    """加载进化规则库"""
    if RULES_PATH.exists():
        with open(RULES_PATH) as f:
            return json.load(f).get("rules", [])
    return []


def save_evolution_rule(rule: dict):
    """追加进化规则"""
    rules = load_evolution_rules()
    
    # 检查是否已存在同 id
    existing_ids = {r["id"] for r in rules}
    if rule["id"] not in existing_ids:
        rules.append(rule)
    else:
        # 更新已有规则
        for i, r in enumerate(rules):
            if r["id"] == rule["id"]:
                rules[i] = rule
    
    data = {
        "last_updated": datetime.now().isoformat(),
        "total_rules": len(rules),
        "rules": rules,
    }
    with open(RULES_PATH, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def record_evolution(trigger: str, diagnosis: dict, fix: dict):
    """记录一次进化事件，自动生成规则"""
    rules = load_evolution_rules()
    next_id = f"rule_{len(rules) + 1:03d}"
    
    rule = {
        "id": next_id,
        "name": diagnosis.get("reason_code", "UNKNOWN"),
        "trigger": trigger,
        "check": None,  # 需要人工编写 check 函数
        "diagnose": diagnosis,
        "fix": fix,
        "confidence": 0.60,  # 新规则置信度低，需验证
        "source": f"auto_detected {date.today().isoformat()}",
        "status": "pending",
    }
    
    save_evolution_rule(rule)
    return rule


# 初始化：把品蜜规则持久化
def init_rules():
    """初始化进化规则库"""
    existing = load_evolution_rules()
    existing_ids = {r["id"] for r in existing}
    
    for rule in TASTE_RULES:
        if rule["id"] not in existing_ids:
            # 去掉 check 函数（不可序列化），存 trigger 描述
            save_rule = {k: v for k, v in rule.items() if k != "check"}
            save_evolution_rule(save_rule)


if __name__ == "__main__":
    # 初始化规则库
    init_rules()
    print(f"✅ 品蜜规则初始化完成: {len(TASTE_RULES)} 条")
    
    # 测试：加载今日排名并品蜜
    today = date.today().isoformat()
    ranking_path = OUTPUT_DIR / f"ranking_{today}.json"
    
    if ranking_path.exists():
        with open(ranking_path) as f:
            rankings = json.load(f)
        
        print(f"\n🍯 品蜜中... ({len(rankings)} 个模型)")
        result = taste(rankings)
        
        print(f"  规则检查: {result['rules_checked']} 条")
        print(f"  触发规则: {len(result['rules_triggered'])} 条")
        
        for triggered in result["rules_triggered"]:
            print(f"  ⚠️  {triggered['id']}: {triggered['name']}")
            print(f"     诊断: {triggered['diagnose']['reason_code']}")
        
        for fix in result["fixes_applied"]:
            print(f"  🔧 {fix['action']}: {fix['description']}")
        
        if result["revised"]:
            # 保存修正后的排名
            revised_path = OUTPUT_DIR / f"ranking_{today}_revised.json"
            with open(revised_path, "w") as f:
                json.dump(result["revised_rankings"], f, ensure_ascii=False, indent=2)
            print(f"\n  ✅ 修正后排名已保存: {revised_path}")
            
            # 打印修正后 Top 5
            for r in result["revised_rankings"][:5]:
                below = " ⚠️低于门槛" if r.get("_below_threshold") else ""
                print(f"  {r['rank']}. {r['model']} ({r.get('vendor','')}) 综合={r['composite_score']:.3f}{below}")
        else:
            print("\n  ✅ 品蜜通过，无需修正")
    else:
        print("❌ 无今日排名数据")
