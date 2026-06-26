#!/usr/bin/env python3
"""
DigitalSalesClaw - ask.py
通用问答 → 意图识别 → 路由到对应模块

升级：
- 多意图检测（同一问题可能涉及多个模块）
- 置信度返回（无法判断时明确说明，而非猜一个意图）
- 上下文记忆（同类问题连续问时复用上次筛选条件）
- 平台自动识别（从问题语义推断 platform 参数）
"""

import sys
import json
import re
from datetime import datetime
from db import query_all, query_one

SKILL_DIR = "/Users/dc/.openclaw/workspace/skills/digitalsalesclaw"

# ─────────────────────────────────────────
# 同义词标准化
# ─────────────────────────────────────────

SYNONYMS = {
    "KOL": "医生",
    "关键意见领袖": "医生",
    "关键意见医生": "医生",
    "学术推广": "医生触达",
    "医师": "医生",
    "OTC": "药品",
    "仿制药": "药品",
    "创新药": "药品",
    "DTP": "药房",
    "药店": "药房",
    "库存不足": "库存低",
    "缺货": "库存低",
    "断货": "库存低",
}

def normalize_question(question: str) -> str:
    result = question
    for synonym, canonical in SYNONYMS.items():
        if synonym in result:
            result = result.replace(synonym, canonical)
    return result

# ─────────────────────────────────────────
# 意图模式定义（带权重）
# ─────────────────────────────────────────

INTENT_PATTERNS = [
    ("content",    ["选题", "内容创作", "内容生成", "创作内容", "帮我生成", "帮我写", "写文章", "写文案",
                     "发笔记", "生成脚本", "帮我创作", "帮我写一篇", "短视频", "发什么内容", "发什么好"],
                     1.0),
    ("hook",      ["钩子", "开头钩子", "抓人开头", "吸引眼球"], 0.9),
    ("optimize",  ["内容优化", "标题优化", "优化标题", "优化一下", "怎么改"], 0.9),
    ("compliance", ["合规", "违禁词", "违规", "审查", "广告法", "药品管理法", "检查文案",
                     "有没有违规", "这条文案能不能发", "帮我看看这条文案", "这句话有没有违规",
                     "能不能发", "有无风险"], 1.0),
    ("patient",   ["患者", "依从性", "随访", "分群", "患者管理", "旅程", "随访计划", "患者会话"], 1.0),
    ("pharmacy",  ["库存", "补货", "药房", "库存低", "库存不足", "断货", "缺货"], 1.0),
    ("competitor",["竞品", "竞争对手", "市场份额", "价格对比", "市场监控", "竞品分析", "其他药企"], 1.0),
    ("doctor",    ["医生", "拜访", "医生触达", "医生关系", "KOL", "学术会议", "医生档案"], 1.0),
    ("analytics", ["数据", "报表", "KPI", "运营概览", "数据分析", "运营报表", "互动率", "曝光量",
                     "点击率", "转化", "ROI", "效果分析"], 1.0),
    ("knowledge", ["知识库", "法规", "指南", "药品信息", "药品说明", "临床指南", "怎么合规"], 0.8),
]

# ─────────────────────────────────────────
# 上下文记忆（跨请求保持）
# ─────────────────────────────────────────

_context_store = {
    "last_intent": None,
    "last_filters": {},
    "last_module": None,
    "last_updated": None,
}

CONTEXT_TTL_SECONDS = 300  # 5分钟内有效

def _get_cached_context():
    """获取上下文记忆（如果未过期）"""
    if _context_store["last_updated"] is None:
        return None
    elapsed = (datetime.now() - _context_store["last_updated"]).total_seconds()
    if elapsed > CONTEXT_TTL_SECONDS:
        return None
    return _context_store

def _set_cached_context(intent, module, filters):
    """更新上下文记忆"""
    _context_store["last_intent"] = intent
    _context_store["last_module"] = module
    _context_store["last_filters"] = filters
    _context_store["last_updated"] = datetime.now()

# ─────────────────────────────────────────
# 过滤器定义
# ─────────────────────────────────────────

KNOWN_FILTERS = {
    "platform": ["douyin", "xiaohongshu", "wechat", "weibo", "bilibili"],
    "status": ["pending", "approved", "published", "draft", "rejected", "archived"],
    "priority": ["high", "medium", "low", "urgent"],
    "format": ["video", "article", "image", "story"],
    "risk_level": ["critical", "high", "medium", "low"],
    "action_level": ["critical", "high", "medium", "low"],
    "review_stage": ["ai_precheck", "human_review", "approved", "rejected"],
    "segment": ["high_risk", "medium_risk", "low_risk", "active", "resolved", "pending"],
    "role": ["user", "assistant", "system"],
    "product_status": ["ok", "low", "out", "overstocked"],
    "visit_type": ["first", "follow_up", "academic", "detail"],
    "result": ["success", "pending", "cancelled", "rescheduled"],
    "level": ["national", "provincial", "regional"],
    "period": ["7d", "14d", "30d", "90d"],
    "model": ["first_touch", "last_touch", "linear", "time_decay", "position_based", "data_driven"],
}

# ─────────────────────────────────────────
# 多意图检测（v2 核心升级）
# ─────────────────────────────────────────

def detect_intents(question: str) -> list[dict]:
    """
    检测所有可能的意图，返回按置信度排序的列表。
    返回格式: [{"intent": "content", "confidence": 0.85, "matched_keywords": [...]}]
    """
    q = normalize_question(question.lower())
    results = []

    for intent, keywords, base_weight in INTENT_PATTERNS:
        matched = []
        for kw in keywords:
            if kw.lower() in q:
                matched.append(kw)
        if matched:
            # 置信度 = 基础权重 × 匹配覆盖率
            confidence = base_weight * min(1.0, len(matched) / 2)
            results.append({
                "intent": intent,
                "confidence": round(confidence, 3),
                "matched_keywords": matched,
            })

    # 按置信度降序排列
    results.sort(key=lambda x: x["confidence"], reverse=True)
    return results

def match_intent(question: str) -> dict:
    """
    返回最佳单一意图（含置信度）。
    置信度低于阈值时返回 {"intent": "unrecognized", "confidence": 0}
    """
    intents = detect_intents(question)
    if not intents:
        return {"intent": "unrecognized", "confidence": 0, "matched_keywords": []}

    top = intents[0]
    if top["confidence"] < 0.3:
        return {"intent": "unrecognized", "confidence": top["confidence"], "matched_keywords": top["matched_keywords"]}

    return {"intent": top["intent"], "confidence": top["confidence"], "matched_keywords": top["matched_keywords"]}

# ─────────────────────────────────────────
# 多意图判断（用于需要多模块协作的场景）
# ─────────────────────────────────────────

def detect_multi_intent(question: str) -> list[str]:
    """
    检测问题是否涉及多个意图模块。
    例如："竞品在抖音发了什么内容" → ["competitor", "content"]
    """
    q = normalize_question(question.lower())
    detected = []

    # 明确的多意图模式
    multi_patterns = [
        (["竞品", "内容"], ["competitor", "content"]),
        (["竞品", "发"], ["competitor", "content"]),
        (["医生", "KOL"], ["doctor", "doctor"]),  # 实际都是 doctor 模块
        (["内容", "合规"], ["content", "compliance"]),
        (["数据", "内容"], ["analytics", "content"]),
        (["库存", "补货"], ["pharmacy", "pharmacy"]),  # 同一模块
    ]

    for kws, modules in multi_patterns:
        if all(kw.lower() in q for kw in kws):
            for mod in modules:
                if mod not in detected:
                    detected.append(mod)
            if detected:
                return detected

    # 单意图回退
    best = match_intent(question)
    return [best["intent"]] if best["intent"] != "unrecognized" else []

# ─────────────────────────────────────────
# 过滤器解析
# ─────────────────────────────────────────

def parse_filters(question: str, explicit_filters: dict = None, use_context: bool = True) -> dict:
    filters = dict(explicit_filters) if explicit_filters else {}

    # 尝试从上下文复用（仅当问题中没有明确指定时）
    ctx = _get_cached_context() if use_context else None

    # 显式 key=value 格式优先
    for m in re.finditer(r'(\w+)=([^\s,，]+)', question):
        key, val = m.group(1), m.group(2).strip('"\'')
        if key in KNOWN_FILTERS:
            valid_vals = KNOWN_FILTERS[key]
            if val in valid_vals:
                filters[key] = val
            else:
                matched = [v for v in valid_vals if val in v]
                if matched:
                    filters[key] = matched[0]

    # 关键词匹配
    for platform in KNOWN_FILTERS["platform"]:
        if platform in question:
            filters["platform"] = platform
            break

    for status_v in KNOWN_FILTERS["status"]:
        if status_v in question:
            filters["status"] = status_v
            break

    for priority_v in KNOWN_FILTERS["priority"]:
        if priority_v in question:
            filters["priority"] = priority_v
            break

    for level_v in KNOWN_FILTERS["risk_level"]:
        if level_v in question:
            filters["risk_level"] = level_v
            break

    for seg in KNOWN_FILTERS["segment"]:
        if seg in question:
            filters["segment"] = seg
            break

    period_match = re.search(r'(\d+)d', question)
    if period_match:
        filters["period"] = f"{period_match.group(1)}d"

    # 从上下文补全（如果关键字段缺失且上下文未过期）
    if ctx and use_context:
        for key in ["platform", "period"]:
            if key not in filters and key in ctx.get("last_filters", {}):
                filters[key] = ctx["last_filters"][key]

    return filters

# ─────────────────────────────────────────
# 平台自动识别（基于语义）
# ─────────────────────────────────────────

PLATFORM_HINTS = {
    "抖音": "douyin",
    "小红书": "xiaohongshu",
    "微信": "wechat",
    "微博": "weibo",
    "B站": "bilibili",
    "bilibili": "bilibili",
}

def infer_platform(question: str) -> str | None:
    """从问题语义推断平台参数"""
    for hint, platform in PLATFORM_HINTS.items():
        if hint in question:
            return platform
    return None

# ─────────────────────────────────────────
# 查询函数（各模块）
# ─────────────────────────────────────────

def query_content(filters: dict = None) -> dict:
    filters = filters or {}
    wc2, params2 = [], []
    for k, v in filters.items():
        if k in ("platform", "status", "priority", "format"):
            wc2.append(f"ct.{k} = %s"); params2.append(v)
        elif k == "period":
            days = int(v.replace("d", ""))
            wc2.append("ct.created_at >= DATE_SUB(NOW(), INTERVAL %s DAY)"); params2.append(days)
    wh2 = " WHERE " + " AND ".join(wc2) if wc2 else ""
    sql = f"SELECT ct.id, ct.topic, ct.platform, ct.status, ct.priority, ct.created_at, COUNT(cs.id) as script_count FROM content_topics ct LEFT JOIN content_scripts cs ON cs.topic_id = ct.id{wh2} GROUP BY ct.id, ct.topic, ct.platform, ct.status, ct.priority, ct.created_at ORDER BY ct.created_at DESC LIMIT 50"
    topics = query_all(sql, tuple(params2)) if params2 else query_all(sql)
    pending = [t for t in topics if t.get("status") == "pending"]
    published = [t for t in topics if t.get("status") == "published"]
    fd = "".join([f"，筛选条件: {', '.join(f'{k}={v}' for k,v in filters.items())}"]) if filters else ""
    return {"total_topics": len(topics), "pending_count": len(pending), "published_count": len(published), "recent_topics": topics[:5], "filters_applied": filters,
            "suggestions": [f"当前 {len(pending)} 个待创作选题", f"已发布 {len(published)} 条内容{fd}", "建议优先处理高优先级选题"]}

def query_compliance(filters: dict = None) -> dict:
    filters = filters or {}
    wc, params = [], []
    for k, v in filters.items():
        if k in ("risk_level", "review_stage"):
            col = "ct." + k if k in ("platform", "status", "priority", "format") else k
            wc.append(f"{col} = %s"); params.append(v)
    wh = " WHERE " + " AND ".join(wc) if wc else ""
    sql = f"SELECT id, content_id, review_result, violations, risk_level, compliance_score, review_stage FROM compliance_reviews{wh} ORDER BY created_at DESC LIMIT 20"
    reviews = query_all(sql, tuple(params)) if params else query_all(sql)
    active = [r for r in reviews if r.get("risk_level") in ("critical", "high")]
    r = query_one("SELECT COUNT(*) as cnt FROM compliance_rules")
    rule_count = r['cnt'] if r else 0
    return {"active_alerts": len(active), "critical_count": len([a for a in active if a.get("risk_level") == "critical"]),
            "high_count": len([a for a in active if a.get("risk_level") == "high"]), "total_rules": rule_count, "recent_reviews": reviews[:5], "filters_applied": filters,
            "suggestions": [f"当前 {len(active)} 条高风险合规告警", f"合规规则库含 {rule_count} 条规则", "建议优先处理 critical 级别告警"]}

def query_patient(filters: dict = None) -> dict:
    filters = filters or {}
    wc, params = [], []
    for k, v in filters.items():
        if k in ("status", "segment"):
            col = "ct." + k if k in ("platform", "status", "priority", "format") else k
            wc.append(f"{col} = %s"); params.append(v)
    wh = " WHERE " + " AND ".join(wc) if wc else ""
    sql = f"SELECT session_id, patient_name, patient_id, status, created_at FROM patient_sessions{wh} ORDER BY created_at DESC LIMIT 50"
    sessions = query_all(sql, tuple(params)) if params else query_all(sql)
    active = [s for s in sessions if s.get("status") == "active"]
    r = query_one("SELECT COUNT(*) as cnt FROM patient_messages WHERE sent = 0")
    pending_msgs = r['cnt'] if r else 0
    return {"total_sessions": len(sessions), "active_sessions": len(active), "pending_replies": pending_msgs, "recent_sessions": sessions[:5], "filters_applied": filters,
            "suggestions": [f"当前 {len(active)} 个活跃患者会话", f"{pending_msgs} 条消息待回复", "建议优先处理 high_risk 分群患者"]}

def query_pharmacy(filters: dict = None) -> dict:
    filters = filters or {}
    wc, params = [], []
    for k, v in filters.items():
        if k in ("product_status", "pharmacy"):
            col = "ct." + k if k in ("platform", "status", "priority", "format") else k
            wc.append(f"{col} = %s"); params.append(v)
    wh = " WHERE " + " AND ".join(wc) if wc else ""
    sql = f"SELECT id, product_id, product_name, quantity, reorder_point, pharmacy, status FROM pharmacy_inventory{wh} ORDER BY (CAST(quantity AS REAL) / NULLIF(reorder_point, 0)) ASC LIMIT 50"
    inventory = query_all(sql, tuple(params)) if params else query_all(sql)
    low_stock = [i for i in inventory if i.get("status") in ("low", "out")]
    out_of_stock = [i for i in inventory if i.get("status") == "out"]
    return {"total_items": len(inventory), "low_stock_count": len(low_stock), "out_of_stock_count": len(out_of_stock), "low_stock_items": low_stock[:5], "filters_applied": filters,
            "suggestions": [f"当前 {len(low_stock)} 个品种库存不足", f"其中 {len(out_of_stock)} 个已售罄", "建议立即启动补货流程"]}

def query_competitor(filters: dict = None) -> dict:
    filters = filters or {}
    wc, params = [], []
    for k, v in filters.items():
        if k == "platform":
            wc.append("platform = %s"); params.append(v)
    wh = " WHERE " + " AND ".join(wc) if wc else ""
    sql = f"SELECT id, product_id, name, platform, price, rating, reviews_count, sales_trend FROM drug_products{wh} ORDER BY reviews_count DESC LIMIT 50"
    products = query_all(sql, tuple(params)) if params else query_all(sql)
    analysis = query_all("SELECT competitor_name, competitor_price, competitor_rating, analysis_date FROM competitor_analysis ORDER BY analysis_date DESC LIMIT 10")
    return {"tracked_products": len(products), "recent_analysis_count": len(analysis), "products": products[:5], "filters_applied": filters,
            "suggestions": [f"追踪 {len(products)} 个竞品", f"最近 {len(analysis)} 条最新动态", "关注价格波动和评价变化"]}

def query_doctor(filters: dict = None) -> dict:
    filters = filters or {}
    wc, params = [], []
    for k, v in filters.items():
        if k in ("specialty", "level"):
            col = "ct." + k if k in ("platform", "status", "priority", "format") else k
            wc.append(f"{col} = %s"); params.append(v)
    wh = " WHERE " + " AND ".join(wc) if wc else ""
    sql = f"SELECT doctor_id, name, hospital, department, title, specialty, influence_score, compliance_score FROM doctor_profiles{wh} ORDER BY influence_score DESC LIMIT 50"
    doctors = query_all(sql, tuple(params)) if params else query_all(sql)
    visits = query_all("SELECT dv.id, dv.doctor_id, dp.name, dv.visit_type, dv.result, dv.created_at FROM doctor_visits dv LEFT JOIN doctor_profiles dp ON dp.doctor_id = dv.doctor_id ORDER BY dv.created_at DESC LIMIT 10")
    r = query_one("SELECT COUNT(*) as cnt FROM kol_profiles WHERE status = 'active'")
    kol = r['cnt'] if r else 0
    return {"total_doctors": len(doctors), "recent_visits": len(visits), "active_kols": kol, "top_doctors": doctors[:5], "filters_applied": filters,
            "suggestions": [f"管理 {len(doctors)} 位医生档案", f"最近 {len(visits)} 次拜访记录", f"当前 {kol} 位活跃KOL"]}

def query_analytics(filters: dict = None) -> dict:
    filters = filters or {}
    period = filters.get("period", "30d")
    days = int(period.replace("d", ""))
    r = query_one("SELECT COUNT(*) as cnt FROM content_campaigns WHERE status = 'active'")
    total_campaigns = r['cnt'] if r else 0
    metrics_sql = "SELECT SUM(impressions) as total_impressions, SUM(clicks) as total_clicks, SUM(spend) as total_spend, SUM(conversions) as total_conversions, AVG(engagement_rate) as avg_engagement, AVG(ctr) as avg_ctr FROM content_metrics WHERE date >= DATE_SUB(NOW(), INTERVAL %s DAY)"
    mr = query_one(metrics_sql, (days,))
    metrics_dict = dict(mr) if mr else {}
    r = query_one("SELECT COUNT(*) as cnt FROM patient_sessions WHERE status = 'active'")
    patients_active = r['cnt'] if r else 0
    r = query_one("SELECT COUNT(*) as cnt FROM compliance_reviews WHERE risk_level IN ('critical','high')")
    compliance_alerts = r['cnt'] if r else 0
    return {"active_campaigns": total_campaigns, "total_impressions": metrics_dict.get("total_impressions") or 0,
            "total_clicks": metrics_dict.get("total_clicks") or 0, "total_spend": metrics_dict.get("total_spend") or 0,
            "total_conversions": metrics_dict.get("total_conversions") or 0,
            "avg_engagement_rate": round(float(metrics_dict.get("avg_engagement") or 0), 2),
            "avg_ctr": round(float(metrics_dict.get("avg_ctr") or 0), 4),
            "active_patients": patients_active, "compliance_alerts": compliance_alerts, "filters_applied": filters,
            "period_days": days,
            "suggestions": [f"当前 {total_campaigns} 个活跃营销活动", f"近{period} {(metrics_dict.get('total_impressions') or 0):,} 次曝光", f"合规告警 {compliance_alerts} 条需关注"]}

def query_knowledge(filters: dict = None) -> dict:
    r = query_one("SELECT COUNT(*) as cnt FROM compliance_rules")
    rules = r['cnt'] if r else 0
    r = query_one("SELECT COUNT(*) as cnt FROM kol_profiles")
    kols = r['cnt'] if r else 0
    r = query_one("SELECT COUNT(*) as cnt FROM doctor_profiles")
    doctors = r['cnt'] if r else 0
    return {"compliance_rules_count": rules, "kol_profiles_count": kols, "doctor_profiles_count": doctors, "filters_applied": filters or {},
            "suggestions": ["可通过知识库查询广告法、药品管理法条款", "支持临床指南和药品说明书查询", "KOL和医生档案可供检索"]}

MODULE_HANDLERS = {
    "content": query_content, "hook": query_content, "optimize": query_content,
    "compliance": query_compliance, "patient": query_patient, "pharmacy": query_pharmacy,
    "competitor": query_competitor, "doctor": query_doctor,
    "analytics": query_analytics, "knowledge": query_knowledge, "general": query_analytics,
}

# ─────────────────────────────────────────
# 结果叙述与思考生成
# ─────────────────────────────────────────

def _generate_thinking(module: str, question: str, result: dict, filters: dict, confidence: float = 1.0) -> str:
    parts = [f"意图识别：「{question}」→ {module} 模块（置信度 {confidence:.0%}）"]
    if filters:
        parts.append(f"筛选条件：{', '.join(f'{k}={v}' for k,v in filters.items())}")
    if module == "content":
        p = result.get('pending_count', 0); pv = result.get('published_count', 0)
        parts.append(f"→ 选题积压较多（{p}个），建议优先处理高优先级" if p > 10 else f"→ 当前 {p} 个待创作选题，健康运转")
        parts.append(f"→ 已发布内容 {pv} 条，持续更新中")
    elif module == "compliance":
        c = result.get('critical_count', 0); h = result.get('high_count', 0)
        parts.append(f"→ 🚨 发现 {c} 条 critical 级别告警，需要立即处理" if c > 0 else f"→ ⚠️  {h} 条 high 级别告警，建议尽快处理" if h > 0 else "→ 合规状态良好，无高风险告警")
        parts.append(f"→ 规则库共 {result.get('total_rules', 0)} 条，持续更新")
    elif module == "patient":
        p = result.get('pending_replies', 0)
        parts.append(f"→ ⚠️ {p} 条消息待回复，存在患者失联风险" if p > 5 else f"→ 当前 {result.get('active_sessions', 0)} 个活跃会话，响应及时")
    elif module == "pharmacy":
        o = result.get('out_of_stock_count', 0); l = result.get('low_stock_count', 0)
        parts.append(f"→ 🚨 {o} 个品种已售罄，紧急补货中" if o > 0 else f"→ ⚠️ {l} 个品种库存不足，建议本周补货" if l > 0 else "→ 库存状态正常，无告警")
    elif module == "analytics":
        imp = result.get('total_impressions', 0); ctr = result.get('avg_ctr', 0); cpg = result.get('active_campaigns', 0)
        parts.append(f"→ {cpg} 个活跃活动，近{result.get('period_days',30)}天 {imp:,} 次曝光")
        if ctr:
            parts.append(f"→ 平均点击率 {ctr:.2%}，{'高于行业均值' if ctr > 0.03 else '有优化空间'}")
    elif module == "competitor":
        parts.append(f"→ 追踪 {result.get('tracked_products',0)} 个竞品，{result.get('recent_analysis_count',0)} 条最新动态")
    return " | ".join(parts)

def _narrate_result(module: str, result: dict) -> str:
    s = result.get("suggestions", [])
    fi = result.get("filters_applied", {})
    fd = ", ".join(f"{k}={v}" for k, v in fi.items()) if fi else ""
    suf = f" | 筛选: {fd}" if fd else ""
    if module == "content": return f"📝 **内容运营**：{result.get('pending_count',0)} 个待创作选题，{result.get('published_count',0)} 条已发布内容{suf}。" + (" ".join(s[:2]) if s else "")
    if module == "compliance": return f"🛡 **合规状态**：{result.get('active_alerts',0)} 条高风险告警（critical: {result.get('critical_count',0)}, high: {result.get('high_count',0)}），规则库 {result.get('total_rules',0)} 条。" + (" ".join(s[:2]) if s else "")
    if module == "patient": return f"👥 **患者管理**：{result.get('active_sessions',0)} 个活跃会话，{result.get('pending_replies',0)} 条待回复消息。" + (" ".join(s[:2]) if s else "")
    if module == "pharmacy": return f"💊 **药房库存**：{result.get('total_items',0)} 个品种，{result.get('low_stock_count',0)} 个不足，{result.get('out_of_stock_count',0)} 个售罄。" + (" ".join(s[:2]) if s else "")
    if module == "competitor": return f"🔍 **竞品追踪**：{result.get('tracked_products',0)} 个产品，{result.get('recent_analysis_count',0)} 条最新动态。" + (" ".join(s[:2]) if s else "")
    if module == "doctor": return f"👨‍⚕️ **医生触达**：{result.get('total_doctors',0)} 位医生档案，{result.get('recent_visits',0)} 次最近拜访，{result.get('active_kols',0)} 位活跃KOL。" + (" ".join(s[:2]) if s else "")
    if module == "analytics": return f"📊 **运营概览**：{result.get('active_campaigns',0)} 个活跃活动，近{result.get('period_days',30)}天 {result.get('total_impressions',0):,} 次曝光，{result.get('compliance_alerts',0)} 条合规告警。" + (" ".join(s[:2]) if s else "")
    if module == "knowledge": return f"📚 **知识库**：{result.get('compliance_rules_count',0)} 条合规规则，{result.get('kol_profiles_count',0)} 个KOL档案。" + (" ".join(s[:2]) if s else "")
    return " ".join(s[:2]) if s else "查询完成"

# ─────────────────────────────────────────
# 主入口函数
# ─────────────────────────────────────────

def ask(question: str, module: str = "auto", filters: dict = None, multi_intent: bool = False) -> dict:
    """
    统一问答入口

    参数:
        question: 用户问题（必填）
        module: 强制指定模块（"auto" 则自动识别）
        filters: 显式筛选条件（可选）
        multi_intent: 是否返回多意图结果（默认 False）

    返回:
        包含 intent, module, confidence, all_intents, result, narration, thinking 的字典
    """
    if not question or not question.strip():
        return {"error": "question is required"}

    question = question.strip()
    normalized_q = normalize_question(question)

    # 1. 检测所有可能意图（含置信度）
    all_intents = detect_intents(question)

    # 2. 多意图检测（当 multi_intent=True 或检测到多模块关键词）
    detected_modules = detect_multi_intent(question) if multi_intent else []

    # 3. 确定主意图
    if module != "auto":
        # 强制指定模块
        best_intent = {"intent": module, "confidence": 1.0, "matched_keywords": ["强制指定"]}
    else:
        if not all_intents:
            best_intent = {"intent": "unrecognized", "confidence": 0, "matched_keywords": []}
        elif all_intents[0]["confidence"] < 0.3:
            # 置信度过低，不猜
            best_intent = {"intent": "unrecognized", "confidence": all_intents[0]["confidence"], "matched_keywords": all_intents[0].get("matched_keywords", [])}
        else:
            best_intent = all_intents[0]

    target_module = best_intent["intent"]

    # 4. 解析过滤器（包含上下文补全）
    parsed_filters = parse_filters(question, filters)

    # 5. 平台自动推断
    inferred_platform = infer_platform(question)
    if inferred_platform and "platform" not in parsed_filters:
        parsed_filters["platform"] = inferred_platform

    # 6. 更新上下文记忆
    _set_cached_context(best_intent["intent"], target_module, parsed_filters)

    # 7. 执行查询
    if target_module == "unrecognized":
        return {
            "intent": "unrecognized",
            "confidence": best_intent["confidence"],
            "all_intents": [{"intent": i["intent"], "confidence": i["confidence"]} for i in all_intents],
            "module": None,
            "error": "无法识别意图，请尝试更明确的描述",
            "question": question,
            "filters_parsed": parsed_filters,
            "hint": "可尝试：内容创作、合规审核、患者管理、竞品分析、医生触达、运营数据",
            "platform_inferred": inferred_platform,
        }

    try:
        handler = MODULE_HANDLERS.get(target_module, query_analytics)
        result = handler(parsed_filters)
    except Exception as e:
        return {
            "error": str(e),
            "intent": best_intent["intent"],
            "confidence": best_intent["confidence"],
            "all_intents": [{"intent": i["intent"], "confidence": i["confidence"]} for i in all_intents],
            "module": target_module,
            "question": question,
            "filters_parsed": parsed_filters,
        }

    narration = _narrate_result(target_module, result)
    thinking = _generate_thinking(target_module, question, result, parsed_filters, best_intent["confidence"])

    response = {
        "intent": best_intent["intent"],
        "confidence": best_intent["confidence"],
        "all_intents": [{"intent": i["intent"], "confidence": i["confidence"]} for i in all_intents],
        "module": target_module,
        "result": result,
        "question": question,
        "filters_parsed": parsed_filters,
        "narration": narration,
        "thinking": thinking,
        "platform_inferred": inferred_platform,
        "multi_intent_detected": detected_modules if detected_modules else None,
    }

    # 多意图模式返回所有检测到的模块结果
    if detected_modules and len(detected_modules) > 1:
        multi_results = {}
        for mod in detected_modules:
            try:
                h = MODULE_HANDLERS.get(mod, query_analytics)
                multi_results[mod] = h(parsed_filters)
            except Exception:
                multi_results[mod] = {"error": f"模块 {mod} 查询失败"}
        response["multi_results"] = multi_results

    return response

# ─────────────────────────────────────────
# CLI 入口
# ─────────────────────────────────────────

def _parse_args():
    if len(sys.argv) > 1:
        try:
            return json.loads(sys.argv[1])
        except json.JSONDecodeError:
            return {"question": sys.argv[1]}
    if not sys.stdin.isatty():
        data = sys.stdin.read().strip()
        if data:
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                return {"question": data}
    return {}

if __name__ == "__main__":
    args = _parse_args()
    result = ask(
        question=args.get("question", ""),
        module=args.get("module", "auto"),
        filters=args.get("filters"),
        multi_intent=args.get("multi_intent", False),
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))