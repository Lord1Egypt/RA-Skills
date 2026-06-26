#!/usr/bin/env python3
"""
DigitalSalesClaw - orchestrate.py
Agent 编排层：多工具协作 + 推理链生成

设计原则：
- 工具是"能力"，不是"接口"
- 编排层负责：任务分解、工具调用顺序、结果聚合、推理链生成
- 对话输出：附带推理过程（Thinking Process），不是只给结论

核心能力：
1. content_pipeline: 选题→创作→合规→预测 全链路
2. patient_care_pipeline: 分群→会话分析→工单升级 全链路
3. competitor_intel_pipeline: 竞品→内容→KOL 全链路
4. 推理链生成：每一步都记录思考过程，供最终叙述用
"""
import sys
import json
from datetime import datetime
from pathlib import Path
from db import get_conn, close_conn

SKILL_DIR = Path(__file__).parent.parent

# ─────────────────────────────────────────
# 推理链记录器
# ─────────────────────────────────────────
class ReasoningChain:
    """记录每一步推理，最终生成带思考过程的叙述"""
    def __init__(self):
        self.steps = []
        self.context = {}

    def add(self, step: str, thinking: str, data: dict = None, confidence: str = "medium"):
        self.steps.append({
            "step": step,
            "thinking": thinking,
            "data": data or {},
            "confidence": confidence,
            "timestamp": datetime.now().isoformat(),
        })

    def set_context(self, key: str, value):
        self.context[key] = value

    def get_context(self, key: str, default=None):
        return self.context.get(key, default)

    def render(self) -> str:
        """渲染为可读的推理链叙述"""
        lines = []
        for i, s in enumerate(self.steps, 1):
            lines.append(f"**{i}. {s['step']}**")
            lines.append(f"   思考：{s['thinking']}")
            if s['data']:
                for k, v in list(s['data'].items())[:3]:
                    if v and k not in ('raw', 'logs', 'details'):
                        lines.append(f"   → {k}: {v}")
            if s['confidence'] == 'low':
                lines.append(f"   ⚠️ 信息不足，部分为推断")
            lines.append("")
        return "\n".join(lines)

    def to_dict(self):
        return {"steps": self.steps, "context": self.context}


# ─────────────────────────────────────────
# 工具调用包装（捕获推理链）
# ─────────────────────────────────────────
def exec_tool(tool_name: str, params: dict) -> tuple[dict, dict]:
    """
    执行工具并返回 (result, reasoning_data)
    reasoning_data 包含这一步的推理上下文
    """
    tool_path = SKILL_DIR / "tools" / f"{tool_name}.py"
    import subprocess
    try:
        result = subprocess.run(
            ["python3", str(tool_path), json.dumps(params)],
            capture_output=True, text=True, timeout=60,
            cwd=str(SKILL_DIR / "tools"),
        )
        if result.returncode != 0:
            return {"error": result.stderr}, {"error": True}
        try:
            data = json.loads(result.stdout.strip())
            return data, {}
        except json.JSONDecodeError:
            return {"raw": result.stdout.strip()}, {}
    except subprocess.TimeoutExpired:
        return {"error": f"Timeout: {tool_name}"}, {"error": True}
    except Exception as e:
        return {"error": str(e)}, {"error": True}


# ─────────────────────────────────────────
# 内容创作 pipeline
# ─────────────────────────────────────────
def content_creation_pipeline(topic: str, platform: str = "douyin", drug_context: str = None) -> dict:
    """
    全链路内容创作：选题 → 创作 → 合规审核 → 效果预测
    
    反馈循环：合规失败 → 自动修正 → 重审（最多2轮）
    """
    chain = ReasoningChain()
    chain.set_context("topic", topic)
    chain.set_context("platform", platform)
    chain.set_context("drug_context", drug_context)

    # ── Step 1: 选题推荐 ──
    chain.add(
        "选题分析",
        f"根据「{topic}」，结合平台特性和当前热点，推荐最适合的话题角度",
        confidence="high"
    )
    
    recommend_result, _ = exec_tool("topic_recommend", {
        "action": "recommend",
        "product": topic,
        "platform": platform,
        "limit": 3
    })
    
    recommended_topics = recommend_result.get("recommendations", [])
    if not recommended_topics:
        # 无推荐时，使用用户给定 topic 作为主话题
        selected_topic = topic
        angle = "健康科普角度"
    else:
        top = recommended_topics[0]
        selected_topic = top.get("topic", topic)
        angle = top.get("reason", "热点+季节性匹配")

    chain.add(
        "话题确定",
        f"选择角度：「{selected_topic}」，理由：{angle}",
        {"selected_topic": selected_topic, "angle": angle, "alternatives": [t.get("topic") for t in recommended_topics[1:]]},
        confidence="medium"
    )

    # ── Step 2: 钩子生成（结合知识库） ──
    chain.add(
        "钩子设计",
        "参考知识库「钩子写法」：提问式/故事式/数据式/对比式/情绪式，先确定开头策略",
        confidence="high"
    )

    hook_result, _ = exec_tool("hook_generator", {
        "topic": selected_topic,
        "style": "auto",
        "platform": platform,
        "count": 3
    })

    hooks = hook_result.get("hooks", [])
    if hooks:
        primary_hook = hooks[0].get("hook", "")
        hook_type = hooks[0].get("style", "提问式")
        chain.add(
            "钩子选定",
            f"选择「{hook_type}」钩子：{primary_hook[:30]}...",
            {"hook": primary_hook, "type": hook_type, "alternatives": [h.get("hook","") for h in hooks[1:]]},
            confidence="high"
        )
    else:
        primary_hook = f"关于{topic}，你必须知道的几件事"
        hook_type = "提问式"
        chain.add("钩子选定", "使用默认提问式钩子", {"hook": primary_hook}, confidence="low")

    # ── Step 3: 脚本生成 ──
    chain.add(
        "脚本创作",
        f"根据「{selected_topic}」+「{hook_type}」钩子，生成完整脚本（开头+正文+结尾）",
        confidence="medium"
    )

    script_result, _ = exec_tool("content", {
        "action": "create",
        "topic": selected_topic,
        "platform": platform,
        "hook": primary_hook,
        "drug_context": drug_context,
    })

    script = script_result.get("script", "")
    title = script_result.get("title", "")
    
    chain.add(
        "脚本生成",
        f"生成标题：「{title}」，脚本长度 {len(script)} 字",
        {"title": title, "script_length": len(script), "preview": script[:100] + "..."},
        confidence="medium"
    )

    # ── Step 4: 合规审核（反馈循环） ──
    chain.add(
        "合规预审",
        f"对脚本进行语义优先审核：检查疾病域、药品类别、平台规则",
        confidence="high"
    )

    max_retries = 2
    retry_count = 0
    final_compliance_result = None

    while retry_count <= max_retries:
        compliance_result, _ = exec_tool("compliance", {
            "action": "analyze",
            "content": script,
            "platform": platform,
        })

        violations = compliance_result.get("guardrail_results", [])
        score_dict = compliance_result.get("compliance_score", {})
        compliance_score = score_dict.get("guardrail_score", 0) if isinstance(score_dict, dict) else (score_dict or 0)
        ai_evidence = compliance_result.get("evidence_for_ai", [])
        ai_reasoning = compliance_result.get("ai_reasoning_prompt", "")

        if retry_count == 0:
            chain.add(
                "初轮合规",
                f"发现 {len(violations)} 个 guardrail 违规，AI证据 {len(ai_evidence)} 条",
                {"violations": len(violations), "score": compliance_score, "ai_evidence_count": len(ai_evidence)},
                confidence="high" if violations else "medium"
            )

        if not violations and compliance_score >= 70:
            final_compliance_result = compliance_result
            chain.add(
                "合规通过",
                f"合规评分 {compliance_score}，审核通过",
                {"score": compliance_score, "ai_reasoning": ai_reasoning[:100]},
                confidence="high"
            )
            break
        else:
            # 失败 → 生成修正建议 → 重审
            retry_count += 1
            if retry_count > max_retries:
                chain.add(
                    "合规未通过",
                    f"经 {max_retries} 轮修正仍有余量风险，建议人工复核",
                    {"score": compliance_score, "remaining_issues": [v.get("matched_text") for v in violations]},
                    confidence="high"
                )
                final_compliance_result = compliance_result
                break

            # 生成修正版
            chain.add(
                "合规修正",
                f"第 {retry_count} 轮：根据 guardrail 反馈修正脚本",
                {"issue_count": len(violations)},
                confidence="medium"
            )

            # 简单修正：对每个 violation 做文本替换
            corrected_script = script
            critical_terms = {"根治": "控制", "治愈": "缓解", "无效退款": "联系客服", 
                             "永不复": "持续关注", "国家级": "高品质", "最佳": "优质"}
            for v in violations:
                for old, new in critical_terms.items():
                    if old in corrected_script:
                        corrected_script = corrected_script.replace(old, new)

            script = corrected_script

    # ── Step 5: 效果预测 ──
    chain.add(
        "效果预测",
        f"基于脚本内容、钩子类型、平台规则，预测互动率",
        confidence="medium"
    )

    predict_result, _ = exec_tool("content_predict", {
        "action": "score",
        "topic": selected_topic,
        "title": title,
        "platform": platform,
    })

    predicted_score = predict_result.get("score", 0)
    score_factors = predict_result.get("factors", [])

    chain.add(
        "预测完成",
        f"预测评分 {predicted_score}/100，影响因素：{', '.join(score_factors[:3])}",
        {"score": predicted_score, "factors": score_factors},
        confidence="medium"
    )

    # ── 最终输出 ──
    return {
        "status": "completed",
        "topic": selected_topic,
        "title": title,
        "hook": primary_hook,
        "hook_type": hook_type,
        "script": script,
        "compliance": {
            "score": final_compliance_result.get("compliance_score", 0) if final_compliance_result else 0,
            "violations": len(violations) if final_compliance_result else 0,
            "passed": len(violations) == 0 if final_compliance_result else False,
            "semantic_entities": final_compliance_result.get("semantic_entities", {}) if final_compliance_result else {},
        },
        "prediction": {
            "score": predicted_score,
            "factors": score_factors,
        },
        "reasoning_chain": chain.render(),
        "reasoning_data": chain.to_dict(),
        "platform": platform,
        "retry_count": retry_count,
    }


# ─────────────────────────────────────────
# 患者关护 pipeline
# ─────────────────────────────────────────
def patient_care_pipeline(session_id: str = None, segment: str = None) -> dict:
    """
    全链路患者关护：分群 → 会话分析 → 风险评估 → 工单升级
    """
    chain = ReasoningChain()

    if session_id:
        # 单患者分析
        chain.add("患者分群", f"查询患者 {session_id} 会话摘要", confidence="high")
        patient_result, _ = exec_tool("patient", {"action": "session_summary", "session_id": session_id})
        at_risk = [patient_result] if "error" not in patient_result else []
    else:
        # 批量分析：先获取分群
        chain.add("患者分群", "查询当前高风险分群患者，筛选需要关护的个体", confidence="high")
        patient_result, _ = exec_tool("patient", {"action": "list_segments"})
        
        # high_risk 列表直接来自 list_segments() 结果
        high_risk_patients = patient_result.get("high_risk", [])[:10]
        at_risk = []
        
        for session in high_risk_patients:
            sid = session.get("session_id", "")
            
            # 获取会话摘要（检查失联风险）
            summary_result, _ = exec_tool("patient", {"action": "session_summary", "session_id": sid})
            if "error" in summary_result:
                continue
            
            messages_count = summary_result.get("message_count", 0)
            last_message_age = summary_result.get("last_message_age_days", 0)
            risk_signals = []
            
            if last_message_age and last_message_age > 3:
                risk_signals.append(f"超过{last_message_age}天未回复")
            if messages_count < 3:
                risk_signals.append("会话深度不足")
            
            # 只有存在风险信号才列入关护
            if risk_signals:
                at_risk.append({
                    "session_id": sid,
                    "patient_name": session.get("patient_name", "未知"),
                    "risk_signals": risk_signals,
                    "last_activity": last_message_age,
                })
    
    chain.add(
        "风险识别",
        f"发现 {len(at_risk)} 个高风险患者需要关护",
        {"at_risk_count": len(at_risk), "patients": [p.get("patient_name") for p in at_risk[:3]]},
        confidence="high"
    )

    # Step 3: 生成干预计划
    interventions = []
    for patient in at_risk:
        primary_signal = patient["risk_signals"][0] if patient["risk_signals"] else "待跟进"
        
        if "未回复" in primary_signal:
            action = "发送随访消息，询问近况"
            priority = "high"
        elif "深度不足" in primary_signal:
            action = "补充健康教育内容，提升参与度"
            priority = "medium"
        else:
            action = "发送关护提醒"
            priority = "normal"

        interventions.append({
            "patient_name": patient["patient_name"],
            "session_id": patient["session_id"],
            "action": action,
            "priority": priority,
            "reason": primary_signal,
        })

    chain.add(
        "干预计划",
        f"生成 {len(interventions)} 个个性化干预计划",
        {"interventions": interventions[:3]},
        confidence="medium"
    )

    # Step 4: 创建工单（如需要）
    tickets_created = 0
    for intervention in interventions:
        if intervention["priority"] in ("high", "medium"):
            ticket_result, _ = exec_tool("patient", {
                "action": "create_ticket",
                "patient_id": intervention["session_id"],
                "issue": intervention["action"],
                "priority": intervention["priority"],
            })
            if "error" not in ticket_result:
                tickets_created += 1

    chain.add(
        "工单创建",
        f"为高优先级干预创建 {tickets_created} 个工单",
        {"tickets": tickets_created},
        confidence="high"
    )

    return {
        "status": "completed",
        "patients_analyzed": len(at_risk),
        "interventions": interventions,
        "tickets_created": tickets_created,
        "reasoning_chain": chain.render(),
        "reasoning_data": chain.to_dict(),
    }


# ─────────────────────────────────────────
# 竞品分析 pipeline
# ─────────────────────────────────────────
def competitor_intel_pipeline(competitor_name: str = None, product: str = None) -> dict:
    """
    全链路竞品分析：竞品数据 → 内容动态 → KOL 策略
    """
    chain = ReasoningChain()

    # Step 1: 竞品基础数据
    chain.add("竞品数据查询", "查询目标竞品的价格、评分、评论量等基础数据", confidence="high")
    
    comp_result, _ = exec_tool("competitor", {
        "action": "analyze" if competitor_name else "overview",
        "competitor": competitor_name,
        "product": product,
    })

    products = comp_result.get("products", [])
    latest_analysis = comp_result.get("latest_analysis", [])

    if not products and not latest_analysis:
        chain.add("无数据", "竞品数据库中暂无该竞品记录", {}, confidence="low")
        return {
            "status": "no_data",
            "reasoning_chain": chain.render(),
            "advice": "建议先通过内容监控收集竞品数据",
        }

    # Step 2: 价格与评分对比
    chain.add(
        "价格分析",
        f"对比 {len(products)} 个竞品的价格和评分",
        {"products": [(p.get("name"), p.get("price"), p.get("rating")) for p in products[:3]]},
        confidence="high"
    )

    # Step 3: 内容策略分析
    chain.add("内容策略", "分析竞品近期内容主题和互动效果", confidence="medium")

    content_result, _ = exec_tool("trend_aware_content", {
        "action": "competitor_content",
        "competitor": competitor_name,
        "limit": 5,
    })

    competitor_content = content_result.get("content_items", [])

    chain.add(
        "内容动态",
        f"发现竞品近期 {len(competitor_content)} 条内容，主题集中在：{', '.join([c.get('topic', '') for c in competitor_content[:3]])}",
        {"content_count": len(competitor_content)},
        confidence="medium"
    )

    # Step 4: KOL 合作策略推断
    chain.add("KOL策略推断", "根据竞品内容和平台分布，推断其 KOL 合作策略", confidence="low")

    # Step 5: 建议
    top_product = products[0] if products else None
    
    recommendations = []
    if top_product:
        price = top_product.get("price", 0)
        rating = top_product.get("rating", 0)
        
        if rating >= 4.5:
            recommendations.append("竞品评分高（≥4.5），需在内容专业性上差异化")
        if price:
            recommendations.append(f"竞品价格带宽 ¥{price * 0.8:.0f}~¥{price * 1.2:.0f}，结合定价策略调整")

    chain.add(
        "策略建议",
        f"生成 {len(recommendations)} 条应对建议",
        {"recommendations": recommendations},
        confidence="medium"
    )

    return {
        "status": "completed",
        "products": products[:5],
        "competitor_content": competitor_content,
        "recommendations": recommendations,
        "reasoning_chain": chain.render(),
        "reasoning_data": chain.to_dict(),
    }


# ─────────────────────────────────────────
# 主入口
# ─────────────────────────────────────────
def orchestrate(action: str, **kwargs) -> dict:
    """统一入口"""
    if action == "content_pipeline":
        return content_creation_pipeline(
            topic=kwargs.get("topic"),
            platform=kwargs.get("platform", "douyin"),
            drug_context=kwargs.get("drug_context"),
        )
    elif action == "patient_care":
        return patient_care_pipeline(
            session_id=kwargs.get("session_id"),
            segment=kwargs.get("segment"),
        )
    elif action == "competitor_intel":
        return competitor_intel_pipeline(
            competitor_name=kwargs.get("competitor"),
            product=kwargs.get("product"),
        )
    else:
        return {
            "error": f"Unknown action: {action}",
            "available": ["content_pipeline", "patient_care", "competitor_intel"],
        }


def _parse_args():
    if len(sys.argv) > 1:
        try:
            return json.loads(sys.argv[1])
        except json.JSONDecodeError:
            return {"action": sys.argv[1], **dict(a.split("=") for a in sys.argv[2:] if "=" in a)}
    if not sys.stdin.isatty():
        data = sys.stdin.read().strip()
        if data:
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                pass
    return {}


if __name__ == "__main__":
    args = _parse_args()
    result = orchestrate(
        action=args.get("action", "content_pipeline"),
        topic=args.get("topic"),
        platform=args.get("platform", "douyin"),
        drug_context=args.get("drug_context"),
        session_id=args.get("session_id"),
        segment=args.get("segment"),
        competitor=args.get("competitor"),
        product=args.get("product"),
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))