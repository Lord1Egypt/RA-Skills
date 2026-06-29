---
name: finance-audit-tracker
description: 上市公司审计追踪与风险检测技能包，自动化分析往来账龄、标记异常交易、检测重复付款、监控大额异常预警。适用于财务审计、内控合规、风险预警、税务风险检测等场景。当用户提到审计追踪、账龄分析、异常交易检测、重复付款、大额预警、风险检测、内控审计、应收账款、应付账款、银行对账、费用审计、税务风险等关键词时触发。
metadata:
  openclaw:
    author: "@AOLIKEJI"
    version: 1.0.0
    category: finance
    tags:
      - 审计
      - 财务
      - 风控
      - 合规
      - 账龄分析
      - 异常检测
      - 税务
      - 报表
    emoji: "🔍"
    homepage: "https://github.com/AOLIKEJI/finance-audit-tracker"
    triggers:
      - 审计追踪
      - 账龄分析
      - 异常交易
      - audit
      - 重复付款
      - 大额预警
      - 风险检测
      - 内控审计
      - 应收账款
      - 应付账款
      - 银行对账
      - 费用审计
      - 税务风险
      - 坏账准备
      - 供应商分析
      - 关联交易
      - 发票核验
---

# 财务审计追踪技能包

## 概述

本技能包为上市公司提供全面的财务审计追踪与风险检测能力，通过自动化分析帮助审计人员高效识别异常交易、账龄问题、重复付款等风险点，提升审计效率与准确性。

## 核心检测流程

### 模块一：应收账款账龄分析

#### 1.1 账龄区间划分标准

| 账龄区间 | 天数范围 | 风险等级 | 备注 |
|---------|---------|---------|------|
| 即时/当前 | 0-30天 | 低 | 正常在信用期内 |
| 短期 | 31-60天 | 中低 | 轻度关注 |
| 中期 | 61-90天 | 中 | 需要催收跟进 |
| 长期 | 91-180天 | 高 | 存在逾期风险 |
| 超长期 | 181-365天 | 很高 | 坏账可能性大 |
| 长期挂账 | 1年以上 | 极高 | 需专项审计 |

#### 1.2 坏账准备计提比例（企业会计政策参考）

```
坏账计提比例 = 
  1年内:     0-5%
  1-2年:     10-30%
  2-3年:     30-50%
  3年以上:   50-100%
```

**账龄分析表生成公式**：
```
期末坏账准备 = Σ(各账龄区间余额 × 对应计提比例)
```

#### 1.3 逾期客户预警清单生成

**触发条件**：
- 单笔应收款逾期超过30天
- 同一客户逾期总额超过信用额度的50%
- 逾期金额占总应收账款10%以上

**输出格式**：
```
逾期预警清单：
| 客户名称 | 逾期金额 | 账龄 | 信用额度 | 占用比例 | 风险等级 |
|---------|---------|------|---------|---------|---------|
| XXX公司 | ¥500,000 | 45天 | ¥800,000 | 62.5% | 🔴高 |
```

---

### 模块二：应付账款账龄分析

#### 2.1 供应商账龄统计

**统计维度**：
- 按供应商维度汇总应付余额
- 按账龄区间分组统计
- 按付款条件对比实际付款周期

#### 2.2 逾期应付款预警

**预警规则**：
```
逾期天数 = 实际付款日期 - 应付到期日
逾期金额 = 逾期天数 > 0 的应付账款合计
```

#### 2.3 付款优先级排序算法

```python
付款优先级 = 
  (紧急程度权重 × 逾期天数) + 
  (金额权重 × log(应付金额)) + 
  (关系权重 × 供应商评级)
```

**权重参考**：
- 紧急程度权重：0.4
- 金额权重：0.3
- 关系权重：0.3

---

### 模块三：异常交易检测

#### 3.1 大额交易预警

**阈值设定**：
```
单笔预警阈值 = max(历史平均交易额 × 3, 固定阈值)
固定阈值默认值：¥500,000
```

**判断逻辑**：
```python
def check_large_transaction(amount, history_avg):
    threshold = max(history_avg * 3, 500000)
    if amount > threshold:
        return {"flag": True, "level": "warning", "threshold": threshold}
    return {"flag": False}
```

#### 3.2 非工作时间交易检测

**检测范围**：
- 工作日 22:00 - 次日 06:00
- 周末及节假日全天

**异常指数计算**：
```
非工作时间交易频率 = 非工作时间交易数 / 总交易数
异常指数 = 非工作时间交易频率 × 金额占比
```

#### 3.3 频繁小额交易（拆单检测）

**拆单特征识别**：
```python
def detect_split_transactions(transactions, amount_threshold=10000):
    """
    检测是否存在将大额交易拆分为多笔小额交易
    """
    # 1. 按交易对手+时间段分组
    grouped = group_by_counterparty_and_period(transactions)
    
    # 2. 识别金额接近阈值的连续交易
    suspicious_patterns = []
    for key, txns in grouped.items():
        sorted_txns = sort_by_time(txns)
        # 3. 检测是否存在金额之和超过阈值的连续小额交易
        for i in range(len(sorted_txns)):
            window_sum = 0
            for j in range(i, min(i+5, len(sorted_txns))):  # 5分钟内
                window_sum += sorted_txns[j].amount
                if window_sum > amount_threshold * 0.9:  # 达到阈值90%
                    suspicious_patterns.append({
                        "transactions": sorted_txns[i:j+1],
                        "total_amount": window_sum,
                        "count": j - i + 1
                    })
    return suspicious_patterns
```

#### 3.4 关联交易异常检测

**关联交易识别维度**：
- 关联方识别：母公司、子公司、合营企业、联营企业
- 交易频率异常：与关联方交易频率显著高于其他供应商
- 价格异常：关联方交易价格偏离市场价20%以上
- 条款异常：给予关联方特殊付款条件

**风险评分公式**：
```
关联交易风险分 = 
  基础分(20) + 
  频率异常加分(0-30) + 
  价格偏离加分(0-30) + 
  条款异常加分(0-20)
```

#### 3.5 整数金额交易检测

**整数判定规则**：
```python
def is_round_amount(amount):
    """检测是否为整数金额（可能存在虚假交易）"""
    # 排除已知的整数交易类型（如工资、水电费）
    if is_known_regular_expense(amount):
        return False
    # 判断是否为整数或接近整数
    return abs(amount - round(amount)) < 0.01

def calculate_round_amount_risk(txns):
    """计算整数金额交易风险指数"""
    round_count = sum(1 for t in txns if is_round_amount(t.amount))
    total_count = len(txns)
    round_ratio = round_count / total_count if total_count > 0 else 0
    
    # 整数金额占比超过行业均值可能有异常
    industry_avg = 0.15  # 行业平均水平
    risk_score = min((round_ratio - industry_avg) * 100, 50)
    return risk_score
```

#### 3.6 月末突击入账检测

**检测逻辑**：
```python
def detect_month_end_spike(transactions, month):
    """检测月末突击入账（粉饰报表嫌疑）"""
    month_txns = filter_by_month(transactions, month)
    
    # 按日期分组统计
    daily_amounts = group_by_day(month_txns)
    
    # 计算最后5天占比
    last_5_days_amount = sum(daily_amounts[-5:])
    month_total = sum(daily_amounts)
    
    spike_ratio = last_5_days_amount / month_total if month_total > 0 else 0
    
    return {
        "last_5_days_ratio": spike_ratio,
        "flag": spike_ratio > 0.4,  # 超过40%触发预警
        "risk_level": "high" if spike_ratio > 0.5 else "medium"
    }
```

---

### 模块四：重复付款检测

#### 4.1 相同金额+相同供应商+相近日期检测

**检测规则**：
```python
def detect_duplicate_payment(transactions, tolerance_days=7, tolerance_amount=0.01):
    """
    检测重复付款
    - 相同供应商
    - 金额差异小于 tolerance_amount
    - 日期差小于 tolerance_days
    """
    duplicates = []
    for i, t1 in enumerate(transactions):
        for t2 in transactions[i+1:]:
            same_supplier = t1.supplier_id == t2.supplier_id
            similar_amount = abs(t1.amount - t2.amount) / t1.amount < tolerance_amount
            close_date = abs((t2.date - t1.date).days) <= tolerance_days
            
            if same_supplier and similar_amount and close_date:
                duplicates.append({
                    "transaction_1": t1,
                    "transaction_2": t2,
                    "match_type": "amount_supplier_date"
                })
    return duplicates
```

#### 4.2 相同发票号重复报销检测

```python
def detect_duplicate_invoice(invoices):
    """检测相同发票号重复报销"""
    invoice_groups = group_by_invoice_number(invoices)
    duplicates = {k: v for k, v in invoice_groups.items() if len(v) > 1}
    return duplicates
```

#### 4.3 重复凭证号检查

```python
def detect_duplicate_voucher(vouchers):
    """检测凭证号重复"""
    voucher_groups = group_by_voucher_number(vouchers)
    duplicates = {k: v for k, v in voucher_groups.items() if len(v) > 1}
    return duplicates
```

#### 4.4 已付款状态变更检测

**检测场景**：
- 同一笔付款记录出现多次"付款完成"状态
- 已付款记录状态被回退为"未付款"
- 付款金额被修改

---

### 模块五：银行对账异常

#### 5.1 银行流水与账面余额差异分析

**对账公式**：
```
银行对账差异 = 银行余额 - 账面余额

调整后余额 = 银行余额 ± 未达账项
应等于 = 账面余额
```

#### 5.2 未达账项分析

**未达账项类型**：
| 类型 | 方向 | 说明 |
|------|------|------|
| 银行已收企业未收 | 企业少计 | 加回 |
| 银行已付企业未付 | 企业多计 | 减除 |
| 企业已收银行未收 | 银行少计 | 减除 |
| 企业已付银行未付 | 银行多计 | 加回 |

#### 5.3 长期挂账项目标记

**挂账期限阈值**：
```
短期挂账: 30-90天
中期挂账: 90-180天
长期挂账: 180天以上
```

#### 5.4 资金流向异常检测

```python
def detect_fund_flow_anomaly(transactions, base_ratio=0.3):
    """
    检测资金流向异常
    - 单个账户流出/流入占比异常
    - 资金快进快出
    - 资金闭环流动
    """
    # 计算各账户资金流占比
    account_flows = calculate_account_flow_ratio(transactions)
    
    anomalies = []
    for account, flow in account_flows.items():
        if abs(flow.out_ratio - 0.5) > base_ratio:  # 流出或流入占比过高
            anomalies.append({
                "account": account,
                "out_ratio": flow.out_ratio,
                "pattern": "单向流动异常" if flow.out_ratio > 0.9 or flow.out_ratio < 0.1 else "比例失衡"
            })
    
    return anomalies
```

---

### 模块六：费用审计

#### 6.1 费用率异常波动检测

**费用率计算**：
```
费用率 = 费用发生额 / 营业收入 × 100%

同比变化率 = (本期费用率 - 上期费用率) / 上期费用率 × 100%
```

**预警阈值**：
- 同比波动超过20%：⚠️关注
- 同比波动超过50%：🔴重点审计

#### 6.2 差旅费合理性检查

**检查维度**：
```python
def audit_travel_expense(claims, company_policy):
    """
    差旅费合理性审计
    - 机票价格是否超标
    - 住宿费是否超标准
    - 出差天数与行程匹配性
    """
    violations = []
    for claim in claims:
        # 机票舱位检查
        if claim.ticket_class != "经济舱" and not claim.is_approved_premium:
            violations.append(f"机票舱位超标: {claim.employee}")
        
        # 住宿费检查
        if claim.hotel_rate > company_policy.max_hotel_rate:
            violations.append(f"住宿超标: {claim.employee}, 实际¥{claim.hotel_rate}, 标准¥{company_policy.max_hotel_rate}")
        
        # 行程合理性检查
        if claim.trip_days < 0.5:  # 当天往返
            if claim.total_expense > company_policy.same_day_limit:
                violations.append(f"当天往返费用超标: {claim.employee}")
    
    return violations
```

#### 6.3 业务招待费限额检测

**税法规定**：
```
扣除限额 = min(营业收入 × 0.5%, 发生额 × 60%)
超出部分需调增应纳税所得额
```

**检测公式**：
```python
def check_entertainment_limit(revenue, entertainment_expense):
    limit_1 = revenue * 0.005  # 营业收入0.5%
    limit_2 = entertainment_expense * 0.6  # 发生额60%
    deductible_limit = min(limit_1, limit_2)
    
    over_limit = entertainment_expense - deductible_limit
    return {
        "deductible_amount": deductible_limit,
        "over_limit_amount": max(0, over_limit),
        "tax_adjustment": max(0, over_limit) * 0.25,  # 假设25%税率
        "flag": over_limit > 0
    }
```

#### 6.4 工资异常变动检测

**检测维度**：
```python
def detect_salary_anomaly(salary_records, threshold_ratio=0.2):
    """
    工资异常变动检测
    - 月度波动检测
    - 人员变动检测
    - 奖金异常发放
    """
    anomalies = []
    
    for employee, records in group_by_employee(salary_records).items():
        sorted_records = sort_by_month(records)
        
        for i in range(1, len(sorted_records)):
            change_ratio = (sorted_records[i].total - sorted_records[i-1].total) / sorted_records[i-1].total
            
            if abs(change_ratio) > threshold_ratio:
                anomalies.append({
                    "employee": employee,
                    "month": sorted_records[i].month,
                    "change_ratio": change_ratio,
                    "possible_reason": "大额奖金" if change_ratio > 0 else "扣款异常"
                })
    
    return anomalies
```

---

### 模块七：税务风险检测

#### 7.1 进销项比率异常

```python
def check_input_output_ratio(purchases, sales, industry_avg_ratio=1.2):
    """
    进销项比率分析
    正常企业进项税额应略大于销项税额
    比率过高可能存在虚开或滞留发票
    比率过低可能存在隐瞒收入
    """
    input_tax = sum(p.amount for p in purchases)
    output_tax = sum(s.tax for s in sales)
    
    ratio = input_tax / output_tax if output_tax > 0 else float('inf')
    
    return {
        "ratio": ratio,
        "flag": ratio < 0.8 or ratio > 2.0,
        "risk": "比率过低-可能隐瞒收入" if ratio < 0.8 else 
                "比率过高-可能虚抵进项" if ratio > 2.0 else "正常"
    }
```

#### 7.2 税负率偏离检测

**行业税负率参考**：
```python
industry_tax_burden = {
    "制造业": (3, 5),      # 增值税税负率范围
    "批发零售": (1.5, 3),
    "建筑业": (2.5, 4.5),
    "服务业": (3, 6),
    "房地产": (5, 10)
}

def check_tax_burden_rate(industry, tax_amount, revenue):
    burden_rate = tax_amount / revenue * 100
    min_rate, max_rate = industry_tax_burden.get(industry, (2, 8))
    
    return {
        "burden_rate": burden_rate,
        "industry_range": (min_rate, max_rate),
        "flag": burden_rate < min_rate or burden_rate > max_rate,
        "risk_level": "偏低-需关注" if burden_rate < min_rate else 
                      "偏高-正常经营" if burden_rate < max_rate else "异常"
    }
```

#### 7.3 发票金额与合同金额不匹配

```python
def check_invoice_contract_mismatch(invoices, contracts):
    """
    检测发票金额与合同金额差异
    允许合理差异范围: ±5%
    """
    mismatches = []
    for invoice in invoices:
        contract = find_contract(contracts, invoice.contract_id)
        if contract:
            diff_ratio = abs(invoice.amount - contract.amount) / contract.amount
            if diff_ratio > 0.05:
                mismatches.append({
                    "invoice_no": invoice.no,
                    "contract_no": contract.no,
                    "invoice_amount": invoice.amount,
                    "contract_amount": contract.amount,
                    "diff_ratio": diff_ratio
                })
    return mismatches
```

#### 7.4 长期零申报/负申报预警

**检测规则**：
```python
def detect_zero_negative_filing(tax_records, threshold_months=6):
    """
    检测长期零申报或负申报
    连续超过 threshold_months 触发预警
    """
    consecutive_count = 0
    warning_periods = []
    current_sequence = []
    
    for record in sorted(tax_records, key=lambda x: x.month):
        if record.tax_amount <= 0:
            consecutive_count += 1
            current_sequence.append(record.month)
            if consecutive_count >= threshold_months:
                warning_periods.append(current_sequence.copy())
        else:
            consecutive_count = 0
            current_sequence = []
    
    return warning_periods
```

---

### 模块八：审计报告辅助

#### 8.1 审计发现清单自动生成

**发现分类标准**：

| 风险等级 | 判定条件 | 响应要求 |
|---------|---------|---------|
| 🔴高风险 | 可能导致重大财务损失或违规 | 24小时内上报 |
| 🟡中风险 | 可能造成财务不实 | 5个工作日内处理 |
| 🟢低风险 | 内控缺陷但不影响报表公允 | 30日内整改 |

**生成模板**：
```
审计发现清单
报告期间: XXXX年XX月
生成时间: XXXX年XX月XX日

一、🔴高风险发现
序号 | 问题描述 | 影响金额 | 发现依据 | 建议措施
---- | -------- | ------- | ------- | -------

二、🟡中风险发现
...

三、🟢低风险发现
...

四、风险汇总统计
| 风险等级 | 数量 | 涉及金额 |
|---------|------|---------|
| 🔴高   | X   | ¥XXX    |
| 🟡中   | X   | ¥XXX    |
| 🟢低   | X   | ¥XXX    |
```

#### 8.2 整改建议生成规则

```python
def generate_remediation_suggestions(finding):
    """根据审计发现自动生成整改建议"""
    suggestion_templates = {
        "大额异常交易": "建议立即冻结相关账户，追查资金去向，完善大额交易审批流程",
        "重复付款": "建议启动付款追回程序，完善付款复核机制，建立付款冲突检测系统",
        "账龄逾期": "建议启动法律催收程序，重新评估客户信用等级，计提相应坏账准备",
        "税务风险": "建议聘请专业税务顾问进行自查，准备相关证明材料，按期完成更正申报",
        "费用超标": "建议加强费用预算管理，完善费用报销审批流程，开展费用合规培训"
    }
    
    category = classify_finding(finding)
    base_suggestion = suggestion_templates.get(category, "建议进行进一步调查核实")
    
    return {
        "finding_id": finding.id,
        "category": category,
        "immediate_action": f"24小时内: {get_immediate_action(category)}",
        "short_term": f"30日内: {get_short_term_action(category)}",
        "long_term": f"制度层面: {get_systemic_action(category)}"
    }
```

#### 8.3 审计底稿模板

```markdown
# 审计底稿模板

## 基本信息
- 项目名称: 
- 审计期间: 
- 审计人员: 
- 复核人员: 
- 审计日期: 

## 审计范围
[描述本次审计覆盖的科目、期间、业务范围]

## 审计程序
### 1. 风险评估程序
- 了解被审计单位及其环境
- 识别和评估重大错报风险

### 2. 实质性程序
- [具体测试步骤]

## 审计证据
| 证据编号 | 证据类型 | 证据来源 | 主要内容 | 获取日期 |
|---------|---------|---------|---------|---------|
| E-001 | 文件 | 财务系统 | XX科目明细 | XXXX-XX-XX |

## 审计结论
[基于审计证据得出的结论]

## 重大事项说明
[需要特别说明的事项]

## 附件清单
1. 
2. 
```

---

## 数据输入格式

### 标准输入格式（CSV/Excel）

```csv
交易日期,凭证号,供应商/客户,摘要,借方金额,贷方金额,余额,交易类型
2024-01-15,V001,供应商A,采购商品,50000,0,50000,采购
2024-01-16,V002,客户B,销售商品,0,80000,80000,销售
```

### 标准输出格式

```json
{
  "audit_date": "2024-01-20",
  "findings": [
    {
      "id": "F001",
      "category": "重复付款",
      "risk_level": "high",
      "description": "检测到向供应商A重复支付",
      "evidence": ["交易记录1", "交易记录2"],
      "amount": 50000,
      "suggestion": "启动付款追回程序"
    }
  ],
  "statistics": {
    "total_transactions": 1000,
    "anomalies_detected": 15,
    "risk_distribution": {"high": 3, "medium": 7, "low": 5}
  }
}
```

---

## 使用示例

### 示例1：应收账款账龄分析

**输入**：
```
客户 | 应收账款余额 | 账龄
---------------------------
A公司 | ¥800,000 | 45天
B公司 | ¥1,200,000 | 120天
C公司 | ¥300,000 | 200天
D公司 | ¥500,000 | 15天
```

**输出**：
```
📊 应收账款账龄分析报告

【账龄分布】
| 区间 | 金额 | 占比 | 客户数 |
|------|------|------|-------|
| 0-30天 | ¥500,000 | 18.5% | 1 |
| 31-60天 | ¥800,000 | 29.6% | 1 |
| 91-180天 | ¥1,200,000 | 44.4% | 1 |
| 180天以上 | ¥300,000 | 11.1% | 1 |

【坏账准备估算】
按一般计提比例：
- 31-60天 (5%): ¥40,000
- 91-180天 (30%): ¥360,000
- 180天以上 (50%): ¥150,000
合计坏账准备: ¥550,000

⚠️ 预警客户:
🔴 B公司 - 账龄120天，逾期严重，建议启动催收或法律程序
🔴 C公司 - 账龄200天，建议全额计提坏账
```

### 示例2：重复付款检测

**输入**：2笔向同一供应商的付款记录，金额相近，日期相差3天

**输出**：
```
🚨 重复付款警报

【检测结果】
- 凭证号 V001 和 V002 疑似重复付款
- 供应商: XX供应商
- 金额: ¥50,000 vs ¥49,995 (差异0.01%)
- 日期: 2024-01-10 vs 2024-01-13 (相差3天)

【建议措施】
1. 立即冻结第二笔付款
2. 联系供应商确认实际收款情况
3. 检查付款审批流程漏洞
4. 追回多付款项

【风险评级】🔴 高风险
```

---

## 注意事项

1. **数据保密**：审计数据涉及商业机密，处理过程需确保数据安全
2. **阈值调整**：各检测阈值可根据企业实际情况调整
3. **人工复核**：所有自动检测结果需经审计人员复核确认
4. **合规要求**：税务相关检测需符合最新税法规定
5. **持续更新**：检测规则库需随业务变化和监管要求更新
