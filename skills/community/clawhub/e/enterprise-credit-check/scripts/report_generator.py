#!/usr/bin/env python3
"""
企业征信核查报告生成器
"""
from datetime import datetime
from typing import Dict, Any
from scripts.risk_calculator import get_risk_emoji


def generate_credit_report(
    enterprise_info: Dict[str, Any],
    check_results: Dict[str, Any],
    risk_result: Dict[str, Any]
) -> str:
    """
    生成企业征信核查报告
    
    Args:
        enterprise_info: 企业基本信息
        check_results: 五维核查结果
        risk_result: 风险评分结果
    
    Returns:
        格式化报告文本
    """
    now = datetime.now()
    report_id = f"EC-{now.strftime('%Y%m%d')}-{now.strftime('%H%M%S')}"
    
    # 获取各维度详情
    pbc = check_results.get("pbc_credit", {})
    biz = check_results.get("business_status", {})
    exec_data = check_results.get("execution", {})
    penalty = check_results.get("penalty", {})
    litigation = check_results.get("litigation", {})
    
    # 构建报告
    report = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
       企业征信核查报告
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

报告编号：{report_id}
查询时间：{now.strftime('%Y年%m月%d日 %H:%M')}
查询企业：{enterprise_info.get('name', '未知')}
统一社会信用代码：{enterprise_info.get('uscc', '未知')}
注册资本：{enterprise_info.get('registered_capital', '未知')}万元
成立日期：{enterprise_info.get('establishment_date', '未知')}
经营范围：{enterprise_info.get('business_scope', '未知')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【重要声明】
本报告数据来源于政府官方渠道，仅供参考。
最终决策请结合其他信息综合判断。
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# 一、核查概况

| 项目 | 内容 |
|------|------|
| 企业名称 | {enterprise_info.get('name', '未知')} |
| 统一社会信用代码 | {enterprise_info.get('uscc', '未知')} |
| 注册资本 | {enterprise_info.get('registered_capital', '未知')}万元 |
| 成立日期 | {enterprise_info.get('establishment_date', '未知')} |

## 1.1 综合评分

| 维度 | 权重 | 得分 | 风险 |
|------|------|------|------|
| 人行征信 | 40% | {risk_result['component_scores']['pbc_credit']} | {get_risk_emoji(get_risk_level(risk_result['component_scores']['pbc_credit']))} |
| 经营状态 | 25% | {risk_result['component_scores']['business_status']} | {get_risk_emoji(get_risk_level(risk_result['component_scores']['business_status']))} |
| 司法执行 | 20% | {risk_result['component_scores']['execution']} | {get_risk_emoji(get_risk_level(risk_result['component_scores']['execution']))} |
| 行政处罚 | 10% | {risk_result['component_scores']['penalty']} | {get_risk_emoji(get_risk_level(risk_result['component_scores']['penalty']))} |
| 诉讼记录 | 5% | {risk_result['component_scores']['litigation']} | {get_risk_emoji(get_risk_level(risk_result['component_scores']['litigation']))} |
| **综合评分** | **100%** | **{risk_result['total_score']}** | {get_risk_emoji(risk_result['risk_level'])} |

## 1.2 风险等级

**{get_risk_emoji(risk_result['risk_level'])}{get_risk_level_text(risk_result['risk_level'])}**

{get_risk_summary(risk_result)}

---

# 二、人行征信（40%）

| 核查项 | 结果 |
|--------|------|
| 信用评级 | {pbc.get('rating', '未知')} |
| 信贷记录 | {pbc.get('loan_count', 0)}笔 |
| 逾期记录 | {'无' if pbc.get('overdue', 0) == 0 else f'有-{pbc.get("overdue")}次'} |
| 担保信息 | {pbc.get('guarantee_count', 0)}笔 |

**征信结论**：{get_pbc_conclusion(pbc)}

---

# 三、经营状态（25%）

| 核查项 | 结果 |
|--------|------|
| 经营状态 | {biz.get('status', '未知')} |
| 经营异常 | {'无' if not biz.get('abnormal') else '有'} |
| 严重违法失信 | {'无' if not biz.get('severe_illegal') else '有'} |
| 年报公示 | {'已报' if biz.get('annual_report') else '未报'} |

**经营结论**：{get_biz_conclusion(biz)}

---

# 四、司法执行（20%）

| 核查项 | 结果 |
|--------|------|
| 失信被执行人 | {'无' if not exec_data.get('dishonest') else f'有-{exec_data.get("dishonest_count", 0)}条'} |
| 被执行人 | {'无' if not exec_data.get('execution') else f'有-{exec_data.get("execution_count", 0)}条'} |
| 限制高消费 | {'无' if not exec_data.get('consumption_restriction') else '有'} |

**执行结论**：{get_exec_conclusion(exec_data)}

---

# 五、行政处罚（10%）

| 核查项 | 结果 |
|--------|------|
| 行政处罚 | {'无' if not penalty.get('has_penalty') else f'有-{penalty.get("penalty_count", 0)}条'} |
| 重大处罚 | {'无' if not penalty.get('major_penalty') else '有'} |

**处罚结论**：{get_penalty_conclusion(penalty)}

---

# 六、诉讼记录（5%）

| 核查项 | 结果 |
|--------|------|
| 总诉讼数 | {litigation.get('total_cases', 0)}件 |
| 知识产权纠纷 | {litigation.get('ip_disputes', 0)}件 |

**诉讼结论**：{get_litigation_conclusion(litigation)}

---

# 七、风险汇总

## 7.1 核查结果摘要

{get_check_summary(check_results)}

---

# 八、使用建议

## 8.1 综合建议

| 建议等级 | 条件 |
|----------|------|
| 🟢 建议推进 | 综合评分≥80分 |
| 🟡 谨慎推进 | 综合评分60-79分 |
| 🔴 不建议推进 | 综合评分<60分 |

**本次建议**：{get_recommendation(risk_result)}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【免责声明】
本报告数据来源于政府官方渠道，仅供参考。
最终决策请结合其他信息综合判断。
如需正式征信报告，请通过正规渠道向征信机构申请。

【联系咨询】
需要信用修复或深度尽调，请联系老胡企业微信：hutian@mantuzhisheng.cn
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    return report


def get_risk_level(score: int) -> str:
    """根据分数获取风险等级"""
    if score >= 80:
        return "low"
    elif score >= 60:
        return "medium"
    elif score >= 40:
        return "high"
    else:
        return "critical"


def get_risk_level_text(level: str) -> str:
    """获取风险等级中文描述"""
    text_map = {
        "low": "低风险",
        "medium": "中等风险",
        "high": "较高风险",
        "critical": "高风险"
    }
    return text_map.get(level, "未知")


def get_risk_summary(risk_result: dict) -> str:
    """获取风险摘要"""
    level = risk_result["risk_level"]
    score = risk_result["total_score"]
    
    if level == "low":
        return f"该企业信用状况良好，综合评分{score}分，五维核查均无明显异常。"
    elif level == "medium":
        return f"该企业存在轻微风险项，综合评分{score}分，建议谨慎推进。"
    elif level == "high":
        return f"该企业存在明显风险项，综合评分{score}分，建议充分评估后再决定。"
    else:
        return f"该企业存在重大风险项，综合评分{score}分，不建议推进业务。"


def get_pbc_conclusion(pbc: dict) -> str:
    """获取人行征信结论"""
    rating = pbc.get("rating", "未知")
    if rating in ["次级", "可疑", "损失"]:
        return "🔴 异常"
    elif rating == "关注":
        return "🟡 关注"
    else:
        return "🟢 正常"


def get_biz_conclusion(biz: dict) -> str:
    """获取经营状态结论"""
    if biz.get("severe_illegal"):
        return "🔴 严重"
    elif biz.get("abnormal"):
        return "🟡 异常"
    else:
        return "🟢 正常"


def get_exec_conclusion(exec_data: dict) -> str:
    """获取司法执行结论"""
    if exec_data.get("dishonest"):
        return "🔴 失信"
    elif exec_data.get("execution") or exec_data.get("consumption_restriction"):
        return "🟡 有记录"
    else:
        return "🟢 无记录"


def get_penalty_conclusion(penalty: dict) -> str:
    """获取行政处罚结论"""
    if penalty.get("major_penalty"):
        return "🔴 重大"
    elif penalty.get("has_penalty"):
        return "🟡 轻微"
    else:
        return "🟢 无"


def get_litigation_conclusion(litigation: dict) -> str:
    """获取诉讼记录结论"""
    if litigation.get("ip_disputes", 0) > 0:
        return "🔴 异常"
    elif litigation.get("total_cases", 0) > 10:
        return "🟡 批量"
    elif litigation.get("total_cases", 0) > 0:
        return "🟡 正常"
    else:
        return "🟢 无"


def get_check_summary(check_results: dict) -> str:
    """获取核查结果摘要"""
    summaries = []
    
    pbc = check_results.get("pbc_credit", {})
    if pbc.get("rating") != "正常":
        summaries.append(f"- 人行征信：{pbc.get('rating')}评级")
    
    biz = check_results.get("business_status", {})
    if biz.get("abnormal"):
        summaries.append("- 经营状态：存在异常记录")
    if biz.get("severe_illegal"):
        summaries.append("- 经营状态：严重违法失信")
    
    exec_data = check_results.get("execution", {})
    if exec_data.get("dishonest"):
        summaries.append("- 司法执行：存在失信记录")
    if exec_data.get("execution"):
        summaries.append("- 司法执行：存在被执行记录")
    
    penalty = check_results.get("penalty", {})
    if penalty.get("has_penalty"):
        summaries.append(f"- 行政处罚：存在{penalty.get('penalty_count', 0)}条处罚记录")
    
    litigation = check_results.get("litigation", {})
    if litigation.get("total_cases", 0) > 0:
        summaries.append(f"- 诉讼记录：共{litigation.get('total_cases', 0)}件")
    if litigation.get("ip_disputes", 0) > 0:
        summaries.append(f"- 知识产权纠纷：{litigation.get('ip_disputes', 0)}件")
    
    if not summaries:
        return "五维核查均未发现明显风险项。"
    
    return "\n".join(summaries)


def get_recommendation(risk_result: dict) -> str:
    """获取综合建议"""
    score = risk_result["total_score"]
    level = risk_result["risk_level"]
    
    if level == "critical":
        return "🔴 不建议推进"
    elif score >= 80:
        return "🟢 建议推进"
    elif score >= 60:
        return "🟡 谨慎推进"
    else:
        return "🔴 不建议推进"
