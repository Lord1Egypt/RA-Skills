#!/usr/bin/env python3
"""
DigitalSalesClaw - compliance.py
医药合规审核工具

设计理念（本体论视角）：
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
语义解析 → 知识图谱上下文 → 结构化证据 → AI推理判断
    本质：证据提供器，AI是判断者

三层职责分离：
  1. 合规工具（本模块）：语义解析 + 知识图谱查询 + 规则兜底Guardrail
  2. Agent推理层（OpenClaw）：基于结构化证据做Chain-of-Thought判断
  3. 知识库（knowledge/）：法规域文档提供领域背景

为什么这样设计？
药企合规的核心难点不是"有没有违禁词"，而是：
  - "效果好" → 降糖药合规表述 vs 减肥药可能是违规疗效承诺
  - "临床证明" → 需要具体试验信息才有意义
  - "专家推荐" → 合规科普 vs 处方药代言（完全不同的语义）
规则无法分辨这些上下文，但AI+本体论可以。

输入: {"action": "analyze|review|guardrail|export_report", "content": "...", "platform": "...", "drug_context": {...}}
输出: 结构化语义证据 + 合规分析报告（供AI推理用）
"""

import sys
import json
import re
from pathlib import Path
from datetime import datetime
from db import get_conn, close_conn

SKILL_DIR = Path(__file__).parent.parent

# ─────────────────────────────────────────
# 语义实体识别（基于关键词扩展，不是硬编码映射）
# ─────────────────────────────────────────
MEDICAL_INDICATOR_PATTERNS = [
    # 疾病/症状
    (r"糖尿病|高血糖|血糖", "disease", "内分泌/代谢"),
    (r"高血压|血压", "disease", "心血管"),
    (r"高血脂|血脂", "disease", "心血管/代谢"),
    (r"冠心病|心梗|脑梗", "disease", "心血管"),
    (r"肝炎|乙肝|丙肝", "disease", "感染/肝病"),
    (r"胃炎|胃溃疡|幽门", "disease", "消化"),
    (r"抑郁|焦虑|失眠|睡眠", "disease", "精神/神经"),
    (r"骨质疏松|骨折", "disease", "骨科"),
    (r"类风湿|关节炎|关节痛", "disease", "风湿免疫"),
    (r"皮炎|湿疹|荨麻疹|过敏", "disease", "皮肤科"),
    (r"咽炎|鼻炎|感冒|咳嗽", "disease", "呼吸"),
    # 药品类别
    (r"降糖药|降血糖|胰岛素|二甲双胍|GLP-1", "drug_category", "糖尿病用药"),
    (r"降压药|钙通道阻滞剂|ARB|ACEI", "drug_category", "高血压用药"),
    (r"他汀|贝特|降脂药", "drug_category", "调脂用药"),
    (r"抗生素|头孢|阿莫西林|阿奇霉素", "drug_category", "抗菌药"),
    (r"中药|中成药|汤剂|配方颗粒", "drug_category", "中药"),
    (r"生物制剂|单抗|PD-1|靶向药", "drug_category", "创新药"),
    (r"OTC|非处方药", "drug_category", "OTC"),
    (r"处方药|Rx", "drug_category", "处方药"),
    # 疗效声明类型（关键语义！）
    (r"根治?|治愈|药到病除", "efficacy_claim", "根治/治愈声明"),
    (r"完全.*(治愈|缓解|好转)", "efficacy_claim", "绝对化疗效"),
    (r"无效退款|保证治愈", "efficacy_claim", "无效承诺"),
    (r"永不复[发癒]|包治百病", "efficacy_claim", "夸大承诺"),
    (r"\\d+%?\s*有效率|有效率\\d+%?", "efficacy_claim", "具体有效率声明"),
    (r"临床试验|研究表明|数据.*显示", "efficacy_claim", "临床数据声明"),
    (r"排名第一|销量第.?一|最佳", "efficacy_claim", "排名/最优声明"),
    (r"专家推荐|医生推荐|医师推荐", "authority_claim", "权威背书"),
    (r"患者.*(治愈|好转|康复)|.*阿姨.*好了", "testimonial", "患者证言"),
    (r"服用前.*服用后|治疗前后.*对比", "testimonial", "患者对比"),
]

# 平台→合规要求映射（语义上下文）
PLATFORM_RULES = {
    "douyin": {
        "name": "抖音",
        "medical_content": "需医疗资质认证，内容不得涉及处方药推荐",
        "restricted_claims": ["在线开药", "医生看诊", "凭处方购买"],
        "allowed_formats": ["健康科普", "用药常识", "疾病教育"],
    },
    "xiaohongshu": {
        "name": "小红书",
        "medical_content": "禁止夸大疗效，禁止处方药宣传种草",
        "restricted_claims": ["OTC购买引导", "处方药种草"],
        "allowed_formats": ["经验分享", "健康笔记", "用药记录"],
    },
    "wechat": {
        "name": "微信",
        "medical_content": "禁止虚假宣传，朋友圈/群组不得发布医药广告",
        "restricted_claims": ["点击购买", "扫码购买", "外链引导"],
        "allowed_formats": ["科普文章", "健康资讯"],
    },
}

# 绝对禁区（Guardrail-only规则，极少量，只用于极端案例拦截）
GUARDRAIL_RULES = [
    # 完全禁止的绝对化表述（直接触发critical，不进入AI推理）
    {"pattern": r"根治|治愈|保证治愈|彻底治愈|包治百病", "level": "critical",
     "reason": "绝对化医疗承诺，任何情况下均违规"},
    {"pattern": r"永不复[发癒]", "level": "critical",
     "reason": "夸大康复承诺"},
    {"pattern": r"国家级|最佳|最优|顶级", "level": "critical",
     "reason": "广告法绝对化用语"},
    {"pattern": r"Rx|处方药.*购买|凭处方购买", "level": "critical",
     "reason": "处方药大众传播违规"},
    {"pattern": r"专家推荐.*(药品|疗法)|医生推荐.*(药品|疗法)", "level": "high",
     "reason": "处方药代言人违规"},
    {"pattern": r"医生.*看诊|在线开药", "level": "critical",
     "reason": "无资质医疗行为"},
    {"pattern": r"无效退款", "level": "high",
     "reason": "医疗无效承诺违规"},
    {"pattern": r"算命|风水|迷信", "level": "critical",
     "reason": "封建迷信内容"},
]


# ─────────────────────────────────────────
# 语义解析引擎
# ─────────────────────────────────────────

def extract_medical_entities(content: str) -> dict:
    """
    从内容中提取医学实体和声明类型
    返回结构化语义证据（供AI推理用）
    """
    entities = {
        "diseases": [],
        "drug_categories": [],
        "efficacy_claims": [],
        "authority_claims": [],
        "testimonials": [],
        "platform_mentions": [],
        "raw_indicators": [],
    }

    for pattern, etype, label in MEDICAL_INDICATOR_PATTERNS:
        for m in re.finditer(pattern, content, re.IGNORECASE):
            span = m.span()
            snippet = content[max(0, span[0]-15):span[1]+15]
            indicator = {
                "text": m.group(),
                "type": etype,
                "label": label,
                "position": span[0],
                "context": f"...{snippet}...",
            }
            entities["raw_indicators"].append(indicator)

            if etype == "disease" and label not in entities["diseases"]:
                entities["diseases"].append(label)
            elif etype == "drug_category" and label not in entities["drug_categories"]:
                entities["drug_categories"].append(label)
            elif etype == "efficacy_claim" and label not in entities["efficacy_claims"]:
                entities["efficacy_claims"].append(label)
            elif etype == "authority_claim" and label not in entities["authority_claims"]:
                entities["authority_claims"].append(label)
            elif etype == "testimonial" and label not in entities["testimonials"]:
                entities["testimonials"].append(label)

    # 平台识别
    for platform, rules in PLATFORM_RULES.items():
        if platform in content.lower():
            entities["platform_mentions"].append(platform)
        for kw in rules.get("restricted_claims", []):
            if kw in content:
                entities["platform_mentions"].append(f"{platform}:restricted:{kw}")

    return entities


def check_guardrail(content: str) -> dict:
    """
    Guardrail检查：极少量绝对禁区规则
    用于拦截明显违规，不做语义判断（AI负责语义判断）
    """
    violations = []
    for rule in GUARDRAIL_RULES:
        for m in re.finditer(rule["pattern"], content, re.IGNORECASE):
            span = m.span()
            snippet = content[max(0, span[0]-10):span[1]+10]
            violations.append({
                "pattern_matched": rule["pattern"],
                "matched_text": m.group(),
                "position": span[0],
                "severity": rule["level"],
                "reason": rule["reason"],
                "snippet": f"...{snippet}...",
                "is_guardrail": True,  # 标记：这是规则拦截，不是AI判断
            })
    return violations


def query_knowledge_context(entities: dict, conn) -> dict:
    """
    从知识库查询相关合规上下文
    返回：该内容涉及的疾病域/药品类的合规关注点
    """
    context = {
        "disease_domains": entities.get("diseases", []),
        "drug_domains": entities.get("drug_categories", []),
        "compliance_focus": [],  # AI需要重点关注的风险点
        "relevant_regulations": [],
        "platform_requirements": [],
    }

    # 合成合规关注点（基于实体类型，AI据此深入推理）
    if entities.get("efficacy_claims"):
        context["compliance_focus"].append({
            "type": "疗效声明",
            "claims": entities["efficacy_claims"],
            "ai_prompt": "该内容包含疗效声明，请判断：(1)声明是否有具体数据支撑？(2)数据是否具有统计显著性？(3)是否属于绝对化承诺？"
        })

    if entities.get("authority_claims"):
        context["compliance_focus"].append({
            "type": "权威背书",
            "claims": entities["authority_claims"],
            "ai_prompt": "该内容包含权威背书，请判断：(1)是否为处方药代言？(2)专家身份是否合规？(3)是否构成医疗误导？"
        })

    if entities.get("testimonials"):
        context["compliance_focus"].append({
            "type": "患者证言",
            "claims": entities["testimonials"],
            "ai_prompt": "该内容包含患者证言，请判断：(1)是否构成疗效承诺？(2)是否违反广告法患者证言规定？(3)是否有虚构或夸大成分？"
        })

    # 平台特定要求
    for platform in set(entities.get("platform_mentions", [])):
        if isinstance(platform, str) and ":" in platform:
            p, _, claim = platform.split(":", 2)
            if p in PLATFORM_RULES:
                context["platform_requirements"].append({
                    "platform": PLATFORM_RULES[p]["name"],
                    "restriction": claim,
                    "rule": "该平台明确限制此表述，需确认是否构成违规"
                })

    return context


def calculate_compliance_score(guardrail_violations: list, entities: dict) -> dict:
    """
    计算合规评分（基于Guardrail结果 + 实体复杂度）
    注意：这是统计评分，不是语义判断。真正的判断由AI做。
    """
    if not guardrail_violations:
        return {
            "guardrail_score": 100,
            "guardrail_level": "pass",
            "severity_distribution": {"critical": 0, "high": 0, "medium": 0, "low": 0}
        }

    severity_weights = {"critical": 30, "high": 20, "medium": 10, "low": 5}
    deduction = sum(severity_weights.get(v.get("severity", "medium"), 10)
                    for v in guardrail_violations)

    score = max(0, 100 - deduction)

    dist = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for v in guardrail_violations:
        dist[v.get("severity", "medium")] = dist.get(v.get("severity", "medium"), 0) + 1

    level = ("fail" if score < 50 else
              "review_required" if score < 70 else
              "warning" if score < 90 else "pass")

    return {
        "guardrail_score": score,
        "guardrail_level": level,
        "severity_distribution": dist
    }


def analyze_content_semantically(content: str, platform: str = "douyin",
                                  drug_context: dict = None, conn=None) -> dict:
    """
    语义优先合规分析主入口

    输出结构（供AI推理用）：
    {
      "semantic_entities": {...},      # 语义实体提取结果
      "guardrail_results": [...],     # 规则兜底拦截结果
      "knowledge_context": {...},      # 知识图谱上下文
      "compliance_score": {...},      # 统计评分（参考用）
      "evidence_for_ai": [...],       # 供AI深度推理的证据链
      "ai_reasoning_prompt": "..."    # 给AI的推理引导
    }
    """
    # Step 1: Guardrail检查（规则兜底，极端案例拦截）
    guardrail_violations = check_guardrail(content)

    # Step 2: 语义实体提取
    entities = extract_medical_entities(content)

    # Step 3: 知识图谱上下文查询
    knowledge_context = query_knowledge_context(entities, conn)

    # Step 4: 统计评分（参考用，非AI判断）
    score_info = calculate_compliance_score(guardrail_violations, entities)

    # Step 5: 合成AI推理证据链
    evidence_for_ai = []

    if entities.get("diseases"):
        evidence_for_ai.append({
            "type": "疾病域",
            "content": f"涉及疾病域：{'、'.join(entities['diseases'])}",
            "question": "这些疾病的疗效声明是否合规？是否有绝对化承诺？"
        })

    if entities.get("drug_categories"):
        drug_info = {
            "糖尿病用药": "降糖药合规表述：可说明血糖管理效果，不得声称'根治'",
            "高血压用药": "降压药合规表述：可说明血压控制，不得声称'治愈高血压'",
            "调脂用药": "调脂药合规表述：可说明血脂调节，不得声称'彻底治愈'",
            "中药": "中药合规表述：可说明中医理论支持下的调理作用，不得声称'根治'",
            "处方药": "处方药：严禁在任何大众媒体进行疗效宣传",
            "OTC": "OTC合规表述：可说明适应症，不得声称绝对疗效",
        }
        relevant = [drug_info.get(d, f"药品类别：{d}") for d in entities["drug_categories"]]
        evidence_for_ai.append({
            "type": "药品类别",
            "content": "；".join(relevant),
            "question": "该药品类别的合规边界是什么？当前表述是否越界？"
        })

    if entities.get("efficacy_claims"):
        evidence_for_ai.append({
            "type": "疗效声明分析",
            "claims": entities["efficacy_claims"],
            "question": "声明的具体数据和措辞是否合规？需要哪些支撑材料？"
        })

    if entities.get("authority_claims"):
        evidence_for_ai.append({
            "type": "权威背书",
            "claims": entities["authority_claims"],
            "question": "是否存在违规的专家/医生代言？"
        })

    if entities.get("testimonials"):
        evidence_for_ai.append({
            "type": "患者证言",
            "claims": entities["testimonials"],
            "question": "患者证言是否构成疗效承诺？是否违反《广告法》第十三条？"
        })

    # 平台要求
    if platform in PLATFORM_RULES:
        p = PLATFORM_RULES[platform]
        evidence_for_ai.append({
            "type": "平台合规要求",
            "content": f"平台：{p['name']} | 允许格式：{'、'.join(p['allowed_formats'])} | 限制：{'、'.join(p.get('restricted_claims', []))}",
            "question": f"内容是否超出{p['name']}允许的医疗内容范围？"
        })

    # Guardrail拦截项（直接给AI确认）
    if guardrail_violations:
        evidence_for_ai.append({
            "type": "Guardrail拦截（规则兜底）",
            "violations": [
                {
                    "text": v["matched_text"],
                    "severity": v["severity"],
                    "reason": v["reason"]
                }
                for v in guardrail_violations
            ],
            "question": "以上为规则拦截的疑似违规点，请结合语义上下文判断是否确实违规"
        })

    # 构造AI推理引导
    if evidence_for_ai:
        ai_prompt = f"你是一位医药合规审核专家。请基于以下证据链，判断内容是否合规：\n\n"
        for i, ev in enumerate(evidence_for_ai, 1):
            ai_prompt += f"{i}. 【{ev['type']}】{ev.get('content', '')}\n"
            if "question" in ev:
                ai_prompt += f"   审核要点：{ev['question']}\n"
        ai_prompt += f"\n内容原文：{content[:200]}{'...' if len(content) > 200 else ''}"
        ai_prompt += f"\n\n请给出：(1)合规判断 (2)具体违规点 (3)修改建议"
    else:
        ai_prompt = f"该内容未检测到明显医学语义违规，请结合常识判断。\n\n内容：{content[:200]}"

    return {
        # 核心语义分析结果
        "semantic_entities": {
            "diseases": entities.get("diseases", []),
            "drug_categories": entities.get("drug_categories", []),
            "efficacy_claims": entities.get("efficacy_claims", []),
            "authority_claims": entities.get("authority_claims", []),
            "testimonials": entities.get("testimonials", []),
            "platform_mentions": entities.get("platform_mentions", []),
        },
        # 规则兜底结果
        "guardrail_results": guardrail_violations,
        # 知识图谱上下文
        "knowledge_context": knowledge_context,
        # 统计评分（参考）
        "compliance_score": score_info,
        # 供AI推理的证据链
        "evidence_for_ai": evidence_for_ai,
        # AI推理引导
        "ai_reasoning_prompt": ai_prompt,
        # 推理链（供 Agent 看）
        "thinking": _build_thinking(entities, guardrail_violations, score_info),
        # 摘要
        "summary": _build_summary(guardrail_violations, entities, score_info),
    }



def _build_thinking(entities, guardrail_violations, score_info) -> str:
    """生成推理链描述"""
    parts = []
    diseases = entities.get("diseases", [])
    drugs = entities.get("drug_categories", [])
    if diseases:
        parts.append("疾病域：" + "、".join(diseases))
    if drugs:
        parts.append("药品类别：" + "、".join(drugs))
    if guardrail_violations:
        parts.append("Guardrail拦截：" + str(len(guardrail_violations)) + "处")
    parts.append("评分" + str(score_info.get("score", 100)))
    return " | ".join(parts)

def _build_summary(guardrail_violations, entities, score_info) -> dict:
    """生成人类可读的合规摘要"""
    if guardrail_violations:
        levels = set(v["severity"] for v in guardrail_violations)
        if "critical" in levels:
            summary_text = "🚨 Guardrail拦截到critical级别疑似违规，建议立即修改"
        elif "high" in levels:
            summary_text = "⚠️ Guardrail拦截到high级别疑似违规，建议修改后发布"
        else:
            summary_text = "💡 检测到疑似违规内容，建议AI深度审核"
    elif entities.get("efficacy_claims") or entities.get("authority_claims"):
        summary_text = "🤔 包含疗效/权威声明，建议AI深度审核确认合规性"
    elif entities.get("diseases") or entities.get("drug_categories"):
        summary_text = "ℹ️ 涉及医疗内容，建议确认表述准确性"
    else:
        summary_text = "✅ 未检测到明显违规，建议常规审核"

    return {
        "text": summary_text,
        "guardrail_violation_count": len(guardrail_violations),
        "has_semantic_risk": bool(entities.get("efficacy_claims") or
                                  entities.get("authority_claims") or
                                  entities.get("testimonials")),
        "needs_ai_review": bool(guardrail_violations or
                                entities.get("efficacy_claims") or
                                entities.get("authority_claims")),
        "score": score_info.get("guardrail_score", 100),
        "level": score_info.get("guardrail_level", "pass"),
    }


def _get_db_conn():
    """获取数据库连接（MySQL 优先）"""
    try:
        import mysql.connector
        from mysql.connector import pooling
        pool = pooling.MySQLConnectionPool(
            host="localhost", port=3306, user="ontology", unix_socket="/tmp/mysql.sock",
            password="ontology", database="digitalsalesclaw",
            pool_name="dsc_compliance_v3", pool_size=3,
            charset="utf8mb4", use_unicode=True
        )
        conn = pool.get_connection()
        conn.autocommit = False
        return conn, False
    except Exception:
        conn = get_conn()
        return conn, True


def review_content(content: str, content_id: str = None,
                   platform: str = "douyin", conn=None) -> dict:
    """完整合规审核（兼容旧接口，内部路由到语义分析）"""
    conn, is_sqlite = _get_db_conn()
    try:
        result = analyze_content_semantically(content, platform, conn=conn)

        # 保存审核记录
        if content_id:
            now = datetime.now().isoformat()
            risk = "critical" if result["summary"]["guardrail_violation_count"] > 0 else "medium"
            violations_json = json.dumps({
                "guardrail_violations": result["guardrail_results"],
                "entities": result["semantic_entities"]
            }, ensure_ascii=False)

            if is_sqlite:
                conn.execute("""
                    INSERT INTO compliance_reviews
                    (content_id, review_stage, violations, risk_level, compliance_score, submitted_at, completed_at, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (content_id, "semantic_review", violations_json, risk,
                      result["compliance_score"]["guardrail_score"], now, now, now))
            else:
                conn.execute("""
                    INSERT INTO compliance_reviews
                    (content_id, review_stage, violations, risk_level, compliance_score, submitted_at, completed_at, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (content_id, "semantic_review", violations_json, risk,
                      result["compliance_score"]["guardrail_score"], now, now, now))
            conn.commit()

        return result
    finally:
        close_conn(conn)


def export_report(risk_level: str = None) -> dict:
    """导出合规报告"""
    conn, is_sqlite = _get_db_conn()
    try:
        if is_sqlite:
            query = "SELECT * FROM compliance_reviews WHERE 1=1"
            params = []
            if risk_level:
                query += " AND risk_level = ?"
                params.append(risk_level)
        else:
            query = "SELECT * FROM compliance_reviews WHERE 1=1"
            params = []
            if risk_level:
                query += " AND risk_level = %s"
                params.append(risk_level)

        rows = conn.execute(query, params).fetchall()
        cols = [d[0] for d in conn.execute("SELECT * FROM compliance_reviews LIMIT 0").description]
        reviews = [dict(zip(cols, r)) for r in rows]

        summary = {
            "total_reviews": len(reviews),
            "critical": len([r for r in reviews if r.get("risk_level") == "critical"]),
            "high": len([r for r in reviews if r.get("risk_level") == "high"]),
            "medium": len([r for r in reviews if r.get("risk_level") == "medium"]),
            "low": len([r for r in reviews if r.get("risk_level") == "low"]),
        }
        return {"summary": summary, "reviews": reviews[:20], "generated_at": datetime.now().isoformat()}
    finally:
        close_conn(conn)


def _parse_args():
    if len(sys.argv) > 1:
        try:
            return json.loads(sys.argv[1])
        except json.JSONDecodeError:
            return {"action": "review", "content": sys.argv[1]}
    if not sys.stdin.isatty():
        data = sys.stdin.read().strip()
        if data:
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                return {"action": "review", "content": data}
    return {}


if __name__ == "__main__":
    args = _parse_args()
    action = args.get("action", "analyze")
    content = args.get("content", "")
    platform = args.get("platform", "douyin")
    content_id = args.get("content_id")

    if action == "guardrail":
        result = {"guardrail_violations": check_guardrail(content)}
    elif action == "extract":
        result = extract_medical_entities(content)
    elif action == "analyze":
        result = analyze_content_semantically(content, platform)
    else:
        result = review_content(content, content_id, platform)

    print(json.dumps(result, ensure_ascii=False, indent=2))
