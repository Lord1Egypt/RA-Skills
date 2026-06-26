#!/usr/bin/env python3
"""
ContractAI Pro - 专业合同审查脚本
功能：智能识别合同风险、提供修改建议、生成审查报告
"""

import argparse
import sys
import os
import re
from datetime import datetime
from typing import List, Dict, Tuple

# 法律风险规则库
RISK_RULES = [
    {
        "id": "R001",
        "name": "违约金比例过高",
        "level": "high",
        "category": "违约责任",
        "patterns": [r"违约金.*[3-9][0-9]%", r"违约金.*百分之[三四五六七八九十]"],
        "risk": "违约金比例超过30%可能被法院认定为过高而予以调减",
        "suggestion": "将违约金比例调整为合同总价的15%-20%，或约定违约金不足以弥补实际损失时另行赔偿差额",
        "law_ref": "《民法典》第585条：约定的违约金低于造成的损失的，人民法院或者仲裁机构可以根据当事人的请求予以增加；约定的违约金过分高于造成的损失的，人民法院或者仲裁机构可以根据当事人的请求予以适当减少"
    },
    {
        "id": "R002",
        "name": "单方解约权不对等",
        "level": "high",
        "category": "合同解除",
        "patterns": [r"甲方有权随时解除", r"仅甲方有权解除", r"乙方不得解除"],
        "risk": "严重违反合同法公平原则，可能被认定为无效格式条款",
        "suggestion": "改为双方均享有解除权，或约定解除条件平等适用于双方",
        "law_ref": "《民法典》第497条：提供格式条款一方不合理地免除或者减轻其责任、加重对方责任、限制对方主要权利，该格式条款无效"
    },
    {
        "id": "R003",
        "name": "争议解决地不利",
        "level": "medium",
        "category": "争议解决",
        "patterns": [r"甲方所在地.*法院", r"由甲方所在地", r"被告所在地法院"],
        "risk": "增加维权成本，可能存在地方保护主义风险",
        "suggestion": "建议改为原告所在地、合同履行地或双方协商选择",
        "law_ref": "《民事诉讼法》第35条：合同或者其他财产权益纠纷的当事人可以书面协议选择被告住所地、合同履行地、合同签订地、原告住所地、标的物所在地等与争议有实际联系的地点的人民法院管辖"
    },
    {
        "id": "R004",
        "name": "保密期限过长",
        "level": "medium",
        "category": "保密条款",
        "patterns": [r"永久保密", r"保密期限.*永久", r"无限期保密"],
        "risk": "保密义务过重，实际履行困难",
        "suggestion": "建议保密期限为合同终止后2-3年",
        "law_ref": "司法实践中，商业秘密保密期限一般不超过5年"
    },
    {
        "id": "R005",
        "name": "试用期超过法定期限",
        "level": "high",
        "category": "劳动合同",
        "patterns": [r"试用期.*6个月.*合同.*1年", r"试用期.*3个月.*合同.*1年"],
        "risk": "试用期约定违反《劳动合同法》，超出部分无效",
        "suggestion": "劳动合同期限1年以上不满3年的，试用期不得超过2个月；3年以上固定期限和无固定期限的劳动合同，试用期不得超过6个月",
        "law_ref": "《劳动合同法》第19条"
    },
    {
        "id": "R006",
        "name": "竞业限制补偿过低",
        "level": "medium",
        "category": "劳动合同",
        "patterns": [r"竞业限制补偿.*[0-2][0-9]%", r"补偿.*工资的.*[0-2][0-9]%"],
        "risk": "竞业限制经济补偿低于法定标准，可能被认定无效",
        "suggestion": "建议竞业限制补偿不低于劳动合同解除或终止前十二个月平均工资的30%",
        "law_ref": "《最高人民法院关于审理劳动争议案件适用法律问题的解释（一）》第36条"
    },
    {
        "id": "R007",
        "name": "免责条款过于宽泛",
        "level": "high",
        "category": "免责条款",
        "patterns": [r"概不负责", r"不承担任何责任", r"无论何种情况均不负责"],
        "risk": "免责条款过于宽泛，可能因排除对方主要权利而无效",
        "suggestion": "明确免责的具体情形，避免使用绝对化表述",
        "law_ref": "《民法典》第506条：合同中的下列免责条款无效：（一）造成对方人身损害的；（二）因故意或者重大过失造成对方财产损失的"
    },
    {
        "id": "R008",
        "name": "缺少必备条款",
        "level": "medium",
        "category": "合同完整性",
        "patterns": [],
        "risk": "合同必备条款缺失可能导致合同不成立或产生争议",
        "suggestion": "补充合同标的、数量、价款、履行期限、违约责任、争议解决等必备条款",
        "law_ref": "《民法典》第470条：合同的内容由当事人约定，一般包括下列条款：（一）当事人的姓名或者名称和住所；（二）标的；（三）数量；（四）质量；（五）价款或者报酬；（六）履行期限、地点和方式；（七）违约责任；（八）解决争议的方法"
    }
]

def read_contract(file_path: str) -> str:
    """读取合同文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"❌ 读取文件失败: {e}")
        sys.exit(1)

def find_risks(content: str) -> List[Dict]:
    """查找合同中的风险"""
    risks = []
    lines = content.split('\n')
    seen_rule_line = set()  # 避免同一规则在同一行重复匹配
    
    for rule in RISK_RULES:
        if not rule['patterns']:
            continue
            
        for pattern in rule['patterns']:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                # 找到匹配的行号
                line_num = 0
                for i, line in enumerate(lines, 1):
                    if match.group() in line:
                        line_num = i
                        break
                
                # 避免同一规则在同一行重复提示
                key = f"{rule['id']}_{line_num}"
                if key in seen_rule_line:
                    continue
                    
                risks.append({
                    **rule,
                    "match_text": match.group(),
                    "line_num": line_num
                })
                seen_rule_line.add(key)
    
    return risks

def check_essential_clauses(content: str) -> List[Dict]:
    """检查必备条款"""
    essential_clauses = [
        ("当事人信息", ["甲方", "乙方", "名称", "住所"]),
        ("合同标的", ["标的", "标的物", "产品", "服务"]),
        ("数量条款", ["数量", "共", "总计"]),
        ("价款报酬", ["价款", "价格", "金额", "费用", "元"]),
        ("履行期限", ["期限", "日期", "年", "月", "日", "交付"]),
        ("违约责任", ["违约", "赔偿", "违约金"]),
        ("争议解决", ["争议", "纠纷", "管辖", "法院", "仲裁"])
    ]
    
    missing = []
    for clause_name, keywords in essential_clauses:
        found = any(keyword in content for keyword in keywords)
        if not found:
            missing.append({
                "clause": clause_name,
                "level": "medium",
                "risk": f"缺少{clause_name}，合同完整性不足",
                "suggestion": f"建议补充{clause_name}相关条款"
            })
    
    return missing

def generate_report(contract_name: str, risks: List[Dict], missing_clauses: List[Dict]) -> str:
    """生成审查报告"""
    high_count = sum(1 for r in risks if r['level'] == 'high')
    medium_count = sum(1 for r in risks if r['level'] == 'medium')
    low_count = sum(1 for r in risks if r['level'] == 'low')
    
    report = []
    report.append("=" * 60)
    report.append("📋 ContractAI Pro 审查报告")
    report.append("=" * 60)
    report.append(f"📋 合同名称：{contract_name}")
    report.append(f"📅 审查时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"📊 风险统计：🔴 高风险{high_count}项 | 🟡 中风险{medium_count + len(missing_clauses)}项 | 🟢 低风险{low_count}项")
    report.append("")
    
    # 高风险
    high_risks = [r for r in risks if r['level'] == 'high']
    if high_risks:
        report.append("🔴 【高风险条款】")
        report.append("-" * 60)
        for i, risk in enumerate(high_risks, 1):
            report.append(f"【高风险{i}】{risk['name']}")
            report.append(f"📍 位置：第{risk['line_num']}行")
            report.append(f"📝 原文：{risk['match_text']}")
            report.append(f"⚠️ 风险：{risk['risk']}")
            report.append(f"💡 修改建议：{risk['suggestion']}")
            report.append(f"📜 法律依据：{risk['law_ref']}")
            report.append("")
    
    # 中风险
    medium_risks = [r for r in risks if r['level'] == 'medium']
    if medium_risks:
        report.append("🟡 【中风险条款】")
        report.append("-" * 60)
        for i, risk in enumerate(medium_risks, 1):
            report.append(f"【中风险{i}】{risk['name']}")
            report.append(f"📍 位置：第{risk['line_num']}行")
            report.append(f"📝 原文：{risk['match_text']}")
            report.append(f"⚠️ 风险：{risk['risk']}")
            report.append(f"💡 修改建议：{risk['suggestion']}")
            report.append("")
    
    # 缺失条款
    if missing_clauses:
        report.append("🟡 【缺失必备条款】")
        report.append("-" * 60)
        for item in missing_clauses:
            report.append(f"⚠️ {item['clause']}：{item['risk']}")
            report.append(f"💡 建议：{item['suggestion']}")
            report.append("")
    
    # 总体评价
    report.append("=" * 60)
    report.append("📌 总体评价：")
    
    if high_count > 0:
        report.append(f"   ⚠️ 该合同存在{high_count}项高风险条款，强烈建议修改后签署")
    elif medium_count > 0:
        report.append(f"   ✅ 该合同无高风险，但存在{medium_count}项中风险，建议优化")
    else:
        report.append("   ✅ 该合同风险较低，可以签署")
    
    if risks:
        report.append("")
        report.append("📋 建议修改优先级：")
        for i, risk in enumerate(risks[:3], 1):
            priority = "必须修改" if risk['level'] == 'high' else "建议修改"
            report.append(f"  {i}. {risk['name']} → {priority}")
    
    report.append("")
    report.append("=" * 60)
    report.append("💡 ContractAI Pro - 专业级合同审查专家")
    report.append("📧 如需深度审查或律师咨询，请联系专业法律顾问")
    report.append("=" * 60)
    
    return "\n".join(report)

def main():
    parser = argparse.ArgumentParser(description='ContractAI Pro - 专业合同审查工具')
    parser.add_argument('--file', '-f', required=True, help='合同文件路径')
    parser.add_argument('--export', '-e', help='导出报告文件路径')
    parser.add_argument('--brief', '-b', action='store_true', help='仅显示简要摘要')
    
    args = parser.parse_args()
    
    print(f"🔍 正在审查合同：{args.file}")
    print(f"⏳ 加载风险规则库... (共{len(RISK_RULES)}条规则)")
    
    # 读取合同
    content = read_contract(args.file)
    print(f"📄 合同大小：{len(content)}字符")
    
    # 查找风险
    risks = find_risks(content)
    missing_clauses = check_essential_clauses(content)
    
    print(f"✅ 审查完成！发现 {len(risks)} 个风险点")
    print()
    
    # 生成报告
    contract_name = os.path.basename(args.file)
    report = generate_report(contract_name, risks, missing_clauses)
    
    if args.brief:
        # 简要输出
        high = sum(1 for r in risks if r['level'] == 'high')
        medium = sum(1 for r in risks if r['level'] == 'medium')
        print(f"📊 风险摘要：🔴 高风险{high}项 | 🟡 中风险{medium}项 | 🟢 低风险0项")
    else:
        print(report)
    
    # 导出报告
    if args.export:
        with open(args.export, 'w', encoding='utf-8') as f:
            f.write(report)
        print()
        print(f"📤 报告已导出至：{args.export}")

if __name__ == "__main__":
    main()
