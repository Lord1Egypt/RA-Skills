# SKILL.md

**License:** MIT  
**Copyright:** 2026 perrykono-debug

---

---
name: performance-exception
description: 履约异常管理技能。基于《园区运营项目客户服务标准指引》第六章"异动阶段"，实现履约异常识别、分级处理、法律程序触发自动化。触发场景：(1) 定时任务每日10:00检查履约异常，(2) 费用逾期30天自动触发异常处理，(3) 手动触发（@企服助手 履约异常）。
---

# 履约异常管理技能 (Performance Exception Skill)

> **本技能已自包含，无需安装 customer-management**
> 
> 本技能已内联客户管理相关逻辑（查询客户档案、构建客户画像），可直接独立运行。

## 功能概述

本技能用于自动化履约异常管理流程，基于《园区运营项目客户服务标准指引》（{TODO: 填写文件编号}）第六章，实现：
1. **履约异常识别**：自动识别欠费、违约、退租等异常情况
2. **分级处理流程**：根据异常等级自动触发相应处理流程（提醒→催缴→律师函→诉讼）
3. **法律程序触发**：欠费逾期超60天自动触发律师函，超90天自动提起诉讼
4. **处理过程记录**：所有处理过程自动记录，生成《履约异常处理报告》

---

## 数据源配置

**数据文件**: `/Users/mac/示例产业园AC+服务.xlsx`

**工作表映射**:
| 功能模块 | 工作表名 | 用途 |
|---------|----------|------|
| **客户档案** | 👨客户管理👨 | 客户基本信息、合同信息 |
| **费用收缴** | 👨💼费用收缴👨💼 | 费用记录、逾期统计 |
| **履约异常记录** | 履约异常记录（待建） | 履约异常记录、处理过程 |
| **法律程序记录** | 法律程序记录（待建） | 律师函、诉讼记录 |

**依赖技能**:
- `fee-collection`：获取欠费信息、生成催缴通知
- `contract-renewal`：处理退租、合同终止

---

## 客户管理逻辑（内联）

> 以下函数从 customer-management 技能内联，无需外部依赖。

### 1. 查询客户档案

```python
def query_customer_profile(unit_no=None, tenant_name=None, contract_no=None):
    """
    查询客户档案（内联自 customer-management 技能）
    
    Args:
        unit_no: 单元号（如 T1-601）
        tenant_name: 租户名（支持模糊匹配）
        contract_no: 合同号
    
    Returns:
        dict: 客户完整档案信息
    """
    import openpyxl
    
    wb = openpyxl.load_workbook('/Users/mac/示例产业园AC+服务.xlsx')
    ws = wb['👨客户管理👨']
    
    headers = [cell.value for cell in ws[1]]
    
    for row in ws.iter_rows(min_row=2, values_only=True):
        # 匹配条件
        if unit_no and row[5] == unit_no:  # 单元号
            return build_customer_dict(headers, row)
        if tenant_name and tenant_name in str(row[6]):  # 租户名模糊匹配
            return build_customer_dict(headers, row)
        if contract_no and row[4] == contract_no:  # 合同号
            return build_customer_dict(headers, row)
    
    return None

def build_customer_dict(headers, row):
    """
    构建客户字典
    
    Args:
        headers: 表头列表
        row: 数据行
    
    Returns:
        dict: 客户信息字典
    """
    customer = {}
    for i, header in enumerate(headers):
        if i < len(row):
            customer[header] = row[i]
    
    # 字段映射（便于访问）
    customer["单元号"] = row[5] if len(row) > 5 else ""
    customer["租户名"] = row[6] if len(row) > 6 else ""
    customer["合同号"] = row[4] if len(row) > 4 else ""
    customer["等级"] = row[15] if len(row) > 15 else "C"
    customer["租户联系人"] = row[14] if len(row) > 14 else "负责人"
    customer["电话"] = row[16] if len(row) > 16 else ""
    customer["开始日期"] = row[11] if len(row) > 11 else ""
    customer["截至日期"] = row[12] if len(row) > 12 else ""
    customer["状态"] = row[13] if len(row) > 13 else ""
    
    return customer
```

### 2. 构建客户画像

```python
def build_customer_portrait(unit_no):
    """
    构建客户画像 - 聚合多个数据源（内联自 customer-management 技能）
    
    Args:
        unit_no: 单元号（主键）
    
    Returns:
        dict: 客户画像（包含服务、费用、报修等汇总）
    """
    import openpyxl
    
    wb = openpyxl.load_workbook('/Users/mac/示例产业园AC+服务.xlsx')
    
    portrait = {
        "基础信息": query_customer_profile(unit_no),
        "服务记录": [],
        "费用记录": [],
        "能耗记录": [],
        "报修记录": [],
        "风险标记": []
    }
    
    if not portrait["基础信息"]:
        return portrait
    
    tenant_name = portrait["基础信息"]["租户名"]
    
    # 1. 查询C+服务记录（关联字段：租户名）
    ws_service = wb['C+服务记录']
    
    for row in ws_service.iter_rows(min_row=2, values_only=True):
        if row[0] == tenant_name:  # 关联客户字段
            portrait["服务记录"].append({
                "走访时间": row[1],
                "走访管家": row[2],
                "客户情绪": row[3],
                "成交情况": row[4],
                "服务类别": row[5],
                "成交金额": row[6],
                "详情记录": row[7]
            })
    
    # 2. 查询费用收缴记录（关联字段：单元号）
    ws_fee = wb['👨💼费用收缴👨💼']
    
    for row in ws_fee.iter_rows(min_row=2, values_only=True):
        if row[1] == unit_no:  # 单元号
            portrait["费用记录"].append({
                "合同编号": row[0],
                "费项项目": row[3],
                "应收金额": row[4],
                "已收金额": row[6],
                "欠收金额": row[8],
                "是否支付": row[9],
                "月份": row[13]
            })
    
    # 3. 查询能耗收缴记录（关联字段：单元号）
    ws_energy = wb['👨💼能耗收缴👨💼']
    
    for row in ws_energy.iter_rows(min_row=2, values_only=True):
        if row[0] == unit_no:  # 单元号
            portrait["能耗记录"].append({
                "租户名": row[1],
                "应收金额": row[2],
                "已收金额": row[3],
                "欠费金额": row[4],
                "是否支付": row[5],
                "月份": row[6]
            })
    
    # 4. 查询报修记录（关联字段：楼层/单元）
    ws_repair = wb['🛠️报修情况汇总🛠️']
    
    for row in ws_repair.iter_rows(min_row=2, values_only=True):
        if unit_no in str(row[0]):  # 楼层/单元匹配
            portrait["报修记录"].append({
                "楼层/单元": row[0],
                "紧急程度": row[1],
                "报修细节描述": row[2],
                "报修人员": row[4],
                "报修时间": row[5],
                "维修人员": row[6],
                "维修跟进状态": row[7]
            })
    
    # 5. 计算风险标记
    portrait["风险标记"] = calculate_risk_tags(portrait)
    
    return portrait

def calculate_risk_tags(portrait):
    """
    计算客户风险标记
    
    Returns:
        list: 风险标记列表（如 ["欠费风险", "流失风险"]）
    """
    import datetime
    
    risks = []
    
    # 1. 欠费风险判断
    欠费总额 = 0
    for fee in portrait["费用记录"]:
        if fee["是否支付"] == "否":
            欠费金额 = float(fee["欠收金额"]) if fee["欠收金额"] else 0
            欠费总额 += 欠费金额
    
    if 欠费总额 > 50000:
        risks.append(f"🚨 高欠费风险（欠费¥{欠费总额:.2f}）")
    elif 欠费总额 > 10000:
        risks.append(f"⚠️ 中度欠费风险（欠费¥{欠费总额:.2f}）")
    elif 欠费总额 > 0:
        risks.append(f"📢 轻度欠费提醒（欠费¥{欠费总额:.2f}）")
    
    # 2. 流失风险判断（续租预警）
    基础信息 = portrait["基础信息"]
    if 基础信息:
        try:
            截至日期 = parse_excel_date(基础信息["截至日期"])
            剩余天数 = (截至日期 - datetime.datetime.now().date()).days
            
            if 剩余天数 <= 30:
                risks.append(f"🚨 流失风险（合同剩余{剩余天数}天）")
            elif 剩余天数 <= 90:
                risks.append(f"⚠️ 续租预警（合同剩余{剩余天数}天）")
        except:
            pass
    
    # 3. 投诉/报修频率判断
    报修次数 = len(portrait["报修记录"])
    if 报修次数 >= 3:  # 最近报修次数>=3
        risks.append(f"⚠️ 高频报修（{报修次数}次）")
    
    # 4. 服务满意度判断
    满意记录 = [s for s in portrait["服务记录"] if s["客户情绪"] == "满意"]
    总记录 = len(portrait["服务记录"])
    
    if 总记录 > 0 and len(满意记录) / 总记录 < 0.5:
        risks.append(f"⚠️ 低满意度（满意率{len(满意记录)/总记录*100:.1f}%）")
    
    return risks
```

### 3. 辅助函数

```python
def parse_excel_date(date_value):
    """
    解析Excel日期（支持多种格式）
    
    Args:
        date_value: Excel日期值（可能是datetime、字符串等）
    
    Returns:
        datetime.date: 解析后的日期
    """
    import datetime
    
    if isinstance(date_value, datetime.datetime):
        return date_value.date()
    elif isinstance(date_value, datetime.date):
        return date_value
    elif isinstance(date_value, str):
        # 尝试解析各种格式
        date_str = date_value.strip()
        
        # 格式：2025年3月1日
        try:
            # 简单解析（生产环境建议使用 dateutil）
            import re
            match = re.search(r'(\d{4})年(\d{1,2})月(\d{1,2})日', date_str)
            if match:
                return datetime.date(int(match.group(1)), int(match.group(2)), int(match.group(3)))
        except:
            pass
        
        # 格式：2025-03-01
        try:
            return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        except:
            pass
    
    return None
```

---

## 核心逻辑

### 1. 履约异常识别模块

```python
def identify_performance_exceptions(days_threshold=30):
    """
    识别履约异常情况
    
    Args:
        days_threshold: 逾期天数阈值（默认30天）
    
    Returns:
        list: 履约异常列表
    """
    import openpyxl
    import datetime
    
    wb = openpyxl.load_workbook('/Users/mac/示例产业园AC+服务.xlsx')
    
    exceptions = []
    
    # 1. 识别欠费异常
    ws_fee = wb['👨💼费用收缴👨💼']
    
    for row in ws_fee.iter_rows(min_row=2, values_only=True):
        unit_no = row[1]
        fee_type = row[3]
        overdue_amount = float(row[8]) if row[8] else 0
        is_paid = row[9]
        due_date = parse_excel_date(row[10])
        
        # 判断是否欠费
        if is_paid == '否' and overdue_amount > 0 and due_date:
            overdue_days = (datetime.datetime.now().date() - due_date).days
            
            # 逾期超过阈值
            if overdue_days >= days_threshold:
                # 获取客户信息（直接调用内联函数）
                customer_profile = query_customer_profile(unit_no=unit_no)
                
                tenant_name = customer_profile.get("租户名", "") if customer_profile else "未知"
                level = customer_profile.get("等级", "C") if customer_profile else "C"
                
                exceptions.append({
                    '异常类型': '欠费',
                    '单元号': unit_no,
                    '租户名': tenant_name,
                    '等级': level,
                    '逾期天数': overdue_days,
                    '欠费金额': overdue_amount,
                    '费项项目': fee_type,
                    '付款截止日期': due_date.strftime('%Y-%m-%d'),
                    '严重程度': '高' if overdue_days > 60 else ('中' if overdue_days > 30 else '低')
                })
    
    # 2. 识别违约异常（模拟）
    # TODO: 基于合同条款检查违约情况（如擅自改变房屋用途、擅自转租等）
    
    # 3. 识别退租异常（模拟）
    # TODO: 检查退租流程是否合规、场地验收是否合格等
    
    return exceptions
```

### 2. 分级处理流程模块

```python
def trigger_exception_handling(exception):
    """
    根据履约异常等级触发相应处理流程
    
    Args:
        exception: 履约异常字典
    
    Returns:
        dict: 处理结果
    """
    exception_type = exception['异常类型']
    severity = exception['严重程度']
    unit_no = exception['单元号']
    tenant_name = exception['租户名']
    overdue_days = exception.get('逾期天数', 0)
    overdue_amount = exception.get('欠费金额', 0)
    
    handling_steps = []
    
    # 根据异常类型和严重程度触发不同处理流程
    if exception_type == '欠费':
        if severity == '低':
            # 低严重程度：提醒 + 电话跟进
            handling_steps = [
                {'步骤': '发送提醒通知', '责任人': '管家', '时限': '1个工作日'},
                {'步骤': '电话跟进', '责任人': '管家', '时限': '3个工作日内'},
                {'步骤': '记录沟通情况', '责任人': '管家', '时限': '跟进后1个工作日内'}
            ]
            
            # 发送提醒通知
            notification = send_payment_reminder(unit_no, tenant_name, overdue_days, overdue_amount)
            
        elif severity == '中':
            # 中严重程度：正式催缴 + 上门沟通
            handling_steps = [
                {'步骤': '发送正式催缴通知', '责任人': '财务部', '时限': '1个工作日'},
                {'步骤': '上门沟通', '责任人': '管家 + 财务部', '时限': '5个工作日内'},
                {'步骤': '制定还款计划', '责任人': '财务部', '时限': '沟通后3个工作日内'},
                {'步骤': '跟踪还款进度', '责任人': '管家', '时限': '每周跟进'}
            ]
            
            # 发送正式催缴通知
            notification = send_formal_payment_notice(unit_no, tenant_name, overdue_days, overdue_amount)
            
        else:  # 高严重程度
            # 高严重程度：律师函 + 法律程序
            handling_steps = [
                {'步骤': '发送律师函', '责任人': '法务部', '时限': '3个工作日内'},
                {'步骤': '提起诉讼', '责任人': '法务部', '时限': '律师函发出后30天'},
                {'步骤': '申请强制执行', '责任人': '法务部', '时限': '判决生效后'}
            ]
            
            # 发送律师函
            notification = send_lawyer_letter(unit_no, tenant_name, overdue_days, overdue_amount)
    
    # 记录处理过程
    record = record_exception_handling(exception, handling_steps, notification)
    
    return {
        '状态': '处理流程已触发',
        '异常类型': exception_type,
        '严重程度': severity,
        '处理步骤': handling_steps,
        '通知状态': notification,
        '处理记录': record
    }

def send_payment_reminder(unit_no, tenant_name, overdue_days, overdue_amount):
    """
    发送付款提醒通知（温和）
    
    Args:
        unit_no: 单元号
        tenant_name: 租户名
        overdue_days: 逾期天数
        overdue_amount: 欠费金额
    
    Returns:
        str: 通知状态
    """
    # 获取客户联系人信息（直接调用内联函数）
    customer_profile = query_customer_profile(unit_no=unit_no)
    
    contact_person = customer_profile.get("租户联系人", "负责人") if customer_profile else "负责人"
    
    # 构建提醒消息
    message = f"""
━━━━━━━━━━━━━━━
【付款提醒】

尊敬的{tenant_name}（联系人：{contact_person}）：

希望贵司业务蒸蒸日上😊

顺便提醒一下，贵司的场地费用（¥{overdue_amount:.2f}）已逾期{overdue_days}天。

如果有什么困难或疑问，欢迎随时沟通，我们尽力协助解决。

麻烦方便时安排付款，谢谢配合！

━━━ 付款信息 ━━━
• 收款单位：深圳市示例集团产城园区运营有限公司
• 银行账号：XXXXXXXXXXXXXXXX
• 开户银行：XX银行XX支行

如有疑问，请于3个工作日内联系我们。

谢谢配合！
━━━━━━━━━━━━━━━
"""
    
    # TODO: 对接企微API/邮件/短信发送通知
    print(message)
    
    return "提醒通知已发送"

def send_formal_payment_notice(unit_no, tenant_name, overdue_days, overdue_amount):
    """
    发送正式催缴通知
    
    Args:
        unit_no: 单元号
        tenant_name: 租户名
        overdue_days: 逾期天数
        overdue_amount: 欠费金额
    
    Returns:
        str: 通知状态
    """
    # 获取客户联系人信息（直接调用内联函数）
    customer_profile = query_customer_profile(unit_no=unit_no)
    
    contact_person = customer_profile.get("租户联系人", "负责人") if customer_profile else "负责人"
    
    # 构建正式催缴消息
    message = f"""
━━━━━━━━━━━━━━━
【催缴通知】

致：{tenant_name}（联系人：{contact_person}）

关于：场地费用催缴事宜

贵司租赁我司园区{unit_no}单元，截至本通知发出之日，贵司已逾期支付场地费用共计 **¥{overdue_amount:.2f}**，逾期天数：**{overdue_days}天**。

根据贵我双方签订的《租赁合同》第X条约定，贵司应于每[月/季]的第X日前支付当期场地费用。贵司逾期支付的行为已构成违约。

现我司正式通知贵司：
1. 请于本通知发出之日起**3个工作日内**付清全部欠款；
2. 请于**3个工作日内**支付逾期违约金（按日万分之X计算）；
3. 如贵司未能在上述期限内付清全部欠款及违约金，我司将保留采取进一步法律措施的权利，包括但不限于：
   - 解除合同
   - 收回租赁场地
   - 追究违约责任
   - 提起诉讼

特此通知！

━━━ 付款信息 ━━━
• 收款单位：深圳市示例集团产城园区运营有限公司
• 银行账号：XXXXXXXXXXXXXXXX
• 开户银行：XX银行XX支行

如有疑问，请于3个工作日内联系我们：
• 联系人：XX经理
• 联系电话：0755-XXXXXXX
• 电子邮箱：XXXX@{TODO: 填写邮箱域名}

谢谢配合！
━━━━━━━━━━━━━━━
"""
    
    # TODO: 对接企微API/邮件/短信发送通知
    print(message)
    
    return "正式催缴通知已发送"

def send_lawyer_letter(unit_no, tenant_name, overdue_days, overdue_amount):
    """
    发送律师函
    
    Args:
        unit_no: 单元号
        tenant_name: 租户名
        overdue_days: 逾期天数
        overdue_amount: 欠费金额
    
    Returns:
        str: 通知状态
    """
    # TODO: 对接法务系统，自动生成律师函并发送
    # TODO: 记录律师函发送时间、函号等信息
    
    message = f"""
━━━━━━━━━━━━━━━
【律师函】

致：{tenant_name}

关于：场地费用催缴事宜

受深圳市示例集团产城园区运营有限公司（以下简称"我委托人"）委托，就贵司租赁我委托人园区{unit_no}单元场地费用逾期支付事宜，特向贵司发出本律师函：

一、事实依据
贵我双方于XXXX年XX月XX日签订《租赁合同》，约定贵司租赁我委托人园区{unit_no}单元，租赁期限自XXXX年XX月XX日至XXXX年XX月XX日。根据合同约定，贵司应于每[月/季]的第X日前支付当期场地费用。

截至本函发出之日，贵司已逾期支付场地费用共计 **¥{overdue_amount:.2f}**，逾期天数：**{overdue_days}天**。

二、法律依据
根据《中华人民共和国民法典》第七百二十二条、《中华人民共和国合同法》第二百二十七条（注：民法典实施后，合同法已废止，此处仅为示例）等相关法律规定，承租人无正当理由未支付或者迟延支付租金的，出租人可以请求承租人在合理期限内支付；承租人逾期不支付的，出租人可以解除合同。

三、律师函要求
鉴于贵司的违约行为，我委托人特委托本律师向贵司正式函告如下：
1. 请于本函发出之日起**7个工作日内**付清全部欠款及违约金；
2. 如贵司未能在上述期限内付清全部欠款及违约金，我委托人将依法解除《租赁合同》，收回租赁场地，并追究贵司的违约责任；
3. 届时，我委托人将向法院提起诉讼，要求贵司支付欠款、违约金、律师费、诉讼费等相关费用。

四、特别提醒
请贵司高度重视本函内容，按时履行付款义务，以免诉累。

特此函告！

━━━ 联系方式 ━━━
• 律师事务所：XX律师事务所
• 经办律师：XX律师
• 联系电话：0755-XXXXXXX
• 电子邮箱：XXXX@lawfirm.com

XX律师事务所
XXXX年XX月XX日
━━━━━━━━━━━━━━━
"""
    
    # TODO: 对接企微API/邮件/短信发送通知
    print(message)
    
    return "律师函已发送"
```

### 3. 法律程序触发模块

```python
def trigger_legal_proceedings(exception):
    """
    触发法律程序（欠费逾期超90天）
    
    Args:
        exception: 履约异常字典
    
    Returns:
        dict: 法律程序触发结果
    """
    import datetime
    
    unit_no = exception['单元号']
    tenant_name = exception['租户名']
    overdue_days = exception['逾期天数']
    overdue_amount = exception['欠费金额']
    
    # 1. 检查是否已经触发法律程序
    legal_status = check_legal_status(unit_no)
    
    if legal_status['状态'] != '未启动':
        return {'状态': '法律程序已启动', '当前状态': legal_status['状态']}
    
    # 2. 欠费逾期超90天 → 自动触发诉讼
    if overdue_days >= 90:
        # 生成《起诉书》
        indictment = generate_indictment(unit_no, tenant_name, overdue_days, overdue_amount)
        
        # 准备诉讼材料
        legal_materials = prepare_legal_materials(unit_no, tenant_name)
        
        # 提交法院（模拟）
        submission = submit_to_court(indictment, legal_materials)
        
        # 记录法律程序
        record = record_legal_proceedings(unit_no, tenant_name, '诉讼', indictment, submission)
        
        return {
            '状态': '诉讼已启动',
            '起诉书': indictment,
            '诉讼材料': legal_materials,
            '提交状态': submission,
            '记录': record
        }
    
    # 3. 欠费逾期超60天 → 自动触发律师函
    elif overdue_days >= 60:
        # 检查是否已发律师函
        if legal_status['状态'] == '律师函已发':
            return {'状态': '律师函已发送，等待中', '发送日期': legal_status['发送日期']}
        
        # 发送律师函
        notification = send_lawyer_letter(unit_no, tenant_name, overdue_days, overdue_amount)
        
        # 记录法律程序
        record = record_legal_proceedings(unit_no, tenant_name, '律师函', notification)
        
        return {
            '状态': '律师函已发送',
            '通知状态': notification,
            '记录': record
        }
    
    else:
        return {'状态': '未达到法律程序触发条件', '逾期天数': overdue_days}

def check_legal_status(unit_no):
    """
    检查法律程序状态
    
    Args:
        unit_no: 单元号
    
    Returns:
        dict: 法律程序状态
    """
    # TODO: 读取"法律程序记录"工作表
    # 模拟返回
    return {
        '状态': '未启动',
        '发送日期': None,
        '诉讼日期': None
    }

def generate_indictment(unit_no, tenant_name, overdue_days, overdue_amount):
    """
    生成《起诉书》
    
    Args:
        unit_no: 单元号
        tenant_name: 租户名
        overdue_days: 逾期天数
        overdue_amount: 欠费金额
    
    Returns:
        str: 起诉书文件路径
    """
    import datetime
    import os
    
    # 构建起诉书内容
    indictment_content = f"""
# 民事起诉状

**原告**：深圳市示例集团产城园区运营有限公司
**法定代表人**：XXX  职务：董事长
**住所地**：深圳市XXX区XXX路XXX号

**被告**：{tenant_name}
**法定代表人**：XXX  职务：XXX
**住所地**：XXX

**案由**：房屋租赁合同纠纷

**诉讼请求**：

1. 判令被告立即支付场地租金人民币 **¥{overdue_amount:.2f}** 及逾期违约金（按日万分之X计算，自逾期之日起至实际付清之日止）；
2. 判令被告立即腾退并向原告返还租赁场地（深圳市XXX区XXX路XXX号示例集团产城园区{unit_no}单元）；
3. 判令被告承担本案全部诉讼费用。

**事实与理由**：

XXXX年XX月XX日，原、被告双方签订《租赁合同》（合同编号：ZJML-XXXX-XXXXXXXX），约定被告租赁原告园区{unit_no}单元，租赁期限自XXXX年XX月XX日至XXXX年XX月XX日，租金为人民币XXX元/月。

合同生效后，原告依约向被告交付了租赁场地，但被告未依约支付租金。截至起诉之日，被告已逾期支付租金共计人民币 **¥{overdue_amount:.2f}**，逾期天数：**{overdue_days}天**。

原告曾多次与被告沟通，并于XXXX年XX月XX日向被告发出《律师函》，催促被告支付欠款，但被告至今仍未支付。

被告的行为已严重违反合同约定，损害了原告的合法权益。为维护原告的合法权益，特向贵院提起诉讼，恳请贵院依法支持原告的全部诉讼请求。

此致
深圳市XXX区人民法院

**具状人**：深圳市示例集团产城园区运营有限公司
**日期**：{datetime.datetime.now().strftime('%Y年%m月%d日')}

---

**附件**：
1. 《租赁合同》复印件
2. 场地交付验收单复印件
3. 催缴通知函复印件
4. 律师函复印件
5. 欠费明细表
6. 原告营业执照复印件
7. 法定代表人身份证明书
"""
    
    # 保存为Markdown文件
    output_dir = "/Users/mac/法律程序文件/起诉书/"
    os.makedirs(output_dir, exist_ok=True)
    
    file_path = f"{output_dir}{unit_no}_{tenant_name}_起诉书_{datetime.datetime.now().strftime('%Y%m%d')}.md"
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(indictment_content)
    
    # TODO: 可选：转换为PDF
    
    return file_path

def prepare_legal_materials(unit_no, tenant_name):
    """
    准备诉讼材料
    
    Args:
        unit_no: 单元号
        tenant_name: 租户名
    
    Returns:
        list: 诉讼材料清单
    """
    # TODO: 自动收集、整理诉讼材料
    materials = [
        "《租赁合同》复印件",
        "场地交付验收单复印件",
        "催缴通知函",
        "律师函",
        "欠费明细表",
        "原告营业执照复印件",
        "法定代表人身份证明书",
        "被告工商登记信息",
        "授权委托书",
        "证据清单"
    ]
    
    return materials

def submit_to_court(indictment, legal_materials):
    """
    提交法院（模拟函数）
    
    Args:
        indictment: 起诉书文件路径
        legal_materials: 诉讼材料清单
    
    Returns:
        dict: 提交状态
    """
    import datetime
    
    # TODO: 对接法院电子诉讼平台，实现在线立案
    return {
        '状态': '已提交',
        '提交时间': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        '案号': '（2026）粤XX民初XX号',  # 模拟案号
        '承办法官': 'XXX法官',
        '开庭时间': (datetime.datetime.now() + datetime.timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
    }

def record_legal_proceedings(unit_no, tenant_name, proceeding_type, content, submission=None):
    """
    记录法律程序
    
    Args:
        unit_no: 单元号
        tenant_name: 租户名
        proceeding_type: 程序类型（'律师函' 或 '诉讼'）
        content: 内容（律师函消息或起诉书路径）
        submission: 提交状态（仅诉讼需要）
    
    Returns:
        str: 记录文件路径
    """
    import datetime
    import os
    
    # 构建记录内容
    record_content = f"""
# 法律程序记录

**单元号**：{unit_no}
**租户名**：{tenant_name}
**程序类型**：{proceeding_type}
**记录时间**：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 一、程序内容

"""
    
    if proceeding_type == '律师函':
        record_content += f"""**律师函发送记录**：

```text
{content}
```

"""
    else:  # 诉讼
        record_content += f"""**起诉书**：{content}

**诉讼材料清单**：

"""
        for i, material in enumerate(submission.get('诉讼材料', [])):
            record_content += f"{i+1}. {material}\n"
        
        record_content += f"""
**提交状态**：

- 状态：{submission['状态']}
- 提交时间：{submission['提交时间']}
- 案号：{submission['案号']}
- 承办法官：{submission['承办法官']}
- 开庭时间：{submission['开庭时间']}

"""
    
    record_content += """
## 二、处理过程记录

| 时间 | 处理人 | 处理内容 | 结果 |
|------|--------|----------|------|
|  |  |  |  |

---

## 三、处理结果

□ 已解决（欠款已收回）
□ 审理中（等待法院判决）
□ 已判决（等待执行）
□ 已执行完毕

---

**备注**：
1. 本记录一式两份，法务部、物业服务中心各执一份
2. 处理完毕后，请将处理结果填写在上述"三、处理结果"中

**编制**：企服助手 (Enterprise Service Assistant)
**版本**：V1.0
"""
    
    # 保存为Markdown文件
    output_dir = "/Users/mac/法律程序记录/"
    os.makedirs(output_dir, exist_ok=True)
    
    file_path = f"{output_dir}{unit_no}_{tenant_name}_{proceeding_type}记录_{datetime.datetime.now().strftime('%Y%m%d')}.md"
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(record_content)
    
    return file_path
```

### 4. 处理过程记录模块

```python
def record_exception_handling(exception, handling_steps, notification):
    """
    记录履约异常处理过程
    
    Args:
        exception: 履约异常字典
        handling_steps: 处理步骤列表
        notification: 通知状态
    
    Returns:
        str: 记录文件路径
    """
    import datetime
    import os
    
    unit_no = exception['单元号']
    tenant_name = exception['租户名']
    exception_type = exception['异常类型']
    severity = exception['严重程度']
    
    # 构建记录内容
    record_content = f"""
# 履约异常处理记录

**单元号**：{unit_no}
**租户名**：{tenant_name}
**异常类型**：{exception_type}
**严重程度**：{severity}
**记录时间**：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 一、异常情况说明

| 字段 | 内容 |
|------|------|
| 异常类型 | {exception_type} |
| 严重程度 | {severity} |
| 逾期天数 | {exception.get('逾期天数', 'N/A')} |
| 欠费金额 | ¥{exception.get('欠费金额', 0):.2f} |
| 费项项目 | {exception.get('费项项目', 'N/A')} |
| 付款截止日期 | {exception.get('付款截止日期', 'N/A')} |

---

## 二、处理步骤

| 序号 | 步骤 | 责任人 | 时限 | 状态 | 完成时间 |
|------|------|--------|------|------|----------|
"""
    
    for i, step in enumerate(handling_steps):
        record_content += f"| {i+1} | {step['步骤']} | {step['责任人']} | {step['时限']} | 待处理 |  |\n"
    
    record_content += f"""
---

## 三、通知记录

```text
{notification}
```

---

## 四、处理过程记录

| 时间 | 处理人 | 处理内容 | 结果 |
|------|--------|----------|------|
|  |  |  |  |

---

## 五、处理结果

□ 已解决（欠款已收回/违约已纠正/退租已完成）
□ 处理中（正在沟通/正在诉讼/正在执行）
□ 未解决（沟通无果/诉讼失败/执行不能）

---

**备注**：
1. 本记录一式两份，责任部门、物业服务中心各执一份
2. 处理完毕后，请将处理结果填写在上述"五、处理结果"中
3. 如启动法律程序，请将法律文书复印件附后

**编制**：企服助手 (Enterprise Service Assistant)
**版本**：V1.0
"""
    
    # 保存为Markdown文件
    output_dir = "/Users/mac/履约异常处理记录/"
    os.makedirs(output_dir, exist_ok=True)
    
    file_path = f"{output_dir}{unit_no}_{tenant_name}_履约异常处理记录_{datetime.datetime.now().strftime('%Y%m%d')}.md"
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(record_content)
    
    # 同时写入Excel"履约异常记录"工作表（待建）
    # TODO: 创建"履约异常记录"工作表，记录处理过程
    
    return file_path

def generate_exception_handling_report(start_date, end_date):
    """
    生成《履约异常处理报告》
    
    Args:
        start_date: 开始日期
        end_date: 结束日期
    
    Returns:
        str: 报告文件路径
    """
    import datetime
    import os
    
    # 1. 读取"履约异常记录"工作表（待建）
    # TODO: 实现
    
    # 模拟数据
    exceptions = [
        {'单元号': 'T1-601', '租户名': '企业A', '异常类型': '欠费', '严重程度': '高', '状态': '已解决'},
        {'单元号': 'T1-602', '租户名': '企业B', '异常类型': '欠费', '严重程度': '中', '状态': '处理中'},
        {'单元号': 'T1-603', '租户名': '企业C', '异常类型': '违约', '严重程度': '高', '状态': '未解决'}
    ]
    
    # 2. 统计分析
    total_count = len(exceptions)
    resolved_count = len([e for e in exceptions if e['状态'] == '已解决'])
    in_progress_count = len([e for e in exceptions if e['状态'] == '处理中'])
    unresolved_count = len([e for e in exceptions if e['状态'] == '未解决'])
    
    resolution_rate = (resolved_count / total_count * 100) if total_count > 0 else 0
    
    # 3. 生成报告
    report_content = f"""
# 履约异常处理报告

**报告周期**：{start_date.strftime('%Y-%m-%d')} 至 {end_date.strftime('%Y-%m-%d')}
**生成时间**：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**编制单位**：示例集团产城园区运营有限公司

---

## 一、履约异常处理概况

| 指标 | 数值 |
|------|------|
| 履约异常总数 | {total_count} |
| 已解决 | {resolved_count} |
| 处理中 | {in_progress_count} |
| 未解决 | {unresolved_count} |
| 解决率 | {resolution_rate:.1f}% |

---

## 二、履约异常明细

| 单元号 | 租户名 | 异常类型 | 严重程度 | 状态 |
|--------|--------|----------|----------|------|
"""
    
    for exception in exceptions:
        report_content += f"| {exception['单元号']} | {exception['租户名']} | {exception['异常类型']} | {exception['严重程度']} | {exception['状态']} |\n"
    
    report_content += f"""
---

## 三、分析与建议

### 3.1 履约异常类型分析

从履约异常类型来看，欠费异常占比最高，说明[分析...]。

### 3.2 履约异常处理效率分析

本期履约异常解决率为{resolution_rate:.1f}%，较上期[上升/下降] [X]个百分点，说明[分析...]。

### 3.3 改进建议

1. **加强事前预防**：[建议...]
2. **优化处理流程**：[建议...]
3. **引入法律手段**：[建议...]

---

**编制**：企服助手 (Enterprise Service Assistant)
**版本**：V1.0
"""
    
    # 保存为Markdown文件
    output_dir = "/Users/mac/履约异常处理报告/"
    os.makedirs(output_dir, exist_ok=True)
    
    file_path = f"{output_dir}履约异常处理报告_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.md"
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    return file_path
```

---

## 执行流程

```
Step 1 → 识别履约异常
         读取Excel费用收缴表
         筛选逾期超过30天的欠费记录
         识别其他异常情况（违约、退租等）

Step 2 → 分级处理
         根据异常类型和严重程度触发相应处理流程
         低严重程度：提醒 + 电话跟进
         中严重程度：正式催缴 + 上门沟通
         高严重程度：律师函 + 法律程序

Step 3 → 触发法律程序
         欠费逾期超60天 → 自动触发律师函
         欠费逾期超90天 → 自动触发诉讼

Step 4 → 记录处理过程
         记录异常处理全过程
         生成《履约异常处理记录》

Step 5 → 生成报告
         定期生成《履约异常处理报告》
         分析处理效率，提出改进建议
```

---

## 定时任务配置

```json
{
  "name": "履约异常检查",
  "schedule": {
    "kind": "cron",
    "expr": "0 10 * * *",
    "tz": "Asia/Shanghai"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "检查履约异常情况（欠费、违约、退租等），识别异常，触发分级处理流程，记录处理过程"
  },
  "sessionTarget": "isolated"
}
```

**说明**：每天10:00自动检查履约异常情况。

---

## 手动触发方式

1. **企微 @提及**: `@企服助手 履约异常`
2. **OpenClaw指令**: `检查履约异常` / `触发法律程序 [单元号]`
   - 示例：`触发法律程序 T1-601`

---

## 配置参数

```json
{
  "performance_exception": {
    "excel_path": "/Users/mac/示例产业园AC+服务.xlsx",
    "days_threshold": 30,  // 逾期天数阈值
    "legal_proceedings_threshold": {
      "lawyer_letter": 60,  // 逾期60天触发律师函
      "lawsuit": 90  // 逾期90天触发诉讼
    },
    "wecom_webhook": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx",
    "lawyer_letter_template": "/Users/mac/模板/律师函模板.docx",
    "indictment_template": "/Users/mac/模板/起诉书模板.docx"
  }
}
```

---

## 使用示例

**用户输入**: `@企服助手 履约异常`

**输出**:
```
━━━━━━━━━━━━━━━
【履约异常检查报告】2026-06-02

━━━ 履约异常清单 ━━━
共发现 3 项履约异常：

1. 【欠费】T1-601，上海XX有限公司
   • 逾期天数：45天
   • 欠费金额：¥15,000.00
   • 严重程度：中
   • 处理状态：正式催缴通知已发送

2. 【欠费】T1-602，深圳XX有限公司
   • 逾期天数：75天
   • 欠费金额：¥32,000.00
   • 严重程度：高
   • 处理状态：律师函已发送

3. 【欠费】T1-603，广州XX有限公司
   • 逾期天数：105天
   • 欠费金额：¥58,000.00
   • 严重程度：高
   • 处理状态：诉讼已启动（案号：（2026）粤XX民初XX号）

━━━ 统计 ━━━
履约异常总数：3 项
已解决：0 项
处理中：2 项
未解决：1 项

⚡ 详细记录已保存至：/Users/mac/履约异常处理记录/
━━━━━━━━━━━━━━━
```

---

## 后续扩展接口

1. **对接集客荟系统 API** - 实时获取合同信息、客户档案
2. **对接法务系统 API** - 自动生成法律文书、在线立案
3. **对接法院电子诉讼平台 API** - 实现在线立案、在线缴费、在线阅卷
4. **对接失信被执行人查询接口** - 自动查询租户是否被列入失信被执行人名单
5. **引入AI法律文书生成** - 基于案情自动生成高质量法律文书

---

## 注意事项

1. **法律程序严谨性** - 法律文书必须严谨、规范，建议在发出前由法务人员审核
2. **时效性** - 法律程序有严格的时效限制，必须在时效内启动
3. **证据保全** - 注意保全证据，避免证据灭失
4. **沟通技巧** - 履约异常处理过程中，要注意沟通技巧，避免激化矛盾

---

**当前状态**: 技能已创建，核心逻辑已定义，已自包含（无需 customer-management 依赖），待与实际系统集成。

**核心功能**: 履约异常识别、分级处理、法律程序触发、处理过程记录。

**依赖说明**: 本技能已内联客户管理逻辑，无需安装 customer-management 技能。

**未来扩展**: 对接各系统API，实现全流程自动化。
