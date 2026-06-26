---
name: contract-renewal
description: 合同续租预警与方案生成技能。基于真实Excel台账（美兰中心C+服务.xlsx）提前识别到期合同，分析企业画像，生成续租方案。触发场景：(1) 定时任务每日09:00检查合同到期日期，(2) 提前3个月标记"续租预警"，(3) 手动触发续租检查（@企服助手 续租检查）。
---

> **📌 本技能已自包含，无需安装 customer-management**
>
> 所有客户管理逻辑（查询客户档案、构建客户画像、计算风险标记）已内联到本文件中，不依赖外部技能。

# 合同续租预警与方案生成技能 (Contract Renewal Skill)

## 功能概述

本技能用于自动化合同续租管理，基于中集金地美兰中心真实Excel台账，提前识别到期合同，分析企业画像，生成个性化续租方案，并推送给招商人员和管家进行审批。

---

## 数据源配置

**数据文件**: `/Users/mac/美兰中心C+服务.xlsx`

**工作表映射**:
| 功能模块 | 工作表名 | 用途 |
|---------|---------|------|
| **客户档案** | 👨客户管理👨 | 主数据源（截至日期、企业类型、等级） |
| **费用收缴** | 👨💼费用收缴👨💼 | 补充数据（历史缴费记录） |
| **C+服务记录** | C+服务记录 | 补充数据（历史服务记录） |
| **客户画像** | customer-management技能 | 聚合分析企业画像 |

---

## 客户管理逻辑（内联）

> 以下逻辑已从 customer-management 技能内联，无需外部依赖。

### 数据结构与辅助函数

```python
import openpyxl
from datetime import datetime

def parse_excel_date(date_value):
    """
    解析Excel日期（支持多种格式）
    """
    if isinstance(date_value, datetime):
        return date_value.date()
    if isinstance(date_value, str):
        # 尝试解析 "2025年3月1日" 格式
        try:
            return datetime.strptime(date_value, "%Y年%m月%d日").date()
        except:
            pass
        # 尝试解析 "2025-03-01" 格式
        try:
            return datetime.strptime(date_value, "%Y-%m-%d").date()
        except:
            pass
    return None

def build_customer_dict(headers, row):
    """
    将Excel行数据构建为字典
    """
    return dict(zip(headers, row))
```

### 1. query_customer_profile（查询客户档案）

```python
def query_customer_profile(unit_no=None, tenant_name=None, contract_no=None):
    """
    查询客户档案
    
    Args:
        unit_no: 单元号（如 T1-601）
        tenant_name: 租户名（支持模糊匹配）
        contract_no: 合同号
    
    Returns:
        dict: 客户完整档案信息
    """
    wb = openpyxl.load_workbook('/Users/mac/美兰中心C+服务.xlsx')
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
```

### 2. build_customer_portrait（构建客户画像）

```python
def build_customer_portrait(unit_no):
    """
    构建客户画像 - 聚合多个数据源
    
    Args:
        unit_no: 单元号（主键）
    
    Returns:
        dict: 客户画像（包含服务、费用、报修等汇总）
    """
    wb = openpyxl.load_workbook('/Users/mac/美兰中心C+服务.xlsx')
    
    portrait = {
        "基础信息": query_customer_profile(unit_no),
        "服务记录": [],
        "费用记录": [],
        "能耗记录": [],
        "报修记录": [],
        "风险标记": []
    }
    
    # 1. 查询C+服务记录（关联字段：租户名）
    ws_service = wb['C+服务记录']
    tenant_name = portrait["基础信息"]["租户名"] if portrait["基础信息"] else ""
    
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
```

### 3. calculate_risk_tags（计算风险标记）

```python
def calculate_risk_tags(portrait):
    """
    计算客户风险标记
    
    Returns:
        list: 风险标记列表（如 ["欠费风险", "流失风险"]）
    """
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
        截至日期 = parse_excel_date(基础信息.get("截至日期"))
        if 截至日期:
            剩余天数 = (截至日期 - datetime.now().date()).days
            
            if 剩余天数 <= 30:
                risks.append(f"🚨 流失风险（合同剩余{剩余天数}天）")
            elif 剩余天数 <= 90:
                risks.append(f"⚠️ 续租预警（合同剩余{剩余天数}天）")
    
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

---

## 核心逻辑

### 1. 续租预警扫描

```python
def scan_renewal_alerts():
    """
    扫描即将到期的合同，生成续租预警
    
    Returns:
        dict: 分类预警清单
    """
    wb = openpyxl.load_workbook('/Users/mac/美兰中心C+服务.xlsx')
    ws_customer = wb['👨客户管理👨']
    
    today = datetime.now().date()
    
    alerts = {
        "红色预警": [],  # ≤30天
        "黄色预警": [],  # 31-60天
        "绿色提醒": []   # 61-90天
    }
    
    # 遍历客户管理表
    for row in ws_customer.iter_rows(min_row=2, values_only=True):
        status = row[12]  # 状态
        
        if status == "签约":
            unit_no = row[5]      # 单元号
            tenant_name = row[6]  # 租户名
            lease_end_str = row[11]  # 截至日期
            
            # 解析截至日期
            lease_end = parse_excel_date(lease_end_str)
            
            # 计算剩余天数
            days_remaining = (lease_end - today).days
            
            if days_remaining <= 90 and days_remaining > 0:
                # 直接调用内联函数获取企业画像
                customer_portrait = build_customer_portrait(unit_no)
                
                alert = {
                    "单元号": unit_no,
                    "租户名": tenant_name,
                    "截至日期": lease_end,
                    "剩余天数": days_remaining,
                    "企业画像": customer_portrait
                }
                
                # 分级归档
                if days_remaining <= 30:
                    alerts["红色预警"].append(alert)
                elif days_remaining <= 60:
                    alerts["黄色预警"].append(alert)
                else:
                    alerts["绿色提醒"].append(alert)
    
    return alerts
```

### 2. 企业画像分析（基于客户画像数据）

```python
def analyze_enterprise_for_renewal(unit_no):
    """
    分析企业画像，为续租方案提供依据
    
    Args:
        unit_no: 单元号
    
    Returns:
        dict: 企业画像分析结果
    """
    # 直接调用内联函数获取客户画像
    portrait = build_customer_portrait(unit_no)
    
    # 1. 计算缴费准时率
    费用记录 = portrait["费用记录"]
    已支付数 = len([f for f in 费用记录 if f["是否支付"] == "是"])
    总费用数 = len(费用记录)
    缴费准时率 = 已支付数 / 总费用数 if 总费用数 > 0 else 0
    
    # 2. 计算服务满意度
    服务记录 = portrait["服务记录"]
    满意数 = len([s for s in 服务记录 if s["客户情绪"] == "满意"])
    总服务数 = len(服务记录)
    满意度 = 满意数 / 总服务数 if 总服务数 > 0 else 0
    
    # 3. 计算服务成交率
    成交数 = len([s for s in 服务记录 if s["成交情况"] == "是"])
    成交率 = 成交数 / 总服务数 if 总服务数 > 0 else 0
    
    # 4. 风险标记
    风险标记 = portrait["风险标记"]
    
    return {
        "缴费准时率": 缴费准时率,
        "满意度": 满意度,
        "成交率": 成交率,
        "风险标记": 风险标记,
        "等级": portrait["基础信息"]["等级"],
        "企业类型": portrait["基础信息"]["企业类型"]
    }
```

### 3. 续租方案生成算法

```python
def generate_renewal_plan(unit_no):
    """
    根据企业画像生成续租方案
    
    Args:
        unit_no: 单元号
    
    Returns:
        dict: 续租方案
    """
    # 获取企业画像分析
    analysis = analyze_enterprise_for_renewal(unit_no)
    
    # 直接调用内联函数获取客户档案
    portrait = query_customer_profile(unit_no)
    
    # 根据画像选择方案模板
    if analysis["缴费准时率"] >= 0.95 and analysis["满意度"] >= 0.8:
        # 优质企业 → 原条件续租
        plan_type = "A"
        proposed_rent = portrait["首年合同单价"]  # 维持原价
        discount_rate = 1.0
        incentive_policy = "无"
    elif analysis["成交率"] >= 0.3 or analysis["等级"] == "A":
        # 潜力企业 → 优惠续租
        plan_type = "B"
        proposed_rent = portrait["首年合同单价"] * 1.05  # 小幅上涨
        discount_rate = 0.95  # 95折
        incentive_policy = "首月租金减免10%"
    else:
        # 一般企业 → 市场化续租
        plan_type = "C"
        proposed_rent = get_market_rent(unit_no)  # 市场价
        discount_rate = 1.0
        incentive_policy = "无"
    
    return {
        "方案类型": plan_type,
        "建议租金": proposed_rent,
        "优惠折扣": discount_rate,
        "优惠政策": incentive_policy,
        "企业画像": analysis
    }
```

---

## 续租预警推送模板

### 红色预警（≤30天）

```
━━━━━━━━━━━━━━━
【续租红色预警】

🏢 企业：{tenant_name}
📍 单元：{unit_no}
📅 合同到期：{lease_end}
⏰ 剩余天数：{days_remaining}天

━━━ 企业画像 ━━━
等级：{level}
企业类型：{enterprise_type}
缴费准时率：{payment_rate*100:.1f}%
服务满意度：{satisfaction*100:.1f}%

━━━ 风险标记 ━━━
{risks}

━━━ 续租方案 ━━━
方案类型：{plan_type}
建议租金：¥{proposed_rent}/㎡/月
优惠折扣：{discount_rate*100:.0f}折
优惠政策：{incentive_policy}

🚨 请 @招商人员 @管家 立即跟进！

⚡ 操作链接：[腾讯文档-客户管理]
━━━━━━━━━━━━━━━
```

---

## 执行流程

```
Step 1 → 读取Excel客户管理表
         工作表：👨客户管理👨
         筛选：状态 = '签约'

Step 2 → 计算合同剩余天数
         剩余天数 = 截至日期 - 今日日期

Step 3 → 调用内联函数获取企业画像
         直接调用 build_customer_portrait()
         获取企业画像（费用记录、服务记录、风险标记）

Step 4 → 分级预警
         ├─ ≤30天   → 红色预警（紧急）
         ├─ 31-60天 → 黄色预警（高）
         └─ 61-90天 → 绿色提醒（中）

Step 5 → 生成续租方案
         根据企业画像（缴费准时率、满意度、成交率）生成方案

Step 6 → 推送企微
         发送给招商人员和管家审批
```

---

## 定时任务配置

```json
{
  "name": "合同续租预警",
  "schedule": {
    "kind": "cron",
    "expr": "0 9 * * *",
    "tz": "Asia/Shanghai"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "检查合同到期日期，提前3个月标记续租预警，提前2个月生成续租方案"
  },
  "sessionTarget": "isolated"
}
```

---

## 手动触发方式

1. **企微 @提及**: `@企服助手 续租检查`
2. **OpenClaw指令**: `检查续租` / `生成续租方案 {单元号}`

---

## 配置参数

```json
{
  "contract_renewal": {
    "excel_path": "/Users/mac/美兰中心C+服务.xlsx",
    "alert_days_before": 90,
    "plan_generation_days_before": 60,
    "auto_generate_plan": true,
    "wecom_webhook": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx"
  }
}
```

---

## 使用示例

**用户输入**: `@企服助手 续租检查`

**输出**:
```
━━━━━━━━━━━━━━━
【续租预警日报】2026-05-28

━━━ 🚨 红色预警（≤30天）━━━
  • T1-XXX，XXX公司，剩余XX天

━━━ ⚠️ 黄色预警（31-60天）━━━
  • T1-601，上海铭尤力食品有限公司，剩余XX天

━━━ ✅ 绿色提醒（61-90天）━━━
  • T1-XXX，XXX公司，剩余XX天

━━━ 统计 ━━━
预警企业总数：XX个
红色预警：XX个 | 黄色预警：XX个 | 绿色提醒：XX个

⚡ 操作链接：[腾讯文档-客户管理]
━━━━━━━━━━━━━━━
```

---

## 核心逻辑（升级版）

### 4. 客户价值评估算法

```python
def evaluate_customer_value(unit_no):
    """
    综合评估客户价值（基于租金、面积、企业规模、资质等维度）
    
    Args:
        unit_no: 单元号
    
    Returns:
        dict: 客户价值评估结果 {'总分': 85, '等级': 'A', '明细': {...}}
    """
    # 直接调用内联函数获取客户档案
    customer_profile = query_customer_profile(unit_no)
    
    if not customer_profile:
        return {'总分': 0, '等级': 'C', '明细': {}}
    
    # 直接调用内联函数获取客户画像
    portrait = build_customer_portrait(unit_no)
    
    score = 0
    details = {}
    
    # 1. 租金贡献（权重30%）
    monthly_rent = float(customer_profile.get("首年合同单价", 0) or 0)
    lease_area = float(customer_profile.get("租赁面积", 0) or 0)
    annual_rent = monthly_rent * lease_area * 12
    
    rent_score = 0
    if annual_rent >= 500000:  # 50万以上
        rent_score = 30
    elif annual_rent >= 200000:  # 20-50万
        rent_score = 20
    elif annual_rent >= 100000:  # 10-20万
        rent_score = 15
    else:
        rent_score = 10
    
    score += rent_score
    details['租金贡献'] = {'得分': rent_score, '满分': 30, '年租金': annual_rent}
    
    # 2. 企业资质（权重25%）
    enterprise_type = customer_profile.get("企业类型", "")
    qualification_score = 0
    if "高新" in enterprise_type or "上市" in enterprise_type:
        qualification_score = 25
    elif "科技" in enterprise_type or "研发" in enterprise_type:
        qualification_score = 20
    elif "贸易" in enterprise_type or "服务" in enterprise_type:
        qualification_score = 15
    else:
        qualification_score = 10
    
    score += qualification_score
    details['企业资质'] = {'得分': qualification_score, '满分': 25, '类型': enterprise_type}
    
    # 3. 缴费准时率（权重20%）
    费用记录 = portrait.get("费用记录", [])
    已支付数 = len([f for f in 费用记录 if f.get("是否支付") == "是"])
    总费用数 = len(费用记录)
    缴费准时率 = 已支付数 / 总费用数 if 总费用数 > 0 else 0
    
    payment_score = 0
    if 缴费准时率 >= 0.95:
        payment_score = 20
    elif 缴费准时率 >= 0.9:
        payment_score = 15
    elif 缴费准时率 >= 0.8:
        payment_score = 10
    else:
        payment_score = 5
    
    score += payment_score
    details['缴费准时率'] = {'得分': payment_score, '满分': 20, '准时率': 缴费准时率}
    
    # 4. 服务满意度（权重15%）
    服务记录 = portrait.get("服务记录", [])
    满意数 = len([s for s in 服务记录 if s.get("客户情绪") == "满意"])
    总服务数 = len(服务记录)
    满意度 = 满意数 / 总服务数 if 总服务数 > 0 else 0
    
    satisfaction_score = 0
    if 满意度 >= 0.8:
        satisfaction_score = 15
    elif 满意度 >= 0.6:
        satisfaction_score = 10
    elif 满意度 >= 0.4:
        satisfaction_score = 5
    else:
        satisfaction_score = 0
    
    score += satisfaction_score
    details['服务满意度'] = {'得分': satisfaction_score, '满分': 15, '满意度': 满意度}
    
    # 5. 成交贡献（权重10%）
    成交数 = len([s for s in 服务记录 if s.get("成交情况") == "是"])
    成交率 = 成交数 / 总服务数 if 总服务数 > 0 else 0
    
    deal_score = 0
    if 成交率 >= 0.3:
        deal_score = 10
    elif 成交率 >= 0.2:
        deal_score = 7
    elif 成交率 >= 0.1:
        deal_score = 5
    else:
        deal_score = 0
    
    score += deal_score
    details['成交贡献'] = {'得分': deal_score, '满分': 10, '成交率': 成交率}
    
    # 确定价值等级
    value_level = 'C'
    if score >= 80:
        value_level = 'A'
    elif score >= 60:
        value_level = 'B'
    
    return {
        '总分': min(score, 100),
        '等级': value_level,
        '明细': details
    }
```

### 5. 稳租方案自动生成算法（基于标准）

```python
def generate_stable_rental_plan(unit_no):
    """
    基于标准中的"差异化稳租策略"自动生成稳租方案
    
    Args:
        unit_no: 单元号
    
    Returns:
        dict: 稳租方案
    """
    # 1. 评估客户价值
    value_assessment = evaluate_customer_value(unit_no)
    value_level = value_assessment['等级']
    value_score = value_assessment['总分']
    
    # 直接调用内联函数获取客户档案
    customer_profile = query_customer_profile(unit_no)
    
    tenant_name = customer_profile.get("租户名", "")
    current_rent = float(customer_profile.get("首年合同单价", 0) or 0)
    lease_area = float(customer_profile.get("租赁面积", 0) or 0)
    
    # 3. 根据价值等级生成差异化稳租策略
    plan = {
        '客户名称': tenant_name,
        '单元号': unit_no,
        '价值等级': value_level,
        '价值评分': value_score,
        '策略组合': [],
        '建议租金': current_rent,
        '优惠方案': '无',
        '预计成本': 0
    }
    
    # A级客户（价值评分≥80）→ 全方位稳租策略
    if value_level == 'A':
        # 策略1：提高服务标准
        plan['策略组合'].append('提高服务标准：增加走访频率（月度→双周），专属管家服务')
        plan['预计成本'] += 5000
        
        # 策略2：关怀活动
        plan['策略组合'].append('关怀活动：生日礼物、节日慰问、企业周年庆贺')
        plan['预计成本'] += 3000
        
        # 策略3：服务赠送
        plan['策略组合'].append('服务赠送：免费会议室使用（8小时/月）、免费停车券（2张/月）')
        plan['预计成本'] += 2000
        
        # 策略4：合同条件调整
        plan['建议租金'] = current_rent * 1.03  # 小幅上涨3%
        plan['优惠方案'] = '续租3年享95折，免租期延长15天'
        plan['策略组合'].append('合同条件调整：小幅上涨+长期优惠')
    
    # B级客户（价值评分60-79）→ 中度稳租策略
    elif value_level == 'B':
        # 策略1：提高服务标准（适度）
        plan['策略组合'].append('提高服务标准：增加走访频率（季度→月度）')
        plan['预计成本'] += 2000
        
        # 策略2：关怀活动（适度）
        plan['策略组合'].append('关怀活动：节日慰问')
        plan['预计成本'] += 1000
        
        # 策略3：服务赠送（适度）
        plan['策略组合'].append('服务赠送：免费会议室使用（4小时/月）')
        plan['预计成本'] += 1000
        
        # 策略4：合同条件调整
        plan['建议租金'] = current_rent * 1.05  # 中等上涨5%
        plan['优惠方案'] = '续租2年享98折' 
        plan['策略组合'].append('合同条件调整：中等上涨+适度优惠')
    
    # C级客户（价值评分<60）→ 基础稳租策略
    else:
        # 策略1：基础服务标准
        plan['策略组合'].append('基础服务标准：保持当前走访频率')
        
        # 策略2：市场化租金
        plan['建议租金'] = get_market_rent(unit_no)  # 市场价
        plan['优惠方案'] = '无'
        plan['策略组合'].append('合同条件调整：市场化定价')
    
    # 4. 计算稳租成本收益率
    年租金收入 = plan['建议租金'] * lease_area * 12
    稳租成本收益率 = (年租金收入 - plan['预计成本']) / plan['预计成本'] if plan['预计成本'] > 0 else 0
    
    plan['年租金收入'] = 年租金收入
    plan['稳租成本收益率'] = round(稳租成本收益率, 2)
    
    return plan

@staticmethod
def get_market_rent(unit_no):
    """
    获取周边市场租金（模拟函数，实际需要对接市场数据）
    """
    # TODO: 对接市场数据API
    # 暂时返回固定值
    return 120  # 元/㎡/月
```

### 6. 续租方案生成算法（升级版）

```python
def generate_renewal_plan(unit_no):
    """
    根据企业画像和稳租方案生成续租方案（升级版）
    
    Returns:
        dict: 续租方案（含稳租策略）
    """
    # 1. 获取企业画像分析
    analysis = analyze_enterprise_for_renewal(unit_no)
    
    # 2. 生成稳租方案
    stable_rental_plan = generate_stable_rental_plan(unit_no)
    
    # 直接调用内联函数获取客户档案
    portrait = query_customer_profile(unit_no)
    
    # 4. 根据画像和稳租方案确定最终方案
    缴费准时率 = analysis['缴费准时率']
    满意度 = analysis['满意度']
    成交率 = analysis['成交率']
    价值等级 = stable_rental_plan['价值等级']
    
    # 方案决策矩阵
    if 价值等级 == 'A' or (缴费准时率 >= 0.95 and 满意度 >= 0.8):
        # 优质企业 → 原条件续租 + 稳租策略
        plan_type = "A"
        proposed_rent = stable_rental_plan['建议租金']
        discount_rate = 0.95 if 价值等级 == 'A' else 1.0
        incentive_policy = stable_rental_plan['优惠方案']
        retention_strategy = stable_rental_plan['策略组合']
    
    elif 价值等级 == 'B' or 成交率 >= 0.3 or 缴费准时率 >= 0.9:
        # 潜力企业 → 优惠续租 + 中度稳租策略
        plan_type = "B"
        proposed_rent = stable_rental_plan['建议租金']
        discount_rate = 0.98
        incentive_policy = stable_rental_plan['优惠方案']
        retention_strategy = stable_rental_plan['策略组合']
    
    else:
        # 一般企业 → 市场化续租 + 基础稳租策略
        plan_type = "C"
        proposed_rent = get_market_rent(unit_no)
        discount_rate = 1.0
        incentive_policy = "无"
        retention_strategy = stable_rental_plan['策略组合']
    
    return {
        "方案类型": plan_type,
        "建议租金": proposed_rent,
        "优惠折扣": discount_rate,
        "优惠政策": incentive_policy,
        "稳租策略": retention_strategy,
        "稳租成本收益率": stable_rental_plan['稳租成本收益率'],
        "客户价值评估": {
            "等级": 价值等级,
            "总分": stable_rental_plan['价值评分']
        },
        "企业画像": analysis
    }
```

---

## 后续扩展接口

1. **谈判话术生成** - 基于企业画像和稳租方案生成个性化谈判策略
2. **竞争对手分析** - 接入周边园区租金数据
3. **续租成功率预测** - 基于历史数据训练预测模型
4. **稳租成本预算管控** - 跟踪稳租成本实际使用情况进行预算管控

---

**当前状态**: ✅ 技能已完成自包含改造，所有客户管理逻辑已内联，无需安装 customer-management 技能。

**核心改进**: 
- ✅ `query_customer_profile()` - 查询客户档案（内联）
- ✅ `build_customer_portrait()` - 构建客户画像（内联）
- ✅ `calculate_risk_tags()` - 计算风险标记（内联）
- ✅ 删除所有 `call_skill("customer-management", ...)` 引用

**数据源**: `/Users/mac/美兰中心C+服务.xlsx`（真实业务数据）

**核心价值**: 合同续租预警与方案生成，基于客户画像的差异化稳租策略。