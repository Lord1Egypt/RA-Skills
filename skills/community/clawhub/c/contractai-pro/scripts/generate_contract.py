#!/usr/bin/env python3
"""
ContractAI Pro - 合同生成脚本
功能：基于模板快速生成各类合同
"""

import argparse
import sys
import os
from datetime import datetime

# 合同模板库
CONTRACT_TEMPLATES = {
    "买卖合同": {
        "name": "买卖合同",
        "description": "适用于货物买卖、产品购销等场景",
        "template": """
# 《买卖合同》

合同编号：{contract_no}
签订地点：{sign_place}
签订日期：{sign_date}

## 第一条 合同双方

甲方（卖方）：{party_a}
法定代表人：{party_a_rep}
地址：{party_a_addr}
联系方式：{party_a_tel}

乙方（买方）：{party_b}
法定代表人：{party_b_rep}
地址：{party_b_addr}
联系方式：{party_b_tel}

## 第二条 合同标的

| 序号 | 产品名称 | 规格型号 | 数量 | 单价（元） | 总价（元） | 备注 |
|-----|---------|---------|------|-----------|-----------|------|
| 1   | {product_name} | {product_spec} | {quantity} | {unit_price} | {total_amount} | |
|     |         |         |      | 合计：    | {total_amount} | |

## 第三条 质量标准

1. 产品质量符合国家标准、行业标准及双方约定的技术标准。
2. 卖方对产品质量负责，质保期为{warranty_period}个月。

## 第四条 交货方式

1. 交货时间：{delivery_date}前
2. 交货地点：{delivery_place}
3. 运输方式及费用：{delivery_method}，运费由{transport_cost_party}承担

## 第五条 付款方式

1. 合同总金额：人民币{total_amount}元（大写：{total_amount_cn}）
2. 付款方式：{payment_method}
3. 付款节点：
   - 预付款：{prepayment_percent}%，合同签订后3日内支付
   - 到货款：{delivery_payment_percent}%，货物验收合格后3日内支付
   - 质保金：{warranty_payment_percent}%，质保期满后3日内支付

## 第六条 验收标准

1. 验收时间：货到后{accept_days}日内完成验收
2. 验收标准：按本合同第二条约定的质量标准
3. 异议期：乙方发现质量问题应在{objection_days}日内提出

## 第七条 违约责任

1. 卖方逾期交货的，每日按逾期交货金额的{default_rate}向买方支付违约金。
2. 买方逾期付款的，每日按逾期付款金额的{default_rate}向卖方支付违约金。
3. 产品质量不符合约定的，卖方应负责更换、退货，并赔偿买方因此遭受的损失。
4. 违约金累计不超过合同总金额的20%。

## 第八条 争议解决

因本合同引起的或与本合同有关的任何争议，双方应友好协商解决；协商不成的，按下列第{dispute_resolution}种方式解决：
1. 向原告所在地人民法院提起诉讼
2. 提交{arbitration_committee}仲裁委员会仲裁

## 第九条 其他条款

1. 本合同自双方签字盖章之日起生效。
2. 本合同一式{copy_count}份，双方各执{copy_each}份，具有同等法律效力。
3. 本合同未尽事宜，双方可签订补充协议，补充协议与本合同具有同等法律效力。

（以下无正文，为签署页）

甲方（盖章）：{party_a}
法定代表人或授权代表（签字）：
日期：  年  月  日

乙方（盖章）：{party_b}
法定代表人或授权代表（签字）：
日期：  年  月  日
        """,
        "required_fields": [
            "contract_no", "sign_place", "sign_date",
            "party_a", "party_a_rep", "party_a_addr", "party_a_tel",
            "party_b", "party_b_rep", "party_b_addr", "party_b_tel",
            "product_name", "product_spec", "quantity", "unit_price", "total_amount",
            "warranty_period", "delivery_date", "delivery_place", "delivery_method",
            "transport_cost_party", "total_amount_cn", "payment_method",
            "prepayment_percent", "delivery_payment_percent", "warranty_payment_percent",
            "accept_days", "objection_days", "default_rate", "dispute_resolution",
            "arbitration_committee", "copy_count", "copy_each"
        ]
    },
    
    "劳动合同": {
        "name": "劳动合同",
        "description": "适用于企业与员工签订劳动合同",
        "template": """
# 《劳动合同》

合同编号：{contract_no}

## 第一条 合同双方

甲方（用人单位）：{employer}
法定代表人：{employer_rep}
地址：{employer_addr}
联系方式：{employer_tel}

乙方（劳动者）：{employee}
身份证号：{employee_id}
住址：{employee_addr}
联系方式：{employee_tel}

## 第二条 合同期限

本合同为{contract_type}劳动合同，期限自{start_date}起至{end_date}止。
其中试用期为{probation_period}个月，自{probation_start}起至{probation_end}止。

## 第三条 工作内容和工作地点

1. 工作岗位：{job_position}
2. 工作内容：{job_description}
3. 工作地点：{work_place}

## 第四条 工作时间和休息休假

1. 实行{work_schedule}工作制。
2. 乙方依法享有法定节假日、年休假、婚假、产假等假期。

## 第五条 劳动报酬

1. 月工资标准：人民币{monthly_salary}元（试用期工资：人民币{probation_salary}元）
2. 工资发放日：每月{pay_day}日
3. 工资构成：基本工资+绩效工资+津贴补贴

## 第六条 社会保险和福利待遇

1. 甲方按国家和地方规定为乙方缴纳社会保险。
2. 乙方享有甲方规定的各项福利待遇。

## 第七条 劳动保护和劳动条件

甲方为乙方提供符合国家规定的劳动安全卫生条件和必要的劳动防护用品。

## 第八条 保密和竞业限制

1. 乙方应对甲方的商业秘密保密，保密期限为{confidentiality_period}。
2. {non_compete_clause}

## 第九条 合同的解除和终止

1. 双方协商一致，可以解除本合同。
2. 乙方提前30日（试用期内提前3日）以书面形式通知甲方，可以解除本合同。
3. 符合法定解除情形的，甲方或乙方可以解除本合同。

## 第十条 违约责任

任何一方违反本合同约定，给对方造成损失的，应承担赔偿责任。

## 第十一条 争议解决

因履行本合同发生的劳动争议，双方应协商解决；协商不成的，可以向劳动争议仲裁委员会申请仲裁。

## 第十二条 其他

1. 本合同一式两份，甲乙双方各执一份，具有同等法律效力。
2. 本合同自双方签字盖章之日起生效。

甲方（盖章）：{employer}
法定代表人或授权代表（签字）：
日期：  年  月  日

乙方（签字）：{employee}
日期：  年  月  日
        """,
        "required_fields": [
            "contract_no", "employer", "employer_rep", "employer_addr", "employer_tel",
            "employee", "employee_id", "employee_addr", "employee_tel",
            "contract_type", "start_date", "end_date",
            "probation_period", "probation_start", "probation_end",
            "job_position", "job_description", "work_place", "work_schedule",
            "monthly_salary", "probation_salary", "pay_day",
            "confidentiality_period", "non_compete_clause"
        ]
    },
    
    "房屋租赁合同": {
        "name": "房屋租赁合同",
        "description": "适用于房屋出租、承租场景",
        "template": """
# 《房屋租赁合同》

合同编号：{contract_no}
签订日期：{sign_date}

## 第一条 合同双方

甲方（出租方）：{lessor}
身份证号：{lessor_id}
联系方式：{lessor_tel}

乙方（承租方）：{lessee}
身份证号：{lessee_id}
联系方式：{lessee_tel}

## 第二条 房屋基本情况

1. 房屋坐落：{house_address}
2. 房屋面积：建筑面积{house_area}平方米
3. 房屋用途：{house_purpose}
4. 房屋权属：产权证号{house_property_no}

## 第三条 租赁期限

1. 租赁期限自{lease_start}起至{lease_end}止，共计{lease_months}个月。
2. 租赁期满，乙方如需续租，应提前{renewal_days}日书面通知甲方。

## 第四条 租金及支付方式

1. 月租金标准：人民币{monthly_rent}元（大写：{monthly_rent_cn}）
2. 租金支付方式：按{rent_payment_cycle}支付
3. 支付时间：每期到期前{rent_payment_days}日支付下期租金
4. 押金：人民币{deposit}元，租赁期满且乙方无违约的，甲方无息退还

## 第五条 相关费用

租赁期间，下列费用由乙方承担：
1. 水费、电费、燃气费
2. 物业管理费
3. 有线电视费、网络费
4. 其他：{other_expenses}

## 第六条 房屋使用和维护

1. 乙方应合理使用房屋及其附属设施，不得擅自改变房屋结构。
2. 房屋及设施的正常维修由甲方负责。
3. 因乙方使用不当造成房屋或设施损坏的，乙方应负责修复或赔偿。

## 第七条 合同的解除

1. 经双方协商一致，可以解除本合同。
2. 乙方逾期支付租金超过{rent_overdue_days}日的，甲方有权解除合同。
3. 乙方擅自转租、改变房屋用途的，甲方有权解除合同。

## 第八条 违约责任

1. 乙方逾期支付租金的，每日按逾期金额的{default_rate}支付违约金。
2. 甲方提前收回房屋的，应退还剩余租金并支付{default_months}个月租金作为违约金。
3. 乙方提前退租的，应支付{default_months}个月租金作为违约金。

## 第九条 争议解决

因本合同引起的争议，双方应协商解决；协商不成的，向房屋所在地人民法院起诉。

## 第十条 其他

1. 本合同一式两份，双方各执一份，具有同等法律效力。
2. 本合同自双方签字之日起生效。

甲方（签字）：{lessor}
日期：  年  月  日

乙方（签字）：{lessee}
日期：  年  月  日
        """,
        "required_fields": [
            "contract_no", "sign_date",
            "lessor", "lessor_id", "lessor_tel",
            "lessee", "lessee_id", "lessee_tel",
            "house_address", "house_area", "house_purpose", "house_property_no",
            "lease_start", "lease_end", "lease_months", "renewal_days",
            "monthly_rent", "monthly_rent_cn", "rent_payment_cycle",
            "rent_payment_days", "deposit", "other_expenses",
            "rent_overdue_days", "default_rate", "default_months"
        ]
    },
    
    "保密协议": {
        "name": "保密协议",
        "description": "适用于企业间或企业与员工间的保密约定",
        "template": """
# 《保密协议》

协议编号：{agreement_no}
签订日期：{sign_date}

## 第一条 协议双方

甲方：{party_a}
地址：{party_a_addr}
联系方式：{party_a_tel}

乙方：{party_b}
地址：{party_b_addr}
联系方式：{party_b_tel}

## 第二条 保密信息

1. 保密信息包括但不限于：
   - 技术信息：{tech_info}
   - 经营信息：{business_info}
   - 其他信息：{other_info}

2. 保密信息的载体包括纸质文件、电子文档、口头披露等形式。

## 第三条 保密义务

1. 乙方应对保密信息严格保密，不得向任何第三方披露。
2. 乙方应采取合理的保密措施，防止保密信息泄露。
3. 乙方仅可向确有必要知晓的员工披露保密信息，并要求其承担保密义务。

## 第四条 保密期限

1. 保密期限自本协议签订之日起至{confidentiality_end_date}止。
2. 保密期限届满后，对于仍处于保密状态的商业秘密，乙方仍应承担保密义务。

## 第五条 禁止行为

1. 不得擅自复制、摘抄、传播保密信息
2. 不得利用保密信息为自己或第三方谋取利益
3. 不得在公开场合谈论保密信息
4. 离职后不得使用或披露保密信息

## 第六条 保密信息的返还

本协议终止或甲方要求时，乙方应立即返还全部保密信息载体，并销毁复制件。

## 第七条 违约责任

1. 乙方违反本协议的，应向甲方支付违约金人民币{penalty_amount}元。
2. 违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。
3. 甲方有权要求乙方承担因调查、维权而产生的合理费用。

## 第八条 争议解决

因本协议引起的争议，双方应协商解决；协商不成的，向甲方所在地人民法院起诉。

## 第九条 其他

1. 本协议一式两份，双方各执一份，具有同等法律效力。
2. 本协议自双方签字盖章之日起生效。

甲方（盖章）：{party_a}
法定代表人或授权代表（签字）：
日期：  年  月  日

乙方（盖章/签字）：{party_b}
法定代表人或授权代表（签字）：
日期：  年  月  日
        """,
        "required_fields": [
            "agreement_no", "sign_date",
            "party_a", "party_a_addr", "party_a_tel",
            "party_b", "party_b_addr", "party_b_tel",
            "tech_info", "business_info", "other_info",
            "confidentiality_end_date", "penalty_amount"
        ]
    }
}

def number_to_chinese(num: int) -> str:
    """将数字转换为中文大写金额"""
    digits = ['零', '壹', '贰', '叁', '肆', '伍', '陆', '柒', '捌', '玖']
    units = ['', '拾', '佰', '仟', '万', '拾', '佰', '仟', '亿']
    
    if num == 0:
        return '零元整'
    
    num_str = str(num)
    result = ''
    
    for i, digit in enumerate(reversed(num_str)):
        if digit != '0':
            result = digits[int(digit)] + units[i] + result
        elif i % 4 == 0 and result and not result.startswith('万'):
            result = units[i] + result
    
    return result + '元整'

def list_templates():
    """列出所有可用模板"""
    print("=" * 60)
    print("📋 可用合同模板列表")
    print("=" * 60)
    
    for i, (key, template) in enumerate(CONTRACT_TEMPLATES.items(), 1):
        print(f"{i}. {template['name']}")
        print(f"   说明：{template['description']}")
        print(f"   必填字段数：{len(template['required_fields'])}个")
        print()
    
    print("=" * 60)
    print(f"💡 使用示例：")
    print(f"   python generate_contract.py --template 买卖合同 --output 我的合同.md")
    print(f"   python generate_contract.py --list  # 查看模板列表")
    print("=" * 60)

def generate_contract(template_name: str, output_file: str, **kwargs):
    """生成合同"""
    if template_name not in CONTRACT_TEMPLATES:
        print(f"❌ 未找到模板：{template_name}")
        print(f"可用模板：{', '.join(CONTRACT_TEMPLATES.keys())}")
        sys.exit(1)
    
    template = CONTRACT_TEMPLATES[template_name]
    
    # 默认值填充
    defaults = {
        "contract_no": f"HT{datetime.now().strftime('%Y%m%d%H%M')}",
        "sign_date": datetime.now().strftime('%Y年%m月%d日'),
        "sign_place": "北京市",
        "default_rate": "0.05%",
        "dispute_resolution": "1",
        "arbitration_committee": "北京",
        "copy_count": "4",
        "copy_each": "2",
        "accept_days": "7",
        "objection_days": "15",
        "warranty_period": "12",
        "transport_cost_party": "卖方",
        "prepayment_percent": "30",
        "delivery_payment_percent": "60",
        "warranty_payment_percent": "10",
        "contract_type": "固定期限",
        "probation_period": "2",
        "work_schedule": "标准工时",
        "confidentiality_period": "合同终止后2年",
        "non_compete_clause": "乙方离职后2年内不得到与甲方有竞争关系的单位任职",
        "lease_months": "12",
        "renewal_days": "30",
        "rent_payment_cycle": "月",
        "rent_payment_days": "5",
        "rent_overdue_days": "15",
        "default_months": "1",
        "penalty_amount": "100000",
        "confidentiality_end_date": "保密信息公开之日"
    }
    
    # 合并参数
    params = {**defaults, **kwargs}
    
    # 金额大写转换
    if 'total_amount' in params and params['total_amount']:
        try:
            params['total_amount_cn'] = number_to_chinese(int(float(params['total_amount'])))
        except:
            params['total_amount_cn'] = params.get('total_amount', '') + "元"
    
    if 'monthly_rent' in params and params['monthly_rent']:
        try:
            params['monthly_rent_cn'] = number_to_chinese(int(float(params['monthly_rent'])))
        except:
            params['monthly_rent_cn'] = params.get('monthly_rent', '') + "元"
    
    # 生成合同
    try:
        contract_content = template['template'].format(**params)
    except KeyError as e:
        print(f"⚠️ 缺少必填参数：{e}")
        print(f"请使用 --{e} 参数提供该值")
        sys.exit(1)
    
    # 保存文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(contract_content)
    
    print(f"✅ 合同生成成功！")
    print(f"📄 模板类型：{template_name}")
    print(f"💾 保存路径：{output_file}")
    print(f"📝 文件大小：{len(contract_content)}字符")
    print()
    print("💡 提示：请根据实际情况修改合同中的具体内容，建议咨询专业律师后签署")

def main():
    parser = argparse.ArgumentParser(description='ContractAI Pro - 合同生成工具')
    parser.add_argument('--list', '-l', action='store_true', help='列出所有可用模板')
    parser.add_argument('--template', '-t', help='选择模板名称')
    parser.add_argument('--output', '-o', default='contract.md', help='输出文件路径')
    
    # 常用参数
    parser.add_argument('--partyA', help='甲方名称')
    parser.add_argument('--partyB', help='乙方名称')
    parser.add_argument('--amount', help='合同金额')
    
    args, unknown = parser.parse_known_args()
    
    # 处理未知参数（允许用户自定义参数）
    custom_params = {}
    for i in range(0, len(unknown), 2):
        if unknown[i].startswith('--'):
            key = unknown[i][2:].replace('-', '_')
            if i + 1 < len(unknown):
                custom_params[key] = unknown[i + 1]
    
    if args.list:
        list_templates()
        return
    
    if not args.template:
        print("❌ 请指定模板名称，使用 --list 查看可用模板")
        sys.exit(1)
    
    # 合并参数
    params = {}
    if args.partyA:
        params['party_a'] = args.partyA
        params['lessor'] = args.partyA
        params['employer'] = args.partyA
    if args.partyB:
        params['party_b'] = args.partyB
        params['lessee'] = args.partyB
        params['employee'] = args.partyB
    if args.amount:
        params['total_amount'] = args.amount
        params['monthly_rent'] = args.amount
    
    params.update(custom_params)
    
    generate_contract(args.template, args.output, **params)

if __name__ == "__main__":
    main()
