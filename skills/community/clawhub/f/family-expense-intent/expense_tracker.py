#!/usr/bin/env python3
"""
家庭消费意图识别 V4 - 整合多款优秀技能功能
支持：消费、收入、储蓄目标、订阅、洞察、趋势分析、比价
"""

import json
import os
import re
from datetime import datetime, timedelta
from pathlib import Path
from collections import Counter

# 数据目录
DATA_DIR = Path.home() / ".openclaw" / "skills-data" / "family-expense-intent"
PROFILES_FILE = DATA_DIR / "profiles.json"
CONVERSATIONS_FILE = DATA_DIR / "conversations.json"
INCOME_FILE = DATA_DIR / "income.json"
PATTERNS_FILE = DATA_DIR / "patterns.json"
BUDGETS_FILE = DATA_DIR / "budgets.json"
GOALS_FILE = DATA_DIR / "goals.json"
SUBSCRIPTIONS_FILE = DATA_DIR / "subscriptions.json"

def ensure_data_dir():
    """确保数据目录存在"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    files = {
        PROFILES_FILE: {"members": {}, "default_member": None},
        CONVERSATIONS_FILE: {"conversations": []},
        INCOME_FILE: {"income": []},
        PATTERNS_FILE: {"patterns": {}, "insights": []},
        BUDGETS_FILE: {"budgets": {}, "monthly_total": 10000},
        GOALS_FILE: {"goals": []},
        SUBSCRIPTIONS_FILE: {"subscriptions": []},
    }
    
    for f, default in files.items():
        if not f.exists():
            with open(f, 'w', encoding='utf-8') as fp:
                json.dump(default, fp, ensure_ascii=False, indent=2)

def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def save_json(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ===== NLP 模块 =====
class NLPParser:
    AMOUNT_PATTERNS = [
        r'(\d+(?:\.\d+)?)\s*(?:块|元|块钱|元整)',
        r'花了\s*(\d+(?:\.\d+)?)',
        r'给了\s*(\d+(?:\.\d+)?)',
        r'买了\s*(\d+(?:\.\d+)?)',
        r'充了\s*(\d+(?:\.\d+)?)',
        r'交了\s*(\d+(?:\.\d+)?)',
        r'(\d+(?:\.\d+)?)\s*多',
    ]
    
    CATEGORY_KEYWORDS = {
        "餐饮": ["买菜", "做饭", "吃饭", "外卖", "下馆子", "火锅", "烧烤", "奶茶", "咖啡"],
        "购物": ["买", "网购", "淘宝", "京东", "拼多多", "衣服", "鞋子", "电子产品"],
        "交通": ["打车", "开车", "加油", "公交", "地铁", "停车"],
        "教育": ["学费", "培训班", "补课", "买书", "文具", "课程"],
        "医疗": ["看病", "买药", "体检", "医院", "药店"],
        "娱乐": ["电影", "游戏", "旅游", "健身", "KTV", "Netflix"],
        "通讯": ["话费", "网费", "手机费", "流量"],
        "理财": ["保险", "理财", "基金", "投资"],
        "住房": ["房租", "水电", "物业", "燃气"],
        "人情": ["红包", "礼物", "请客", "随礼"],
    }
    
    INTENT_KEYWORDS = {
        "冲动消费": ["好想买", "好好看", "忍不住", "冲动"],
        "计划消费": ["打算", "准备", "计划"],
        "投资型消费": ["学习", "提升", "培训"],
    }
    
    @classmethod
    def parse_message(cls, message):
        result = {"amount": None, "category": None, "category_confidence": 0, "intent_type": None}
        
        amount = cls.extract_amount(message)
        if amount:
            result["amount"] = amount
        
        category, confidence = cls.extract_category(message)
        if category:
            result["category"] = category
            result["category_confidence"] = confidence
        
        intent_type, _ = cls.extract_intent(message)
        if intent_type:
            result["intent_type"] = intent_type
        
        return result
    
    @classmethod
    def extract_amount(cls, message):
        for pattern in cls.AMOUNT_PATTERNS:
            match = re.search(pattern, message)
            if match:
                try:
                    return float(match.group(1))
                except:
                    pass
        return None
    
    @classmethod
    def extract_category(cls, message):
        best_match, best_confidence = None, 0
        for category, keywords in cls.CATEGORY_KEYWORDS.items():
            count = sum(1 for kw in keywords if kw in message)
            if count > 0:
                confidence = min(count * 30, 95)
                if confidence > best_confidence:
                    best_confidence = confidence
                    best_match = category
        return best_match, best_confidence
    
    @classmethod
    def extract_intent(cls, message):
        best_match, best_strength = None, 0
        for intent, keywords in cls.INTENT_KEYWORDS.items():
            count = sum(1 for kw in keywords if kw in message)
            if count > 0:
                strength = count * 20
                if strength > best_strength:
                    best_strength = strength
                    best_match = intent
        return best_match, min(best_strength, 100)

# ===== 成员管理 =====
def add_member(name, relationship=None):
    ensure_data_dir()
    profiles = load_json(PROFILES_FILE)
    member_id = f"member_{len(profiles.get('members', {})) + 1}"
    profiles['members'][member_id] = {"name": name, "relationship": relationship, "created_at": datetime.now().isoformat()}
    if not profiles.get('default_member'):
        profiles['default_member'] = member_id
    save_json(PROFILES_FILE, profiles)
    return member_id

def get_members():
    return load_json(PROFILES_FILE).get('members', {})

# ===== 消费记录 =====
def add_conversation(member_id, message, amount=None, category=None, use_nlp=True):
    ensure_data_dir()
    if use_nlp and message:
        nlp = NLPParser.parse_message(message)
        amount = amount or nlp.get('amount')
        category = category or nlp.get('category')
    
    conversations = load_json(CONVERSATIONS_FILE)
    record = {
        "id": f"conv_{len(conversations['conversations']) + 1}",
        "member_id": member_id, "message": message, "amount": amount,
        "category": category, "timestamp": datetime.now().isoformat()
    }
    conversations['conversations'].append(record)
    if len(conversations['conversations']) > 1000:
        conversations['conversations'] = conversations['conversations'][-1000:]
    save_json(CONVERSATIONS_FILE, conversations)
    return record

def get_conversations(member_id=None, category=None, days=30, limit=50):
    conversations = load_json(CONVERSATIONS_FILE)['conversations']
    if member_id: conversations = [c for c in conversations if c.get('member_id') == member_id]
    if category: conversations = [c for c in conversations if c.get('category') == category]
    if days:
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()
        conversations = [c for c in conversations if c.get('timestamp', '') >= cutoff]
    return sorted(conversations, key=lambda x: x.get('timestamp', ''), reverse=True)[:limit]

def get_stats(member_id=None, days=30):
    records = get_conversations(member_id, days=days, limit=1000)
    total, count = sum(r.get('amount', 0) or 0 for r in records), len(records)
    cats = {}
    for r in records:
        cat = r.get('category', '其他')
        cats[cat] = cats.get('cat', {"count": 0, "total": 0})
        cats[cat]["count"] += 1
        cats[cat]["total"] += r.get('amount', 0) or 0
    return {"total_amount": total, "total_count": count, "category_stats": cats, "average": total/count if count else 0}

# ===== 收入管理 (V4新增) =====
def add_income(member_id, amount, source, note=None):
    ensure_data_dir()
    income_data = load_json(INCOME_FILE)
    record = {
        "id": f"inc_{len(income_data['income']) + 1}",
        "member_id": member_id, "amount": amount, "source": source,
        "note": note, "timestamp": datetime.now().isoformat()
    }
    income_data['income'].append(record)
    save_json(INCOME_FILE, income_data)
    return record

def get_income(member_id=None, days=30):
    income_data = load_json(INCOME_FILE)['income']
    if member_id: income_data = [i for i in income_data if i.get('member_id') == member_id]
    if days:
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()
        income_data = [i for i in income_data if i.get('timestamp', '') >= cutoff]
    return sorted(income_data, key=lambda x: x.get('timestamp', ''), reverse=True)

# ===== 储蓄目标 (V4新增) =====
def add_goal(name, target, deadline=None, priority="normal"):
    ensure_data_dir()
    goals_data = load_json(GOALS_FILE)
    goal = {
        "id": f"goal_{len(goals_data['goals']) + 1}",
        "name": name, "target": target, "current": 0,
        "deadline": deadline, "priority": priority,
        "created_at": datetime.now().isoformat()
    }
    goals_data['goals'].append(goal)
    save_json(GOALS_FILE, goals_data)
    return goal

def contribute_goal(goal_name, amount):
    goals_data = load_json(GOALS_FILE)
    for g in goals_data['goals']:
        if g['name'] == goal_name:
            g['current'] = g.get('current', 0) + amount
            save_json(GOALS_FILE, goals_data)
            return g
    return None

def get_goals():
    return load_json(GOALS_FILE).get('goals', [])

def goal_progress():
    goals = get_goals()
    result = []
    for g in goals:
        pct = (g.get('current', 0) / g['target'] * 100) if g['target'] else 0
        result.append({
            "name": g['name'], "target": g['target'], "current": g.get('current', 0),
            "percentage": round(pct, 1), "remaining": g['target'] - g.get('current', 0)
        })
    return result

# ===== 订阅管理 (V4新增) =====
def add_subscription(member_id, name, amount, category, frequency="monthly"):
    ensure_data_dir()
    subs_data = load_json(SUBSCRIPTIONS_FILE)
    sub = {
        "id": f"sub_{len(subs_data['subscriptions']) + 1}",
        "member_id": member_id, "name": name, "amount": amount,
        "category": category, "frequency": frequency,
        "created_at": datetime.now().isoformat()
    }
    subs_data['subscriptions'].append(sub)
    save_json(SUBSCRIPTIONS_FILE, subs_data)
    return sub

def get_subscriptions():
    return load_json(SUBSCRIPTIONS_FILE).get('subscriptions', [])

def subscription_total():
    subs = get_subscriptions()
    total = sum(s.get('amount', 0) for s in subs)
    return {"count": len(subs), "monthly_total": total}

# ===== 预算管理 =====
def set_budget(category, amount):
    budgets = load_json(BUDGETS_FILE)
    budgets['budgets'][category] = amount
    save_json(BUDGETS_FILE, budgets)

def get_budgets():
    return load_json(BUDGETS_FILE).get('budgets', {})

def check_budget(category):
    budgets = load_json(BUDGETS_FILE).get('budgets', {})
    if category not in budgets:
        return None
    budget = budgets[category]
    # 获取该类别的消费
    conversations = load_json(CONVERSATIONS_FILE)['conversations']
    this_month = datetime.now().strftime("%Y-%m")
    records = [c for c in conversations if c.get('category') == category and c.get('timestamp', '').startswith(this_month)]
    used = sum(r.get('amount', 0) or 0 for r in records)
    return {"budget": budget, "used": used, "remaining": budget-used, "percentage": (used/budget*100) if budget else 0}

def budget_alerts():
    budgets = get_budgets()
    alerts = []
    for cat, amount in budgets.items():
        status = check_budget(cat)
        if status and status['percentage'] >= 100:
            alerts.append(f"⚠️ {cat}超预算 {status['percentage']:.0f}%")
        elif status and status['percentage'] >= 80:
            alerts.append(f"⚡ {cat}即将超预算 {status['percentage']:.0f}%")
    return alerts if alerts else ["✅ 所有预算正常"]

# ===== 消费洞察 (V4新增) =====
def generate_insights(member_id=None):
    insights = []
    
    # 超预算提醒
    for alert in budget_alerts():
        insights.append(alert)
    
    # 消费频率分析
    stats = get_stats(member_id)
    if stats['total_count'] > 0:
        avg = stats['average']
        if avg > 5000:
            insights.append(f"⚠️ 月均消费较高，约¥{avg:.0f}")
        elif avg < 1000:
            insights.append(f"💡 消费控制良好，月均仅¥{avg:.0f}")
    
    # 类别分析
    cats = stats.get('category_stats', {})
    if cats:
        top_cat = max(cats.items(), key=lambda x: x[1]['total'])
        insights.append(f"📊 主要支出: {top_cat[0]} ¥{top_cat[1]['total']}")
    
    return insights if insights else ["数据不足，请记录更多消费"]

def compare_months():
    # 简化版月度对比
    current = get_stats(days=30)
    last_month = get_stats(days=60)
    
    change = ((current['total_amount'] - last_month['total_amount']) / last_month['total_amount'] * 100) if last_month['total_amount'] else 0
    
    direction = "↑" if change > 0 else "↓"
    return f"本月 vs 上月: {abs(change):.1f}% {direction}"

# ===== 趋势分析 (V4新增) =====
def trends(months=6):
    result = []
    for i in range(months):
        days_ago = i * 30
        stats = get_stats(days=days_ago)
        month_name = (datetime.now() - timedelta(days=days_ago)).strftime("%m月")
        result.append(f"{month_name}: ¥{stats['total_amount']:.0f}")
    return "\n".join(reversed(result))

# ===== 购物比价 (V4新增) =====
def compare_product(keyword, source="taobao"):
    """模拟比价功能 - 实际需要调用外部API"""
    # 这里返回模拟数据，实际应该调用淘宝/京东API
    demo_data = {
        "taobao": {"price": 299, "discount": "无"},
        "jd": {"price": 299, "discount": "满减20"},
        "pinduoduo": {"price": 279, "discount": "百亿补贴"}
    }
    
    result = f"🛒 {keyword} 比价结果:\n"
    result += "┌─────────────┬────────┬──────────┐\n"
    result += "│ 平台       │ 价格   │ 优惠    │\n"
    result += "├─────────────┼────────┼──────────┤\n"
    
    for platform, info in demo_data.items():
        result += f"│ {platform:<11} │ ¥{info['price']:<5} │ {info['discount']:<8} │\n"
    
    result += "└─────────────┴────────┴──────────┘\n"
    result += f"💡 推荐: 拼多多 ¥279 (最便宜)"
    
    return result

# ===== 月度报告 =====
def monthly_report():
    stats = get_stats()
    income_records = get_income(days=30)
    total_income = sum(i.get('amount', 0) for i in income_records)
    subs_total = subscription_total()
    goals = goal_progress()
    alerts = budget_alerts()
    
    result = f"""
═══════════════════════════════════════
     {datetime.now().strftime('%Y年%m月')} 家庭消费报告
═══════════════════════════════════════

💰 收入: ¥{total_income:,.0f}
💸 支出: ¥{stats['total_amount']:,.0f}
💵 结余: ¥{total_income - stats['total_amount']:,.0f} ({(total_income - stats['total_amount'])/total_income*100:.0f}%)

📊 支出明细:
"""
    for cat, data in stats.get('category_stats', {}).items():
        budget = get_budgets().get(cat, 0)
        budget_str = f"[预算¥{budget:,}]" if budget else ""
        over = "⚠️" if budget and data['total'] > budget else ""
        result += f"  {cat}: ¥{data['total']:,.0f} ({data['count']}次) {budget_str} {over}\n"
    
    result += f"\n📈 趋势: {compare_months()}\n"
    
    if subs_total['count'] > 0:
        result += f"\n🔄 订阅: {subs_total['count']}个, 月均¥{subs_total['monthly_total']}\n"
    
    if goals:
        result += "\n🎯 储蓄目标:\n"
        for g in goals:
            result += f"  {g['name']}: ¥{g['current']:,.0f}/¥{g['target']:,.0f} ({g['percentage']}%)\n"
    
    if alerts:
        result += f"\n⚠️ 提醒: {', '.join(alerts)}\n"
    
    return result

# ===== CLI 接口 =====
def main():
    import sys
    ensure_data_dir()
    
    if len(sys.argv) < 2:
        print("用法: python expense_tracker.py <命令> [参数]")
        print("\n命令:")
        print("  add-member <名字> [关系]")
        print("  list-members")
        print("  add-conv <member_id> <消息> [--amount N] [--category X]")
        print("  add-income <member_id> <金额> <来源>")
        print("  get-income [--member X]")
        print("  add-goal <目标名> <金额> [--deadline 日期] [--priority high/normal]")
        print("  contribute-goal <目标名> <金额>")
        print("  goals")
        print("  goal-progress")
        print("  add-subscription <member_id> <名称> <金额> <类别> [frequency]")
        print("  subscriptions")
        print("  set-budget <类别> <金额>")
        print("  budgets")
        print("  check-budget <类别>")
        print("  budget-alerts")
        print("  insights")
        print("  compare-months")
        print("  trends [月数]")
        print("  compare <商品关键词>")
        print("  monthly-report")
        return
    
    cmd = sys.argv[1]
    
    if cmd == "add-member" and len(sys.argv) > 2:
        rel = sys.argv[3] if len(sys.argv) > 3 else None
        print(add_member(sys.argv[2], rel))
    
    elif cmd == "list-members":
        for mid, m in get_members().items():
            print(f"{mid}: {m['name']} ({m.get('relationship', '')})")
    
    elif cmd == "add-conv" and len(sys.argv) > 3:
        member_id = sys.argv[2]
        message = ' '.join(sys.argv[3:])
        amount, category = None, None
        for i, a in enumerate(sys.argv):
            if a == "--amount" and i+1 < len(sys.argv):
                amount = float(sys.argv[i+1])
            if a == "--category" and i+1 < len(sys.argv):
                category = sys.argv[i+1]
        print(json.dumps(add_conversation(member_id, message, amount, category), ensure_ascii=False, indent=2))
    
    elif cmd == "add-income" and len(sys.argv) > 4:
        member_id, amount, source = sys.argv[2], float(sys.argv[3]), sys.argv[4]
        print(json.dumps(add_income(member_id, amount, source), ensure_ascii=False, indent=2))
    
    elif cmd == "get-income":
        member_id = None
        for i, a in enumerate(sys.argv):
            if a == "--member" and i+1 < len(sys.argv):
                member_id = sys.argv[i+1]
        for i in get_income(member_id):
            print(f"[{i['timestamp'][:10]}] {i.get('source')}: ¥{i.get('amount')}")
    
    elif cmd == "add-goal" and len(sys.argv) > 3:
        name, target = sys.argv[2], float(sys.argv[3])
        deadline, priority = None, "normal"
        for i, a in enumerate(sys.argv):
            if a == "--deadline" and i+1 < len(sys.argv):
                deadline = sys.argv[i+1]
            if a == "--priority" and i+1 < len(sys.argv):
                priority = sys.argv[i+1]
        print(json.dumps(add_goal(name, target, deadline, priority), ensure_ascii=False, indent=2))
    
    elif cmd == "contribute-goal" and len(sys.argv) > 3:
        print(json.dumps(contribute_goal(sys.argv[2], float(sys.argv[3])), ensure_ascii=False, indent=2))
    
    elif cmd == "goals":
        print(json.dumps(get_goals(), ensure_ascii=False, indent=2))
    
    elif cmd == "goal-progress":
        for g in goal_progress():
            bar = "█" * int(g['percentage']/10) + "░" * (10 - int(g['percentage']/10))
            print(f"{g['name']}: {bar} {g['percentage']}% (¥{g['current']}/¥{g['target']})")
    
    elif cmd == "add-subscription" and len(sys.argv) > 5:
        member_id, name, amount, category = sys.argv[2], sys.argv[3], float(sys.argv[4]), sys.argv[5]
        freq = sys.argv[6] if len(sys.argv) > 6 else "monthly"
        print(json.dumps(add_subscription(member_id, name, amount, category, freq), ensure_ascii=False, indent=2))
    
    elif cmd == "subscriptions":
        print(json.dumps(get_subscriptions(), ensure_ascii=False, indent=2))
    
    elif cmd == "set-budget" and len(sys.argv) > 3:
        set_budget(sys.argv[2], float(sys.argv[3]))
        print(f"✅ 已设置 {sys.argv[2]} 预算: ¥{sys.argv[3]}")
    
    elif cmd == "budgets":
        print(json.dumps(get_budgets(), ensure_ascii=False, indent=2))
    
    elif cmd == "check-budget" and len(sys.argv) > 2:
        print(json.dumps(check_budget(sys.argv[2]), ensure_ascii=False, indent=2))
    
    elif cmd == "budget-alerts":
        for a in budget_alerts():
            print(a)
    
    elif cmd == "insights":
        for i in generate_insights():
            print(i)
    
    elif cmd == "compare-months":
        print(compare_months())
    
    elif cmd == "trends":
        months = int(sys.argv[2]) if len(sys.argv) > 2 else 6
        print(trends(months))
    
    elif cmd == "compare" and len(sys.argv) > 2:
        print(compare_product(' '.join(sys.argv[2:])))
    
    elif cmd == "monthly-report":
        print(monthly_report())
    
    elif cmd == "stats":
        member_id = None
        for i, a in enumerate(sys.argv):
            if a == "--member" and i+1 < len(sys.argv):
                member_id = sys.argv[i+1]
        print(json.dumps(get_stats(member_id), ensure_ascii=False, indent=2))
    
    elif cmd == "get-convs":
        member_id, category, days = None, None, 30
        for i, a in enumerate(sys.argv):
            if a == "--member" and i+1 < len(sys.argv): member_id = sys.argv[i+1]
            if a == "--category" and i+1 < len(sys.argv): category = sys.argv[i+1]
            if a == "--days" and i+1 < len(sys.argv): days = int(sys.argv[i+1])
        for c in get_conversations(member_id, category, days):
            print(f"[{c['timestamp'][:10]}] {c.get('category')}: ¥{c.get('amount', 0)} - {c.get('message', '')[:40]}")

if __name__ == "__main__":
    main()
