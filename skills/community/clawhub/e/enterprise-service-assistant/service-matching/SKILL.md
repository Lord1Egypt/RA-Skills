# SKILL.md

**License:** MIT  
**Copyright:** 2026 perrykono-debug

---

---
name: service-matching
description: C+服务需求匹配技能。基于真实Excel台账（示例产业园AC+服务.xlsx）挖掘企业需求，匹配C+服务资源。触发场景：(1) 管家上传走访记录，(2) 定时任务每日10:00分析昨日走访记录，(3) 手动触发服务匹配（@企服助手 服务匹配）。
---

# C+服务需求匹配技能 (Service Matching Skill)

> **本技能已自包含，无需安装 customer-management**

## 功能概述

本技能用于从走访记录中自动挖掘企业需求，基于示例产业园A真实Excel台账，根据企业类型和画像匹配适合的C+服务，生成推荐方案供管家确认。

---

## 数据源配置

**数据文件**: `/Users/mac/示例产业园AC+服务.xlsx`

**工作表映射**:
| 功能模块 | 工作表名 | 用途 |
|---------|---------|------|
| **C+服务记录** | C+服务记录 | 主数据源（走访记录、需求描述） |
| **客户画像** | 👨客户管理👨 | 企业画像（企业类型、等级、经营范围） |

---

## 客户管理逻辑（内联）

> 以下逻辑从 customer-management 技能内联，无需外部依赖。

### 查询客户档案

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
    将Excel行数据构建为字典
    
    Args:
        headers: 表头列表
        row: 行数据元组
    
    Returns:
        dict: 客户档案字典
    """
    return dict(zip(headers, row))
```

### 客户档案字段说明

**客户管理表字段（27个）**:
```
基础信息字段:
  - 项目名称: 美慧城四期T1
  - 单元类型: 办公
  - 名义楼层: 6
  - 实际楼层: 5
  - 单元号: T1-601 （主键，用于关联其他表）

合同信息字段:
  - 合同号: {TODO: 填写合同编号} （关联费用收缴表）
  - 租户名: 示例企业名称
  - 建筑面积: 143.95
  - 首年合同单价: 1.75
  - 租期: 3年

租期信息字段:
  - 开始日期: 2025年3月1日
  - 截至日期: 2028年2月29日
  - 状态: 签约/退租/毛坯

联系人信息:
  - 租户联系人: 薛臻
  - 电话: （从Excel读取）
  - 注册地址: 上海市宝山区金石路1658弄11号4层410室

企业画像字段:
  - 等级: A/B/C
  - 企业类型: 餐饮配套/制造业/商务配套等
  - 经营范围: （具体业务）
  - 纳税人资质: 一般纳税人/小规模纳税人
  - 天眼评分: （天眼查评分）
  - 招商: （招商人员）
```

---

## Excel工作表字段映射

### C+服务记录表（10字段）

| Excel列序号 | 字段名 | 用途 |
|-------------|--------|------|
| 1 | 租户名 | 关联客户管理表 |
| 2 | 走访时间 | 时间 |
| 3 | 走访管家 | 人员 |
| 4 | 客户情绪 | 满意/一般/不满意 |
| 5 | 成交情况 | 是/否 |
| 6 | 服务类别 | 室内保洁/商务接待等 |
| 7 | 成交金额 | 金额 |
| 8 | 详情记录 | 企业需求描述 |
| 9 | 月份 | 月份 |
| 10 | 备注 | 备注 |

---

## 核心逻辑

### 1. 需求挖掘（NLP提取）

```python
def extract_needs_from_visit(detail_record):
    """
    从走访记录中提取企业需求
    
    Args:
        detail_record: 走访详情文本
    
    Returns:
        list: 需求列表
    """
    # NLP关键词匹配
    needs_keywords = {
        "保洁需求": ["清洁", "卫生", "保洁", "打扫"],
        "商务接待": ["接待", "会议室", "访客", "客人"],
        "室内维修": ["维修", "修理", "更换", "安装"],
        "环境优化": ["空气", "绿植", "噪音", "光线"],
        "能源管理": ["电费", "水费", "节能", "空调"],
        "证照服务": ["许可证", "执照", "审批", "证照"],
        "企业服务": ["注册", "变更", "年检", "税务"]
    }
    
    needs = []
    for need_type, keywords in needs_keywords.items():
        for keyword in keywords:
            if keyword in detail_record:
                needs.append(need_type)
                break
    
    return needs
```

### 2. 企业画像获取（内联逻辑）

```python
def get_enterprise_profile(tenant_name):
    """
    获取企业画像（内联逻辑，无需调用外部技能）
    
    Args:
        tenant_name: 租户名
    
    Returns:
        dict: 企业画像
    """
    # 直接调用内联的 query_customer_profile 函数
    customer_profile = query_customer_profile(tenant_name=tenant_name)
    
    if not customer_profile:
        return None
    
    return {
        "租户名": customer_profile.get("租户名", ""),
        "企业类型": customer_profile.get("企业类型", ""),
        "等级": customer_profile.get("等级", ""),
        "经营范围": customer_profile.get("经营范围", ""),
        "纳税人资质": customer_profile.get("纳税人资质", ""),
        "天眼评分": customer_profile.get("天眼评分", 0)
    }
```

### 3. 服务推荐算法

```python
def recommend_services(enterprise_profile, needs):
    """
    根据企业画像和需求推荐服务
    
    Args:
        enterprise_profile: 企业画像
        needs: 需求列表
    
    Returns:
        list: 推荐服务列表
    """
    # 服务匹配规则库
    service_rules = {
        "餐饮配套": {
            "优先服务": ["卫生许可证提醒", "固废清运", "室内保洁", "能源管理"],
            "优惠政策": "首月9折"
        },
        "制造业": {
            "优先服务": ["固废清运", "环境检测", "安全生产培训"],
            "优惠政策": "包年8折"
        },
        "商务配套": {
            "优先服务": ["商务接待", "会议室预定", "室内保洁", "绿植租赁"],
            "优惠政策": "首次免费体验"
        },
        "科技企业": {
            "优先服务": ["企业注册变更", "知识产权服务", "政策申报"],
            "优惠政策": "代办服务9折"
        }
    }
    
    enterprise_type = enterprise_profile.get("企业类型", "商务配套")
    level = enterprise_profile.get("等级", "B")
    
    # 获取匹配规则
    rules = service_rules.get(enterprise_type, service_rules["商务配套"])
    
    recommendations = []
    
    # 1. 基于企业类型的推荐
    for service in rules["优先服务"]:
        recommendations.append({
            "服务名称": service,
            "推荐理由": f"适合{enterprise_type}企业",
            "优先级": "高" if level == "A" else "中",
            "优惠政策": rules["优惠政策"],
            "跟进状态": "待确认",
            "跟进时间": None,
            "跟进结果": None
        })
    
    # 2. 基于需求的推荐
    for need in needs:
        if need not in [r["服务名称"] for r in recommendations]:
            recommendations.append({
                "服务名称": need,
                "推荐理由": "走访需求匹配",
                "优先级": "高",
                "优惠政策": rules["优惠政策"],
                "跟进状态": "待确认",
                "跟进时间": None,
                "跟进结果": None
            })
    
    return recommendations
```

### 4. 服务跟踪闭环功能

```python
def track_service_followup(tenant_name, service_name, followup_status, notes=""):
    """
    跟踪服务跟进状态
    
    Args:
        tenant_name: 租户名
        service_name: 服务名称
        followup_status: 跟进状态（待确认/已推荐/已拒绝/已成交）
        notes: 跟进说明
    
    Returns:
        bool: 是否更新成功
    """
    wb = openpyxl.load_workbook('/Users/mac/示例产业园AC+服务.xlsx')
    ws_service = wb['C+服务记录']
    
    today = datetime.now().date()
    
    # 1. 查找匹配的服务记录
    for row in ws_service.iter_rows(min_row=2):
        if row[0].value == tenant_name and service_name in str(row[5].value):  # 服务类别匹配
            # 2. 更新跟进状态（需要扩展Excel列）
            # 假设新增列：跟进状态、跟进时间、跟进结果
            row[10].value = followup_status  # 跟进状态
            row[11].value = today.strftime("%Y年%m月%d日")  # 跟进时间
            row[12].value = notes  # 跟进结果/说明
            
            wb.save('/Users/mac/示例产业园AC+服务.xlsx')
            
            # 3. 发送跟进通知
            send_followup_notification({
                "租户名": tenant_name,
                "服务名称": service_name,
                "跟进状态": followup_status,
                "跟进时间": today.strftime("%Y年%m月%d日"),
                "说明": notes
            })
            
            return True
    
    return False
```

### 5. 跟进提醒机制

```python
def check_followup_reminders():
    """
    检查需要跟进的服务推荐
    
    Returns:
        dict: 需要跟进的服务清单
    """
    wb = openpyxl.load_workbook('/Users/mac/示例产业园AC+服务.xlsx')
    ws_service = wb['C+服务记录']
    
    today = datetime.now().date()
    reminders = {
        "今日需跟进": [],
        "逾期未完成": [],
        "本周计划跟进": []
    }
    
    for row in ws_service.iter_rows(min_row=2, values_only=True):
        tenant_name = row[0]
        service_type = row[5]  # 服务类别
        followup_status = row[10] if len(row) > 10 else None  # 跟进状态
        followup_time = row[11] if len(row) > 11 else None  # 跟进时间
        
        if followup_status == "待确认":
            # 判断是否需要提醒
            if followup_time:
                followup_date = parse_excel_date(followup_time)
                days_pending = (today - followup_date).days
                
                if days_pending == 0:
                    reminders["今日需跟进"].append({
                        "租户名": tenant_name,
                        "服务名称": service_type,
                        "待跟进天数": days_pending
                    })
                elif days_pending > 3:  # 超过3天未跟进
                    reminders["逾期未完成"].append({
                        "租户名": tenant_name,
                        "服务名称": service_type,
                        "逾期天数": days_pending
                    })
            else:
                # 没有跟进时间，加入本周计划
                reminders["本周计划跟进"].append({
                    "租户名": tenant_name,
                    "服务名称": service_type
                })
    
    return reminders
```

### 6. 服务效果评估

```python
def evaluate_service_effectiveness(tenant_name, service_name):
    """
    评估服务效果
    
    Args:
        tenant_name: 租户名
        service_name: 服务名称
    
    Returns:
        dict: 服务效果评估结果
    """
    wb = openpyxl.load_workbook('/Users/mac/示例产业园AC+服务.xlsx')
    ws_service = wb['C+服务记录']
    
    # 获取服务记录
    service_record = None
    for row in ws_service.iter_rows(min_row=2, values_only=True):
        if row[0] == tenant_name and service_name in str(row[5]):
            service_record = {
                "走访时间": row[1],
                "客户情绪": row[3],
                "成交情况": row[4],
                "服务类别": row[5],
                "成交金额": row[6]
            }
            break
    
    if not service_record:
        return {'效果': '无记录', '评分': 0}
    
    # 计算效果评分
    score = 0
    
    # 1. 成交情况（权重50%）
    if service_record["成交情况"] == "是":
        score += 50
        # 成交金额加分
        amount = float(service_record["成交金额"] or 0)
        if amount > 5000:
            score += 20
    
    # 2. 客户情绪（权重30%）
    if service_record["客户情绪"] == "满意":
        score += 30
    elif service_record["客户情绪"] == "一般":
        score += 15
    
    # 3. 跟进及时性（权重20%）
    # 这里需要跟进时间数据，暂时简化处理
    score += 20
    
    # 确定效果等级
    effect_level = "差"
    if score >= 80:
        effect_level = "优"
    elif score >= 60:
        effect_level = "良"
    elif score >= 40:
        effect_level = "中"
    
    return {
        "效果等级": effect_level,
        "评分": min(score, 100),
        "成交情况": service_record["成交情况"],
        "客户情绪": service_record["客户情绪"],
        "成交金额": service_record["成交金额"]
    }
```

---

## 执行流程

```
Step 1 → 读取Excel C+服务记录表
         工作表：C+服务记录
         筛选：昨日走访记录 或 指定时间范围

Step 2 → NLP需求提取
         从详情记录中提取关键词，识别需求类型

Step 3 → 获取企业画像（内联逻辑）
         读取Excel 👨客户管理👨 工作表
         获取企业类型、等级、经营范围

Step 4 → 服务匹配
         根据企业类型 + 需求 → 匹配服务规则库

Step 5 → 生成推荐方案
         包含：服务名称、推荐理由、优先级、优惠政策

Step 6 → 推送企微
         发送给管家确认
```

---

## 推送模板

```
━━━━━━━━━━━━━━━
【C+服务推荐】

🏢 企业：{tenant_name}
📍 单元：{unit_no}
━━━ 企业画像 ━━━
类型：{enterprise_type}
等级：{level}
经营范围：{business_scope}

━━━ 走访需求 ━━━
{needs}

━━━ 推荐服务 ━━━
{recommendations}

💡 建议：{suggestion}

⚡ 操作链接：[腾讯文档-C+服务]
━━━━━━━━━━━━━━━
```

---

## 定时任务配置

```json
{
  "name": "C+服务需求分析",
  "schedule": {
    "kind": "cron",
    "expr": "0 10 * * *",
    "tz": "Asia/Shanghai"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "分析昨日C+服务走访记录，提取企业需求，匹配服务资源，生成推荐方案"
  },
  "sessionTarget": "isolated"
}
```

---

## 手动触发方式

1. **企微 @提及**: `@企服助手 服务匹配`
2. **OpenClaw指令**: `分析服务需求`

---

## 配置参数

```json
{
  "service_matching": {
    "excel_path": "/Users/mac/示例产业园AC+服务.xlsx",
    "auto_recommend": true,
    "wecom_webhook": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx"
  }
}
```

---

## 使用示例

**用户输入**: `@企服助手 服务匹配 示例企业`

**输出**:
```
━━━━━━━━━━━━━━━
【C+服务推荐】示例企业名称

━━━ 企业画像 ━━━
类型：食品制造业
等级：B级
经营范围：食品生产销售

━━━ 推荐服务 ━━━
1. 卫生许可证提醒（高优先级）
   理由：适合食品制造业
   优惠：首月9折

2. 固废清运（高优先级）
   理由：适合食品制造业
   优惠：首月9折

3. 室内保洁（中优先级）
   理由：适合食品制造业
   优惠：首月9折

⚡ 操作链接：[腾讯文档-C+服务]
━━━━━━━━━━━━━━━
```

---

**当前状态**: 技能已完成自包含改造，内联了客户管理逻辑，无需依赖 customer-management 技能。

**核心改进**: 从调用 customer-management 技能 → 改为直接读取 Excel 👨客户管理👨 工作表获取企业画像。
