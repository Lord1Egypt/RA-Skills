# SKILL.md

**License:** MIT  
**Copyright:** 2026 perrykono-debug

---

---
name: operations-monitoring
description: 运营监测技能。基于《园区运营项目客户服务标准指引》第五章"运营监测"，实现数据收集、分析、任务分发自动化。自动生成《季度运营监测报告》，向责任部门分发任务单，跟踪处理进度。
---

# 运营监测技能 (Operations Monitoring Skill)

## 功能概述

本技能用于自动化运营监测流程，基于《园区运营项目客户服务标准指引》（{TODO: 填写文件编号}）第五章，实现：
1. **数据收集**：整合多源数据（客户档案、费用记录、服务记录、报事报修、能耗数据）
2. **数据分析**：客户健康度评估、园区出租率趋势、客户满意度趋势、重大风险预警
3. **任务分发**：自动生成《季度运营监测报告》，向责任部门分发任务单，跟踪处理进度

---

## 数据来源配置

**主数据文件**: `/Users/mac/示例产业园AC+服务.xlsx`

**工作表映射**:
| 功能模块 | 工作表名 | 来源系统 | 用途 |
|---------|---------|----------|------|
| **客户档案** | 👨客户管理👨 | 集客荟系统 | 客户基本信息、合同信息 |
| **费用收缴** | 👨💼费用收缴👨💼 | 财务部 | 费用记录、逾期统计 |
| **能耗收缴** | 👨💼能耗收缴👨💼 | 集能荟系统 | 能耗数据、欠费统计 |
| **C+服务记录** | C+服务记录 | 物业服务中心 | 走访记录、服务记录 |
| **报事报修** | 报事报修 | 集享荟系统 | 报修记录、处理进度 |

**系统接口（未来扩展）**:
- 集客荟系统 API：客户档案、合同审批、跟进记录
- 集享荟平台 API：报事报修数据、企业认证数据
- 集能荟系统 API：能耗监控数据、缴费记录
- 停车场管理系统 API：车辆出入数据
- 门禁系统 API：客户活跃度数据

---

## 核心逻辑

### 1. 数据收集模块

```python
def collect_operations_data(quarter, year):
    """
    收集指定季度和年份的运营数据
    
    Args:
        quarter: 季度（1-4）
        year: 年份（如2026）
    
    Returns:
        dict: 收集到的运营数据
    """
    wb = openpyxl.load_workbook('/Users/mac/示例产业园AC+服务.xlsx')
    
    # 计算季度时间范围
    start_month = (quarter - 1) * 3 + 1
    end_month = quarter * 3
    start_date = datetime(year, start_month, 1)
    end_date = datetime(year, end_month, 28)  # 简单处理，实际应计算最后一天
    
    data = {
        '季度': f'{year}年第{quarter}季度',
        '时间范围': f'{start_date.strftime("%Y-%m-%d")} 至 {end_date.strftime("%Y-%m-%d")}',
        '客户档案': [],
        '费用记录': [],
        '服务记录': [],
        '报修记录': [],
        '能耗数据': []
    }
    
    # 1. 客户档案数据
    ws_customer = wb['👨客户管理👨']
    for row in ws_customer.iter_rows(min_row=2, values_only=True):
        if row[12] == '签约':  # 状态 = 签约
            data['客户档案'].append({
                '单元号': row[5],
                '租户名': row[6],
                '等级': row[7] if len(row) > 7 else 'B',
                '租赁面积': row[8] if len(row) > 8 else 0,
                '截至日期': row[11],
                '首年合同单价': row[9] if len(row) > 9 else 0
            })
    
    # 2. 费用收缴数据
    ws_fee = wb['👨💼费用收缴👨💼']
    for row in ws_fee.iter_rows(min_row=2, values_only=True):
        payment_date = parse_excel_date(row[10]) if len(row) > 10 else None
        if payment_date and start_date <= payment_date <= end_date:
            data['费用记录'].append({
                '单元号': row[1],
                '费项项目': row[3],
                '应收金额': row[4],
                '已收金额': row[6],
                '欠收金额': row[8],
                '是否支付': row[9],
                '付款截止日期': row[10]
            })
    
    # 3. C+服务记录数据
    ws_service = wb['C+服务记录']
    for row in ws_service.iter_rows(min_row=2, values_only=True):
        service_date = parse_excel_date(row[1])
        if service_date and start_date <= service_date <= end_date:
            data['服务记录'].append({
                '租户名': row[0],
                '走访时间': row[1],
                '走访管家': row[2],
                '客户情绪': row[3],
                '成交情况': row[4],
                '服务类别': row[5],
                '详情记录': row[7]
            })
    
    # 4. 报事报修数据（如果有此工作表）
    if '报事报修' in wb.sheetnames:
        ws_repair = wb['报事报修']
        for row in ws_repair.iter_rows(min_row=2, values_only=True):
            report_date = parse_excel_date(row[0]) if row else None
            if report_date and start_date <= report_date <= end_date:
                data['报修记录'].append({
                    '报修时间': row[0],
                    '单元号': row[1],
                    '报修内容': row[2],
                    '处理状态': row[3],
                    '处理时长': row[4] if len(row) > 4 else None
                })
    
    # 5. 能耗数据
    ws_energy = wb['👨💼能耗收缴👨💼']
    for row in ws_energy.iter_rows(min_row=2, values_only=True):
        # 能耗数据按月份筛选
        month_str = row[6] if len(row) > 6 else ''  # 月份字段
        if month_str and f'{year}年{start_month}月' <= month_str <= f'{year}年{end_month}月':
            data['能耗数据'].append({
                '单元号': row[0],
                '租户名': row[1],
                '应收金额': row[2],
                '已收金额': row[3],
                '欠费金额': row[4],
                '是否支付': row[5]
            })
    
    return data
```

### 2. 数据分析模块

```python
def analyze_operations_data(data):
    """
    分析运营数据，生成分析结果
    
    Args:
        data: collect_operations_data 的输出
    
    Returns:
        dict: 分析结果
    """
    analysis = {
        '客户健康度': {},
        '园区出租率': {},
        '客户满意度': {},
        '重大风险预警': []
    }
    
    # 1. 客户健康度评估
    customer_health = {}
    for customer in data['客户档案']:
        unit_no = customer['单元号']
        tenant_name = customer['租户名']
        
        # 计算缴费准时率
        customer_fees = [f for f in data['费用记录'] if f['单元号'] == unit_no]
        on_time_payments = len([f for f in customer_fees if f['是否支付'] == '是'])
        total_payments = len(customer_fees)
        payment_rate = on_time_payments / total_payments if total_payments > 0 else 1.0
        
        # 计算服务满意度
        customer_services = [s for s in data['服务记录'] if s['租户名'] == tenant_name]
        satisfied_services = len([s for s in customer_services if s['客户情绪'] == '满意'])
        total_services = len(customer_services)
        satisfaction_rate = satisfied_services / total_services if total_services > 0 else 1.0
        
        # 计算报修响应速度
        customer_repairs = [r for r in data['报修记录'] if r['单元号'] == unit_no]
        avg_repair_time = 0
        if customer_repairs:
            repair_times = [r['处理时长'] for r in customer_repairs if r.get('处理时长')]
            avg_repair_time = sum(repair_times) / len(repair_times) if repair_times else 0
        
        # 综合健康度评分
        health_score = 0
        if payment_rate >= 0.95 and satisfaction_rate >= 0.8 and avg_repair_time <= 24:
            health_score = 90  # 健康
        elif payment_rate >= 0.9 and satisfaction_rate >= 0.6 and avg_repair_time <= 48:
            health_score = 70  # 良好
        elif payment_rate >= 0.8 and satisfaction_rate >= 0.4:
            health_score = 50  # 一般
        else:
            health_score = 30  # 风险
        
        customer_health[unit_no] = {
            '租户名': tenant_name,
            '健康度评分': health_score,
            '缴费准时率': round(payment_rate * 100, 2),
            '服务满意度': round(satisfaction_rate * 100, 2),
            '平均报修响应小时': round(avg_repair_time, 2),
            '等级': customer['等级']
        }
    
    analysis['客户健康度'] = customer_health
    
    # 2. 园区出租率趋势
    total_units = len(data['客户档案'])  # 简化：假设所有签约客户都是出租的
    # TODO: 实际应该对接园区总单元数
    occupancy_rate = 100.0  # 简化：假设100%出租率
    
    # 计算续租率
    # TODO: 需要历史数据对比
    renewal_rate = 0  # 简化
    
    analysis['园区出租率'] = {
        '出租率': occupancy_rate,
        '续租率': renewal_rate,
        '季度新增': 0,  # TODO: 需要计算新增客户
        '季度退租': 0   # TODO: 需要计算退租客户
    }
    
    # 3. 客户满意度趋势
    total_services = len(data['服务记录'])
    satisfied_count = len([s for s in data['服务记录'] if s['客户情绪'] == '满意'])
    overall_satisfaction = (satisfied_count / total_services * 100) if total_services > 0 else 0
    
    analysis['客户满意度'] = {
        '整体满意度': round(overall_satisfaction, 2),
        '服务次数': total_services,
        '满意次数': satisfied_count
    }
    
    # 4. 重大风险预警
    risks = []
    
    # 风险1：欠费风险
    overdue_customers = {}
    for fee in data['费用记录']:
        if fee['是否支付'] == '否':
            unit_no = fee['单元号']
            if unit_no not in overdue_customers:
                overdue_customers[unit_no] = {'欠费总额': 0, '逾期天数': 0}
            overdue_customers[unit_no]['欠费总额'] += float(fee['欠收金额'] or 0)
            
            # 计算逾期天数
            due_date = parse_excel_date(fee['付款截止日期'])
            if due_date:
                overdue_days = (datetime.now().date() - due_date).days
                overdue_customers[unit_no]['逾期天数'] = max(overdue_customers[unit_no]['逾期天数'], overdue_days)
    
    for unit_no, overdue_info in overdue_customers.items():
        if overdue_info['逾期天数'] > 30 or overdue_info['欠费总额'] > 10000:
            risks.append({
                '风险类型': '欠费风险',
                '单元号': unit_no,
                '风险描述': f"欠费¥{overdue_info['欠费总额']:.2f}，逾期{overdue_info['逾期天数']}天",
                '严重程度': '高' if overdue_info['逾期天数'] > 60 else '中'
            })
    
    # 风险2：服务满意度下降
    for unit_no, health in customer_health.items():
        if health['服务满意度'] < 60:
            risks.append({
                '风险类型': '满意度风险',
                '单元号': unit_no,
                '风险描述': f"服务满意度{health['服务满意度']}%，低于60%",
                '严重程度': '中'
            })
    
    # 风险3：报修响应慢
    for unit_no, health in customer_health.items():
        if health['平均报修响应小时'] > 48:
            risks.append({
                '风险类型': '服务效率风险',
                '单元号': unit_no,
                '风险描述': f"平均报修响应{health['平均报修响应小时']}小时，超过48小时",
                '严重程度': '中'
            })
    
    analysis['重大风险预警'] = risks
    
    return analysis
```

### 3. 任务分发模块

```python
def generate_quarterly_report(data, analysis, output_format='markdown'):
    """
    生成《季度运营监测报告》
    
    Args:
        data: collect_operations_data 的输出
        analysis: analyze_operations_data 的输出
        output_format: 输出格式（'markdown' 或 'docx'）
    
    Returns:
        str: 报告内容（Markdown格式）或 docx 文件路径
    """
    quarter = data['季度']
    
    # 构建报告内容
    report = f"""# 季度运营监测报告

**报告季度**：{quarter}  
**报告时间**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**编制单位**：示例集团产城园区运营有限公司  

---

## 一、客户健康度评估

### 1.1 整体健康度分布

| 健康度等级 | 企业数量 | 占比 |
|-----------|---------|------|
| 健康（≥80分） | {len([c for c in analysis['客户健康度'].values() if c['健康度评分'] >= 80])} | {len([c for c in analysis['客户健康度'].values() if c['健康度评分'] >= 80]) / len(analysis['客户健康度']) * 100:.1f}% |
| 良好（60-79分） | {len([c for c in analysis['客户健康度'].values() if 60 <= c['健康度评分'] < 80])} | {len([c for c in analysis['客户健康度'].values() if 60 <= c['健康度评分'] < 80]) / len(analysis['客户健康度']) * 100:.1f}% |
| 一般（40-59分） | {len([c for c in analysis['客户健康度'].values() if 40 <= c['健康度评分'] < 60])} | {len([c for c in analysis['客户健康度'].values() if 40 <= c['健康度评分'] < 60]) / len(analysis['客户健康度']) * 100:.1f}% |
| 风险（<40分） | {len([c for c in analysis['客户健康度'].values() if c['健康度评分'] < 40])} | {len([c for c in analysis['客户健康度'].values() if c['健康度评分'] < 40]) / len(analysis['客户健康度']) * 100:.1f}% |

### 1.2 重点客户健康度详情

以下是健康度评分前10和后10的客户：

**健康度最高的10个客户**：

| 单元号 | 租户名 | 健康度评分 | 缴费准时率 | 服务满意度 | 等级 |
|--------|--------|------------|------------|------------|------|
"""

    # 按健康度评分排序
    sorted_customers = sorted(analysis['客户健康度'].items(), key=lambda x: x[1]['健康度评分'], reverse=True)
    
    # 前10
    for i, (unit_no, health) in enumerate(sorted_customers[:10]):
        report += f"| {unit_no} | {health['租户名']} | {health['健康度评分']} | {health['缴费准时率']}% | {health['服务满意度']}% | {health['等级']} |\n"
    
    report += "\n**健康度最低的10个客户**：\n\n"
    report += "| 单元号 | 租户名 | 健康度评分 | 缴费准时率 | 服务满意度 | 等级 |\n"
    report += "|--------|--------|------------|------------|------------|------|\n"
    
    # 后10
    for i, (unit_no, health) in enumerate(sorted_customers[-10:]):
        report += f"| {unit_no} | {health['租户名']} | {health['健康度评分']} | {health['缴费准时率']}% | {health['服务满意度']}% | {health['等级']} |\n"
    
    report += f"""
---

## 二、园区出租率趋势

| 指标 | 数值 |
|------|------|
| 出租率 | {analysis['园区出租率']['出租率']}% |
| 续租率 | {analysis['园区出租率']['续租率']}% |
| 季度新增企业 | {analysis['园区出租率']['季度新增']} 家 |
| 季度退租企业 | {analysis['园区出租率']['季度退租']} 家 |

---

## 三、客户满意度趋势

| 指标 | 数值 |
|------|------|
| 整体满意度 | {analysis['客户满意度']['整体满意度']}% |
| 服务次数 | {analysis['客户满意度']['服务次数']} 次 |
| 满意次数 | {analysis['客户满意度']['满意次数']} 次 |

---

## 四、重大风险预警

**共发现 {len(analysis['重大风险预警'])} 项重大风险**：

"""

    # 按严重程度排序
    sorted_risks = sorted(analysis['重大风险预警'], key=lambda x: {'高': 0, '中': 1, '低': 2}[x['严重程度']])
    
    for i, risk in enumerate(sorted_risks):
        report += f"""
### 风险 {i+1}：{risk['风险类型']}（严重程度：{risk['严重程度']}）

- **单元号**：{risk['单元号']}
- **风险描述**：{risk['风险描述']}
- **建议措施**：
  - {'立即启动催缴程序，安排专人跟进' if risk['风险类型'] == '欠费风险' else ''}
  - {'安排管家上门走访，了解不满意原因，制定改进方案' if risk['风险类型'] == '满意度风险' else ''}
  - {'优化报修流程，增加维修人员配置，缩短响应时间' if risk['风险类型'] == '服务效率风险' else ''}

"""
    
    report += f"""
---

## 五、改进建议

基于以上分析，提出以下改进建议：

1. **针对健康度低的客户**：
   - 安排专属管家上门走访
   - 制定个性化服务方案
   - 建立定期沟通机制

2. **针对欠费风险**：
   - 启动分级催缴程序
   - 对高欠费客户安排法律程序
   - 优化账单提醒机制

3. **针对满意度下降**：
   - 开展客户服务培训
   - 建立服务反馈机制
   - 定期服务满意度调查

4. **针对报修响应时间长**：
   - 优化报事报修流程
   - 增加工程维修人员
   - 建立报修响应时效考核

---

**报告编制**：企服助手 (Enterprise Service Assistant)  
**报告版本**：V1.0  
**下次报告时间**：{quarter}结束后15个工作日内

"""
    
    if output_format == 'markdown':
        return report
    elif output_format == 'docx':
        # 使用 docx skill 生成 Word 文档
        # TODO: 调用 docx skill
        pass
```

### 4. 任务分发与跟踪模块

```python
def distribute_tasks(analysis, wecom_webhook):
    """
    根据分析结果，向责任部门分发任务单
    
    Args:
        analysis: analyze_operations_data 的输出
        wecom_webhook: 企微群 Webhook URL
    
    Returns:
        dict: 任务分发结果
    """
    tasks = {
        '招商部': [],
        '产业服务部': [],
        '物业服务中心': [],
        '财务部': []
    }
    
    # 1. 欠费风险 → 财务部 + 物业服务中心
    for risk in analysis['重大风险预警']:
        if risk['风险类型'] == '欠费风险':
            tasks['财务部'].append({
                '任务类型': '欠费催缴',
                '单元号': risk['单元号'],
                '任务描述': risk['风险描述'],
                '优先级': risk['严重程度'],
                '处理时限': '3个工作日' if risk['严重程度'] == '高' else '7个工作日'
            })
            tasks['物业服务中心'].append({
                '任务类型': '配合催缴',
                '单元号': risk['单元号'],
                '任务描述': '配合财务部进行欠费催缴，安排管家上门沟通',
                '优先级': risk['严重程度'],
                '处理时限': '3个工作日' if risk['严重程度'] == '高' else '7个工作日'
            })
    
    # 2. 满意度风险 → 产业服务部 + 物业服务中心
    for risk in analysis['重大风险预警']:
        if risk['风险类型'] == '满意度风险':
            tasks['产业服务部'].append({
                '任务类型': '满意度提升',
                '单元号': risk['单元号'],
                '任务描述': risk['风险描述'],
                '优先级': risk['严重程度'],
                '处理时限': '7个工作日'
            })
            tasks['物业服务中心'].append({
                '任务类型': '服务改进',
                '单元号': risk['单元号'],
                '任务描述': '制定服务改进方案，提升客户满意度',
                '优先级': risk['严重程度'],
                '处理时限': '7个工作日'
            })
    
    # 3. 服务效率风险 → 物业服务中心
    for risk in analysis['重大风险预警']:
        if risk['风险类型'] == '服务效率风险':
            tasks['物业服务中心'].append({
                '任务类型': '报修流程优化',
                '单元号': risk['单元号'],
                '任务描述': risk['风险描述'],
                '优先级': risk['严重程度'],
                '处理时限': '5个工作日'
            })
    
    # 4. 出租率下降风险 → 招商部
    if analysis['园区出租率']['续租率'] < 80:
        tasks['招商部'].append({
            '任务类型': '续租率提升',
            '任务描述': f"园区续租率{analysis['园区出租率']['续租率']}%，低于80%，需要制定续租提升方案",
            '优先级': '高',
            '处理时限': '15个工作日'
        })
    
    # 推送任务到企微群
    import requests
    
    for department, task_list in tasks.items():
        if not task_list:
            continue
        
        message = f"""
━━━━━━━━━━━━━━━
【运营监测任务分发】{datetime.now().strftime('%Y-%m-%d')}

**责任部门**：{department}
**任务数量**：{len(task_list)} 项

**任务清单**：

"""
        
        for i, task in enumerate(task_list):
            message += f"""
{i+1}. **{task['任务类型']}** （优先级：{task['优先级']}）
   - 单元号：{task.get('单元号', '全园区')}
   - 任务描述：{task['任务描述']}
   - 处理时限：{task['处理时限']}

"""
        
        message += """
请责任部门于处理时限内完成任务，并将处理结果反馈至企服助手。

━━━━━━━━━━━━━━━
"""
        
        # 推送到企微群
        if wecom_webhook:
            payload = {
                "msgtype": "text",
                "text": {
                    "content": message
                }
            }
            
            try:
                response = requests.post(wecom_webhook, json=payload, timeout=10)
                if response.status_code == 200:
                    print(f"✅ 任务已推送到{department}企微群")
                else:
                    print(f"❌ 推送失败：{response.text}")
            except Exception as e:
                print(f"❌ 推送异常：{e}")
    
    return tasks
```

---

## 执行流程

```
Step 1 → 数据收集
         读取Excel各工作表
         筛选指定季度数据
         整合多源数据

Step 2 → 数据分析
         客户健康度评估
         园区出租率趋势分析
         客户满意度趋势分析
         重大风险预警识别

Step 3 → 生成报告
         生成《季度运营监测报告》
         支持 Markdown 和 Word 格式

Step 4 → 任务分发
         根据风险类型分配责任部门
         推送任务单到企微群
         
Step 5 → 跟踪进度
         定期提醒责任部门处理
         跟踪任务完成状态
         更新任务状态
```

---

## 定时任务配置

```json
{
  "name": "季度运营监测报告生成",
  "schedule": {
    "kind": "cron",
    "expr": "0 9 15 1,4,7,10 *",
    "tz": "Asia/Shanghai"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "生成上季度运营监测报告，分析客户健康度、园区出租率、客户满意度，识别重大风险，分发任务单"
  },
  "sessionTarget": "isolated"
}
```

**说明**：每年1月15日、4月15日、7月15日、10月15日自动生成上季度报告。

---

## 手动触发方式

1. **企微 @提及**: `@企服助手 运营监测`
2. **OpenClaw指令**: `生成运营监测报告 [季度] [年份]`
   - 示例：`生成运营监测报告 1 2026` → 生成2026年第1季度报告

---

## 配置参数

```json
{
  "operations_monitoring": {
    "excel_path": "/Users/mac/示例产业园AC+服务.xlsx",
    "report_output_dir": "/Users/mac/运营监测报告/",
    "wecom_webhook": {
      "招商部": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx",
      "产业服务部": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx",
      "物业服务中心": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx",
      "财务部": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx"
    },
    "health_score_thresholds": {
      "健康": 80,
      "良好": 60,
      "一般": 40,
      "风险": 0
    },
    "risk_thresholds": {
      "欠费金额": 10000,
      "逾期天数": 30,
      "满意度": 60,
      "报修响应小时": 48
    }
  }
}
```

---

## 使用示例

**用户输入**: `@企服助手 运营监测` 或 `生成运营监测报告 1 2026`

**输出**:
```
━━━━━━━━━━━━━━━
【季度运营监测报告】2026年第1季度

━━━ 客户健康度评估 ━━━
健康（≥80分）：15家 (50.0%)
良好（60-79分）：9家 (30.0%)
一般（40-59分）：4家 (13.3%)
风险（<40分）：2家 (6.7%)

━━━ 园区出租率趋势 ━━━
出租率：95.0%
续租率：85.0%
季度新增：2家
季度退租：1家

━━━ 客户满意度趋势 ━━━
整体满意度：82.5%
服务次数：120次
满意次数：99次

━━━ 重大风险预警 ━━━
共发现 3 项重大风险：

1. 欠费风险（严重程度：高）
   单元号：T1-XXX
   风险描述：欠费¥15000.00，逾期45天
   
2. 满意度风险（严重程度：中）
   单元号：T1-XXX
   风险描述：服务满意度55%，低于60%
   
3. 服务效率风险（严重程度：中）
   单元号：T1-XXX
   风险描述：平均报修响应52小时，超过48小时

━━━ 任务分发 ━━━
已将任务推送到各部门企微群：
  • 财务部：1项任务
  • 产业服务部：1项任务
  • 物业服务中心：3项任务

⚡ 完整报告已保存至：/Users/mac/运营监测报告/2026Q1运营监测报告.md
━━━━━━━━━━━━━━━
```

---

## 后续扩展接口

1. **对接集客荟系统 API** - 实时获取客户档案、合同信息
2. **对接集享荟平台 API** - 实时获取报事报修数据
3. **对接集能荟系统 API** - 实时获取能耗数据
4. **对接门禁系统 API** - 获取客户活跃度数据
5. **预测性分析** - 基于历史数据预测未来风险
6. **可视化仪表盘** - 生成可视化图表（柱状图、折线图、饼图等）

---

## 注意事项

1. **数据准确性** - 确保Excel台账数据及时更新
2. **隐私保护** - 客户数据仅用于内部分析，不得外泄
3. **报告时效性** - 季度报告应在季度结束后15个工作日内完成
4. **任务跟踪** - 建立任务跟踪机制，确保任务按时完成

---

**当前状态**: 技能已创建，基于Excel台账实现基础数据分析功能。

**核心功能**: 数据收集、数据分析、报告生成、任务分发。

**未来扩展**: 对接各系统API，实现实时数据监控和预测性分析。
