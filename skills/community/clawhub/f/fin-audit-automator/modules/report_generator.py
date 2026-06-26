#!/usr/bin/env python3
"""
审计报告生成模块
Audit Report Generator Module
"""

from typing import List, Dict, Any
from datetime import datetime


def generate_audit_report(findings: List[Dict[str, Any]], period: str = "2026-Q1") -> str:
    """
    生成符合监管格式的审计底稿
    """
    report_lines = []
    
    # 报告标题
    report_lines.append(f"# 金融合规审计报告 ({period})")
    report_lines.append(f"\n**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append(f"**审计期间**: {period}")
    report_lines.append(f"**发现项数**: {len(findings)}")
    
    # 总体结论
    report_lines.append("\n## 1. 总体结论\n")
    if len(findings) == 0:
        report_lines.append("本期未发现重大合规风险。")
    else:
        high_count = sum(1 for f in findings if f.get('severity') == 'HIGH')
        medium_count = sum(1 for f in findings if f.get('severity') == 'MEDIUM')
        low_count = sum(1 for f in findings if f.get('severity') == 'LOW')
        
        report_lines.append(f"本期发现 **{len(findings)}** 项潜在风险，需重点关注。")
        report_lines.append(f"- 高风险: {high_count} 项")
        report_lines.append(f"- 中风险: {medium_count} 项")
        report_lines.append(f"- 低风险: {low_count} 项")
    
    # 风险明细
    report_lines.append("\n## 2. 风险明细\n")
    if findings:
        for i, item in enumerate(findings, 1):
            report_lines.append(f"### 2.{i} {item.get('type', '未知类型')}")
            report_lines.append(f"- **风险等级**: {item.get('severity', 'UNKNOWN')}")
            report_lines.append(f"- **涉及账户**: {item.get('account_id', 'N/A')}")
            report_lines.append(f"- **描述**: {item.get('description', '无描述')}")
            report_lines.append(f"- **建议**: {_get_recommendation(item)}")
            report_lines.append("")
    else:
        report_lines.append("无风险项。")
    
    # 统计分析
    report_lines.append("\n## 3. 统计分析\n")
    report_lines.append("| 风险类型 | 数量 | 占比 |")
    report_lines.append("|----------|------|------|")
    
    type_counts = {}
    for f in findings:
        t = f.get('type', 'UNKNOWN')
        type_counts[t] = type_counts.get(t, 0) + 1
    
    for t, count in type_counts.items():
        pct = f"{count/len(findings)*100:.1f}%" if findings else "0%"
        report_lines.append(f"| {t} | {count} | {pct} |")
    
    if not findings:
        report_lines.append("| 无 | 0 | 0% |")
    
    # 整改建议
    report_lines.append("\n## 4. 整改建议\n")
    report_lines.append("1. 对高风险项应立即进行人工复核")
    report_lines.append("2. 完善相关内控制度和操作流程")
    report_lines.append("3. 加强员工合规培训")
    report_lines.append("4. 定期更新规则库和风险模型")
    
    # 签字确认
    report_lines.append("\n## 5. 签字确认\n")
    report_lines.append("```")
    report_lines.append("审计员：________________  日期：________________")
    report_lines.append("复核人：________________  日期：________________")
    report_lines.append("负责人：________________  日期：________________")
    report_lines.append("```")
    
    # 免责声明
    report_lines.append("\n---")
    report_lines.append("*本报告由AI辅助生成，仅供内部参考，不作为正式审计意见。*")
    
    return "\n".join(report_lines)


def _get_recommendation(finding: Dict[str, Any]) -> str:
    """根据风险类型生成建议"""
    recommendations = {
        "HIGH_FREQUENCY": "核实交易背景，确认是否存在异常交易行为",
        "ROUND_AMOUNT_PATTERN": "检查交易对手和资金来源，核实是否存在洗钱风险",
        "STRUCTURING": "高度关注，建议上报反洗钱部门",
        "LARGE_CASH_TRANSACTION": "核实大额交易的合法性和必要性",
        "UNUSUAL_HOURS": "了解异常时段交易原因，评估风险"
    }
    return recommendations.get(finding.get('type', ''), "建议人工复核")


def generate_summary(findings: List[Dict[str, Any]]) -> Dict[str, Any]:
    """生成摘要统计"""
    return {
        "total_findings": len(findings),
        "high_risk": sum(1 for f in findings if f.get('severity') == 'HIGH'),
        "medium_risk": sum(1 for f in findings if f.get('severity') == 'MEDIUM'),
        "low_risk": sum(1 for f in findings if f.get('severity') == 'LOW'),
        "risk_types": list(set(f.get('type', 'UNKNOWN') for f in findings)),
        "affected_accounts": list(set(f.get('account_id', '') for f in findings if f.get('account_id')))
    }


if __name__ == "__main__":
    # 测试
    test_findings = [
        {"type": "HIGH_FREQUENCY", "severity": "HIGH", "account_id": "A001", "description": "1小时内5笔大额交易"},
        {"type": "ROUND_AMOUNT_PATTERN", "severity": "MEDIUM", "account_id": "A002", "description": "90%交易为整数金额"},
        {"type": "STRUCTURING", "severity": "HIGH", "account_id": "A003", "description": "疑似结构化交易"}
    ]
    
    report = generate_audit_report(test_findings, "2026-Q1")
    print(report)
