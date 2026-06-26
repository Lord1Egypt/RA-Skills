#!/usr/bin/env python3
"""
城投贸易风控扫描器
输入：合同文本 或 对手方名称
输出：风险评估报告

用法：
python3 risk_scanner.py --type contract --input "合同文本..."
python3 risk_scanner.py --type company --input "公司名称"
"""

import json
import sys
import re
from datetime import datetime
from typing import Optional

# ============== 风险特征库 ==============

FINANCING_TRADE_PATTERNS = [
    # 回购相关
    r"回购.{0,10}(股权|资产|货物|产品)",
    r"(承诺|保证).{0,10}(回购|收购|兜底)",
    r"到期.{0,10}(回购|收购|返还)",
    
    # 差额补足相关
    r"差额.{0,10}(补足|补偿|支付)",
    r"(保证|承诺).{0,10}(收益|回报|利息)",
    r"年化.{0,10}(收益|回报|利息)",
    
    # 增信相关
    r"(抵押|质押|保证|担保).{0,10}(条款|协议|承诺)",
    r"第三方.{0,10}(增信|担保|保证)",
    
    # 融资特征
    r"(融资|借贷|贷款|借款).{0,10}(合同|协议|安排)",
    r"资金.{0,10}(拆借|拆出|拆入|借贷)",
    
    # 走单不走货特征
    r"(上游|下游|供应商|客户).{0,10}(同一|关联|一致)",
    r"(货权|货物|存货|库存).{0,10}(转移|交付|交接).{0,10}(无|未|不)",
    r"仅.{0,10}(收据|凭证|单据).{0,10}(无|未|不).{0,10}(实际|真实)",
]

UNSCAFFOLD_TRADE_PATTERNS = [
    # 空单特征
    r"(空单|走单|虚构|虚假).{0,10}(贸易|交易|业务|合同)",
    r"无.{0,10}(实际|真实).{0,10}(货物|货权|交付|物流)",
    r"(合同|协议).{0,10}(无|未|不).{0,10}(实际|真实)",
    
    # 无商业实质
    r"无.{0,10}(商业|业务|经营).{0,10}(实质|背景|目的)",
    r"仅为.{0,10}(融资|借贷|套利|套取)",
]

GOVERNMENT_TEN_NO = [
    {
        "number": "一",
        "title": "不准开展融资性贸易",
        "description": "严禁假借供应链之名，实际提供资金"
    },
    {
        "number": "二", 
        "title": "不准开展空转、走单贸易",
        "description": "严禁无真实货权流转的虚假贸易"
    },
    {
        "number": "三",
        "title": "不准超越主业开展贸易",
        "description": "严禁超范围、超能力开展贸易业务"
    },
    {
        "number": "四",
        "title": "不准超负债率开展贸易",
        "description": "严禁超出财务承受能力开展贸易"
    },
    {
        "number": "五",
        "title": "不准对资信不足的企业赊销",
        "description": "严禁对资信不足企业提供信用销售"
    },
    {
        "number": "六",
        "title": "不准无商业实质办理保理",
        "description": "严禁无真实贸易背景办理保理业务"
    },
    {
        "number": "七",
        "title": "不准违规拆借资金",
        "description": "严禁违规将贸易资金用于借贷"
    },
    {
        "number": "八",
        "title": "不准违规提供担保",
        "description": "严禁违规为他人提供担保"
    },
    {
        "number": "九",
        "title": "不准虚假贸易合同套取融资",
        "description": "严禁以虚假贸易合同套取银行融资"
    },
    {
        "number": "十",
        "title": "不准将贸易业务异化为融资工具",
        "description": "严禁将贸易业务变成融资通道"
    }
]


def scan_contract(text: str) -> dict:
    """扫描合同文本，返回风险评估"""
    
    findings = {
        "scan_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "risk_level": "低",
        "financing_risks": [],
        "empty_trade_risks": [],
        "matched_rules": [],
        "recommendations": []
    }
    
    # 检查融资性贸易特征
    for i, pattern in enumerate(FINANCING_TRADE_PATTERNS):
        matches = re.findall(pattern, text)
        if matches:
            # 处理 capture group 的情况，提取文本片段
            clean_matches = []
            for m in matches[:3]:
                if isinstance(m, tuple):
                    clean_matches.append(' '.join(str(x) for x in m if x))
                else:
                    clean_matches.append(str(m))
            findings["financing_risks"].append({
                "pattern_id": i + 1,
                "pattern": pattern,
                "matches": clean_matches,
                "rule": "融资性贸易特征"
            })
            findings["matched_rules"].append(f"融资性贸易特征-{i+1}")
    
    # 检查空转走单特征
    for i, pattern in enumerate(UNSCAFFOLD_TRADE_PATTERNS):
        matches = re.findall(pattern, text)
        if matches:
            clean_matches = []
            for m in matches[:3]:
                if isinstance(m, tuple):
                    clean_matches.append(' '.join(str(x) for x in m if x))
                else:
                    clean_matches.append(str(m))
            findings["empty_trade_risks"].append({
                "pattern_id": i + 1,
                "pattern": pattern,
                "matches": clean_matches,
                "rule": "空转走单贸易特征"
            })
            findings["matched_rules"].append(f"空转走单特征-{i+1}")
    
    # 综合风险等级
    total_risks = len(findings["financing_risks"]) + len(findings["empty_trade_risks"])
    if total_risks >= 3:
        findings["risk_level"] = "高"
    elif total_risks >= 1:
        findings["risk_level"] = "中"
    
    # 生成建议
    if findings["financing_risks"]:
        findings["recommendations"].append(
            "发现融资性贸易特征，建议："
            "1) 重新审视交易结构是否实质为提供资金"
            "2) 检查是否有回购/差额补足条款"
            "3) 评估是否符合国资监管要求"
        )
    
    if findings["empty_trade_risks"]:
        findings["recommendations"].append(
            "发现空转走单风险，建议："
            "1) 核实货权凭证是否真实完整"
            "2) 确认货物实际交付情况"
            "3) 检查贸易是否有真实商业实质"
        )
    
    if not findings["matched_rules"]:
        findings["recommendations"].append("未发现明显违规特征，但建议进行完整合规审查")
    
    return findings


def generate_contract_report(findings: dict, contract_name: str = "未命名合同") -> str:
    """生成合同审查报告"""
    
    risk_emoji = {"高": "🔴", "中": "🟡", "低": "🟢"}
    
    report = f"""
================================================================================
                        合同风险审查报告
================================================================================

合同名称：{contract_name}
审查时间：{findings['scan_time']}
风险等级：{risk_emoji.get(findings['risk_level'], '⚪')} {findings['risk_level']}

--------------------------------------------------------------------------------
一、风险检测结果
--------------------------------------------------------------------------------

"""
    
    if findings["financing_risks"]:
        report += f"""【融资性贸易风险】发现 {len(findings['financing_risks'])} 项

"""
        for risk in findings["financing_risks"]:
            # matches 可能是 tuple 或 str，需要统一处理
            match_texts = []
            for m in risk['matches']:
                if isinstance(m, tuple):
                    match_texts.append(' '.join(str(x) for x in m))
                else:
                    match_texts.append(str(m))
            report += f"""  风险 #{risk['pattern_id']}
  匹配模式：{risk['pattern']}
  示例文本：{', '.join(match_texts[:3])}
  
"""
    
    if findings["empty_trade_risks"]:
        report += f"""【空转走单风险】发现 {len(findings['empty_trade_risks'])} 项

"""
        for risk in findings["empty_trade_risks"]:
            match_texts = []
            for m in risk['matches']:
                if isinstance(m, tuple):
                    match_texts.append(' '.join(str(x) for x in m))
                else:
                    match_texts.append(str(m))
            report += f"""  风险 #{risk['pattern_id']}
  匹配模式：{risk['pattern']}
  示例文本：{', '.join(match_texts[:3])}
  
"""
    
    if not findings["financing_risks"] and not findings["empty_trade_risks"]:
        report += """【检测结果】未发现明显融资性贸易或空转走单特征

"""
    
    report += """--------------------------------------------------------------------------------
二、对应监管红线
--------------------------------------------------------------------------------

"""
    
    if findings["financing_risks"]:
        for no in GOVERNMENT_TEN_NO[:2]:
            report += f"  十不准第{no['number']}条：{no['title']}\n"
            report += f"    {no['description']}\n\n"
    
    report += """--------------------------------------------------------------------------------
三、修改建议
--------------------------------------------------------------------------------

"""
    
    for i, rec in enumerate(findings["recommendations"], 1):
        report += f"  {i}. {rec}\n"
    
    report += f"""
================================================================================
                            报告完毕
================================================================================
本报告仅供参考，不构成法律意见。重大决策请咨询专业律师。
生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

    return report


if __name__ == "__main__":
    # 示例用法
    sample_contract = """
    购销合同
    
    第一条：本合同为甲方向乙方采购钢材的购销合同...
    
    第七条：甲方承诺在12个月后按原价回购乙方持有的剩余货物...
    
    第八条：如乙方未能按时还款，甲方同意差额补足...
    """
    
    print("城投贸易风控扫描器")
    print("=" * 40)
    
    result = scan_contract(sample_contract)
    report = generate_contract_report(result, "钢材购销合同示例")
    print(report)
