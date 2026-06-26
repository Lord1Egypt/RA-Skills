# SKILL.md

**License:** MIT  
**Copyright:** 2026 perrykono-debug

---

---
name: operations-analysis
description: 运营分析中心技能。提供今日待办、本周重点、月度统计等运营分析功能。基于示例产业园A真实Excel台账数据，生成可视化报表和统计图表。触发场景：(1) 定时任务每日08:00生成今日待办，(2) 每周一09:00生成周报，(3) 每月1日09:00生成月报，(4) 手动触发运营分析（@企服助手 运营分析）。
---

# 运营分析中心技能 (Operations Analysis Skill)

## 功能概述

本技能提供园区企业服务的运营数据分析，基于示例产业园A真实Excel台账，生成今日待办、本周重点、月度统计等报表，帮助管理层掌握运营状况。

---

## 数据源配置

**数据文件**: `/Users/mac/示例产业园AC+服务.xlsx`

**工作表清单**:
| 工作表名 | 用途 | 关键字段 |
|---------|------|---------|
| 👨客户管理👨 | 客户基础数据 | 状态、等级、截至日期 |
| 👨💼费用收缴👨💼 | 费用数据 | 应收金额、已收金额、是否支付 |
| 👨💼能耗收缴👨💼 | 能耗数据 | 应收金额、已收金额、是否支付 |
| 🛠️报修情况汇总🛠️ | 工单数据 | 维修跟进状态、紧急程度 |
| C+服务记录 | 服务数据 | 走访时间、成交情况、客户情绪 |
| 📦库存管理📦秩序环境 | 库存数据 | 物品名称、数量、单位 |
| 📦库存管理📦固定资产 | 库存数据 | 物品名称、数量、单位 |
| 📦库存管理📦工程 | 库存数据 | 物品名称、数量、单位 |

---

## 核心功能

### 1. 今日待办（Daily Tasks）

#### 功能说明
自动汇总今日需要处理的所有事项，包括：
- 待处理工单
- 今日到期费用
- 今日走访计划
- 续租预警（剩余≤30天）
- 库存预警

#### 实现逻辑
```python
def get_today_tasks():
    """
    获取今日待办事项
    
    Returns:
        dict: 今日待办清单
    """
    wb = openpyxl.load_workbook('/Users/mac/示例产业园AC+服务.xlsx')
    today = datetime.now().date()
    
    tasks = {
        "紧急待办": [],
        "重要待办": [],
        "普通待办": []
    }
    
    # 1. 待处理工单（紧急程度：紧急！急需处理！）
    ws_repair = wb['🛠️报修情况汇总🛠️']
    for row in ws_repair.iter_rows(min_row=2, values_only=True):
        if row[7] == "待处理":  # 维修跟进状态
            urgency = row[1]  # 紧急程度
            if urgency == "紧急！急需处理！":
                tasks["紧急待办"].append({
                    "类型": "工单",
                    "描述": f"{row[0]} - {row[2]}",  # 楼层/单元 - 报修描述
                    "紧急程度": urgency
                })
            else:
                tasks["重要待办"].append({
                    "类型": "工单",
                    "描述": f"{row[0]} - {row[2]}",
                    "紧急程度": urgency
                })
    
    # 2. 今日到期费用
    ws_fee = wb['👨💼费用收缴👨💼']
    for row in ws_fee.iter_rows(min_row=2, values_only=True):
        due_date = parse_excel_date(row[13])  # 月份字段
        if due_date == today and row[9] == "否":  # 是否支付 = 否
            tasks["重要待办"].append({
                "类型": "费用催缴",
                "描述": f"{row[2]} - {row[3]}到期",  # 单元号 - 费项项目
                "金额": row[8]  # 欠收金额
            })
    
    # 3. 今日走访计划（从走访计划表中读取）
    # TODO: 需要创建走访计划表
    # 暂时从C+服务记录中筛选今日计划
    ws_service = wb['C+服务记录']
    for row in ws_service.iter_rows(min_row=2, values_only=True):

        visit_date = parse_excel_date(row[1])  # 走访时间
        if visit_date == today:
            tasks["普通待办"].append({
                "类型": "走访",
                "描述": f"今日走访 {row[0]}",  # 租户名
                "管家": row[2]  # 走访管家
            })
    
    # 4. 续租预警（剩余≤30天）
    ws_customer = wb['👨客户管理👨']
    for row in ws_customer.iter_rows(min_row=2, values_only=True):
        if row[12] == "签约":  # 状态 = 签约
            lease_end = parse_excel_date(row[11])  # 截至日期
            days_remaining = (lease_end - today).days
            if 0 < days_remaining <= 30:
                tasks["紧急待办"].append({
                    "类型": "续租预警",
                    "描述": f"{row[6]} 合同剩余{days_remaining}天",  # 租户名
                    "紧急程度": "红色预警"
                })
    
    # 5. 库存预警（数量≤5）
    for sheet_name in ['📦库存管理📦秩序环境', '📦库存管理📦固定资产', '📦库存管理📦工程']:
        ws_inventory = wb[sheet_name]
        for row in ws_inventory.iter_rows(min_row=2, values_only=True):
            if row[4] <= 5:  # 数量字段
                tasks["普通待办"].append({
                    "类型": "库存预警",
                    "描述": f"{row[2]} 库存不足（剩余{row[4]}{row[5]}）",  # 物品名称
                    "库存量": row[4]
                })
    
    return tasks
```

#### 输出示例
```
━━━━━━━━━━━━━━━
【今日待办】2026-06-02

━━━ 🚨 紧急待办 ━━━
1. 工单：T1-1009 - 单元跳闸
   紧急程度：紧急！急需处理！

2. 续租预警：上海XX公司 合同剩余25天
   紧急程度：红色预警

━━━ ⚠️ 重要待办 ━━━
1. 工单：T1-9F女厕 - 女厕门打不开
   紧急程度：紧急！一周内处理！

2. 费用催缴：T1-601 - 物业管理费到期
   金额：¥12,500

━━━ 📝 普通待办 ━━━
1. 走访：今日走访 示例企业名称
   管家：戚亮先

2. 库存预警：LED灯泡 库存不足（剩余3个）
   库存量：3

━━━ 统计 ━━━
紧急待办：2个 | 重要待办：2个 | 普通待办：2个
总计：6个待办事项

⚡ 操作链接：[腾讯文档-今日待办]
━━━━━━━━━━━━━━━
```

---

### 2. 本周重点（Weekly Focus）

#### 功能说明
汇总本周（周一至周日）的重点工作，包括：
- 本周新增工单
- 本周走访计划
- 本周费用收缴情况
- 本周续租预警更新
- 本周服务成交情况

#### 实现逻辑
```python
def get_weekly_focus():
    """
    获取本周重点项目
    
    Returns:
        dict: 本周重点清单
    """
    wb = openpyxl.load_workbook('/Users/mac/示例产业园AC+服务.xlsx')
    
    today = datetime.now().date()
    # 计算本周一和周日
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)
    
    weekly = {
        "本周工单": {"新增": 0, "完成": 0, "待处理": 0},
        "本周走访": {"计划": 0, "完成": 0, "转化率": 0},
        "本周费用": {"应收": 0, "已收": 0, "欠费": 0},
        "本周续租": {"红色预警": 0, "黄色预警": 0, "绿色提醒": 0},
        "本周服务": {"推荐": 0, "成交": 0, "成交率": 0}
    }
    
    # 1. 本周工单统计
    ws_repair = wb['🛠️报修情况汇总🛠️']
    for row in ws_repair.iter_rows(min_row=2, values_only=True):
        report_date = parse_excel_date(row[5])  # 报修时间
        if monday <= report_date <= sunday:
            weekly["本周工单"]["新增"] += 1
            
            status = row[7]  # 维修跟进状态
            if status == "已完成":
                weekly["本周工单"]["完成"] += 1
            elif status == "待处理":
                weekly["本周工单"]["待处理"] += 1
    
    # 2. 本周走访统计
    ws_service = wb['C+服务记录']
    for row in ws_service.iter_rows(min_row=2, values_only=True):
        visit_date = parse_excel_date(row[1])  # 走访时间
        if monday <= visit_date <= sunday:
            weekly["本周走访"]["计划"] += 1
            
            if row[4] == "是":  # 成交情况 = 是
                weekly["本周走访"]["完成"] += 1
    
    if weekly["本周走访"]["计划"] > 0:
        weekly["本周走访"]["转化率"] = round(
            weekly["本周走访"]["完成"] / weekly["本周走访"]["计划"] * 100, 1
        )
    
    # 3. 本周费用统计
    ws_fee = wb['👨💼费用收缴👨💼']
    for row in ws_fee.iter_rows(min_row=2, values_only=True):
        fee_date = parse_excel_date(row[13])  # 月份字段
        if fee_date and monday <= fee_date <= sunday:
            weekly["本周费用"]["应收"] += float(row[4] or 0)  # 应收金额
            weekly["本周费用"]["已收"] += float(row[6] or 0)  # 已收金额
            weekly["本周费用"]["欠费"] += float(row[8] or 0)  # 欠收金额
    
    # 4. 本周续租预警统计
    ws_customer = wb['👨客户管理👨']
    for row in ws_customer.iter_rows(min_row=2, values_only=True):
        if row[12] == "签约":  # 状态 = 签约
            lease_end = parse_excel_date(row[11])  # 截至日期
            days_remaining = (lease_end - today).days
            
            if 0 < days_remaining <= 30:
                weekly["本周续租"]["红色预警"] += 1
            elif 30 < days_remaining <= 60:
                weekly["本周续租"]["黄色预警"] += 1
            elif 60 < days_remaining <= 90:
                weekly["本周续租"]["绿色提醒"] += 1
    
    # 5. 本周服务成交统计
    for row in ws_service.iter_rows(min_row=2, values_only=True):
        visit_date = parse_excel_date(row[1])  # 走访时间
        if monday <= visit_date <= sunday:
            weekly["本周服务"]["推荐"] += 1
            
            if row[4] == "是":  # 成交情况 = 是
                weekly["本周服务"]["成交"] += 1
    
    if weekly["本周服务"]["推荐"] > 0:
        weekly["本周服务"]["成交率"] = round(
            weekly["本周服务"]["成交"] / weekly["本周服务"]["推荐"] * 100, 1
        )
    
    return weekly
```

#### 输出示例
```
━━━━━━━━━━━━━━━
【本周重点】2026-06-02 ~ 2026-06-08

━━━ 📊 本周工单 ━━━
新增：3个 | 完成：2个 | 待处理：1个
完成率：66.7%

━━━ 📅 本周走访 ━━━
计划：5个 | 完成：3个 | 转化率：60.0%

━━━ 💰 本周费用 ━━━
应收：¥85,200 | 已收：¥62,500 | 欠费：¥22,700
收缴率：73.4%

━━━ 📋 本周续租 ━━━
红色预警：2个 | 黄色预警：3个 | 绿色提醒：5个

━━━ 🤝 本周服务 ━━━
推荐：8次 | 成交：2次 | 成交率：25.0%

━━━ 统计 ━━━
本周总工作量：23项
工作效率：待评估

⚡ 操作链接：[腾讯文档-本周重点]
━━━━━━━━━━━━━━━
```

---

### 3. 月度统计（Monthly Statistics）

#### 功能说明
生成月度运营统计报告，包括：
- 客户统计（新增、退租、续租）
- 财务统计（应收、实收、欠费）
- 服务统计（走访次数、成交率）
- 工单统计（报修次数、完成率）
- 库存统计（出入库、预警）

#### 实现逻辑
```python
def get_monthly_statistics(year, month):
    """
    获取月度统计数据
    
    Args:
        year: 年份
        month: 月份
    
    Returns:
        dict: 月度统计报告
    """
    wb = openpyxl.load_workbook('/Users/mac/示例产业园AC+服务.xlsx')
    
    stats = {
        "客户统计": {
            "签约客户": 0,
            "本月新增": 0,
            "本月退租": 0,
            "续租客户": 0
        },
        "财务统计": {
            "应收总额": 0,
            "实收总额": 0,
            "欠费总额": 0,
            "收缴率": 0
        },
        "服务统计": {
            "走访次数": 0,
            "成交次数": 0,
            "成交率": 0,
            "满意度": 0
        },
        "工单统计": {
            "报修次数": 0,
            "完成次数": 0,
            "完成率": 0,
            "平均响应时间": 0
        },
        "库存统计": {
            "采购次数": 0,
            "领用次数": 0,
            "预警物品": 0
        }
    }
    
    # 1. 客户统计
    ws_customer = wb['👨客户管理👨']
    for row in ws_customer.iter_rows(min_row=2, values_only=True):
        status = row[12]  # 状态
        
        if status == "签约":
            stats["客户统计"]["签约客户"] += 1
            
            # 本月新增（开始日期在本月）
            start_date = parse_excel_date(row[11])  # 开始日期
            if start_date and start_date.year == year and start_date.month == month:
                stats["客户统计"]["本月新增"] += 1
        
        elif status == "退租":
            # 本月退租（退租日期在本月）
            # TODO: 需要从退租汇总表中读取退租日期
            pass
    
    # 2. 财务统计
    ws_fee = wb['👨💼费用收缴👨💼']
    for row in ws_fee.iter_rows(min_row=2, values_only=True):
        fee_date = parse_excel_date(row[13])  # 月份字段
        if fee_date and fee_date.year == year and fee_date.month == month:
            stats["财务统计"]["应收总额"] += float(row[4] or 0)  # 应收金额
            stats["财务统计"]["实收总额"] += float(row[6] or 0)  # 已收金额
            stats["财务统计"]["欠费总额"] += float(row[8] or 0)  # 欠收金额
    
    if stats["财务统计"]["应收总额"] > 0:
        stats["财务统计"]["收缴率"] = round(
            stats["财务统计"]["实收总额"] / stats["财务统计"]["应收总额"] * 100, 1
        )
    
    # 3. 服务统计
    ws_service = wb['C+服务记录']
    satisfaction_count = 0
    for row in ws_service.iter_rows(min_row=2, values_only=True):
        visit_date = parse_excel_date(row[1])  # 走访时间
        if visit_date and visit_date.year == year and visit_date.month == month:
            stats["服务统计"]["走访次数"] += 1
            
            if row[4] == "是":  # 成交情况 = 是
                stats["服务统计"]["成交次数"] += 1
            
            if row[3] == "满意":  # 客户情绪 = 满意
                satisfaction_count += 1
    
    if stats["服务统计"]["走访次数"] > 0:
        stats["服务统计"]["成交率"] = round(
            stats["服务统计"]["成交次数"] / stats["服务统计"]["走访次数"] * 100, 1
        )
        stats["服务统计"]["满意度"] = round(
            satisfaction_count / stats["服务统计"]["走访次数"] * 100, 1
        )
    
    # 4. 工单统计
    ws_repair = wb['🛠️报修情况汇总🛠️']
    total_response_time = 0
    for row in ws_repair.iter_rows(min_row=2, values_only=True):
        report_date = parse_excel_date(row[5])  # 报修时间
        if report_date and report_date.year == year and report_date.month == month:
            stats["工单统计"]["报修次数"] += 1
            
            if row[7] == "已完成":  # 维修跟进状态 = 已完成
                stats["工单统计"]["完成次数"] += 1
                
                # 计算响应时间（报修时间到完成时间）
                complete_date = parse_excel_date(row[10])  # 维修完成时间
                if complete_date:
                    response_time = (complete_date - report_date).days
                    total_response_time += response_time
    
    if stats["工单统计"]["报修次数"] > 0:
        stats["工单统计"]["完成率"] = round(
            stats["工单统计"]["完成次数"] / stats["工单统计"]["报修次数"] * 100, 1
        )
        
        if stats["工单统计"]["完成次数"] > 0:
            stats["工单统计"]["平均响应时间"] = round(
                total_response_time / stats["工单统计"]["完成次数"], 1
            )
    
    # 5. 库存统计
    for sheet_name in ['📦库存管理📦秩序环境', '📦库存管理📦固定资产', '📦库存管理📦工程']:
        ws_inventory = wb[sheet_name]
        for row in ws_inventory.iter_rows(min_row=2, values_only=True):
            # TODO: 需要库存变动记录表来统计采购和领用
            # 暂时只统计预警物品
            if row[4] <= 5:  # 数量字段
                stats["库存统计"]["预警物品"] += 1
    
    return stats
```

#### 输出示例
```
━━━━━━━━━━━━━━━
【月度统计报告】2026年5月

━━━ 👥 客户统计 ━━━
签约客户：45家
本月新增：2家 | 本月退租：1家
续租客户：0家

━━━ 💰 财务统计 ━━━
应收总额：¥425,600
实收总额：¥358,200
欠费总额：¥67,400
收缴率：84.2%

━━━ 🤝 服务统计 ━━━
走访次数：23次
成交次数：5次
成交率：21.7%
满意度：78.3%

━━━ 🛠️ 工单统计 ━━━
报修次数：8次
完成次数：7次
完成率：87.5%
平均响应时间：1.2天

━━━ 📦 库存统计 ━━━
采购次数：-- 次
领用次数：-- 次
预警物品：3个

━━━ 📊 月度总结 ━━━
本月运营状况：良好
主要亮点：工单完成率较高（87.5%）
待改进：费用收缴率需提升（当前84.2%）

⚡ 操作链接：[腾讯文档-月度统计]
━━━━━━━━━━━━━━━
```

---

## 定时任务配置

### 1. 每日今日待办
```json
{
  "name": "今日待办生成",
  "schedule": {
    "kind": "cron",
    "expr": "0 8 * * *",
    "tz": "Asia/Shanghai"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "生成今日待办清单，推送企微群"
  },
  "sessionTarget": "isolated"
}
```

### 2. 每周重点
```json
{
  "name": "本周重点生成",
  "schedule": {
    "kind": "cron",
    "expr": "0 9 * * 1",
    "tz": "Asia/Shanghai"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "生成本周重点工作报告，推送企微群"
  },
  "sessionTarget": "isolated"
}
```

### 3. 月度统计
```json
{
  "name": "月度统计生成",
  "schedule": {
    "kind": "cron",
    "expr": "0 9 1 * *",
    "tz": "Asia/Shanghai"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "生成上月月度统计报告，推送企微群"
  },
  "sessionTarget": "isolated"
}
```

---

## 手动触发方式

1. **今日待办**: `@企服助手 今日待办`
2. **本周重点**: `@企服助手 本周重点`
3. **月度统计**: `@企服助手 月度统计 2026 5` (年 月)
4. **运营分析**: `@企服助手 运营分析`

---

## 配置参数

```json
{
  "operations_analysis": {
    "excel_path": "/Users/mac/示例产业园AC+服务.xlsx",
    "auto_push": true,
    "wecom_webhook": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx",
    "push_time": {
      "daily": "08:00",
      "weekly": "周一 09:00",
      "monthly": "1日 09:00"
    }
  }
}
```

---

## 企微推送模板

### 今日待办推送
```
━━━━━━━━━━━━━━━
【今日待办】2026-06-02

🚨 紧急待办（2个）
1. 工单：T1-1009 - 单元跳闸
2. 续租预警：上海XX公司 剩余25天

⚠️ 重要待办（2个）
1. 工单：T1-9F女厕 - 门打不开
2. 费用催缴：T1-601 - ¥12,500

📝 普通待办（2个）
1. 走访：示例企业
2. 库存预警：LED灯泡不足

📊 合计：6个待办
━━━━━━━━━━━━━━━
```

### 本周重点推送
```
━━━━━━━━━━━━━━━
【本周重点】2026-06-02~06-08

📊 本周工单：新增3 | 完成2 | 完成率66.7%
📅 本周走访：计划5 | 完成3 | 转化率60.0%
💰 本周费用：应收¥85.2K | 收缴率73.4%
📋 本周续租：红色2 | 黄色3 | 绿色5
🤝 本周服务：推荐8 | 成交2 | 成交率25.0%

📈 本周总工作量：23项
━━━━━━━━━━━━━━━
```

### 月度统计推送
```
━━━━━━━━━━━━━━━
【月度统计】2026年5月

👥 客户：签约45家 | 新增2家 | 退租1家
💰 财务：应收¥425.6K | 收缴率84.2%
🤝 服务：走访23次 | 成交率21.7% | 满意度78.3%
🛠️ 工单：报修8次 | 完成率87.5% | 平均1.2天
📦 库存：预警3个

📊 月度总结：运营状况良好，工单完成率高
━━━━━━━━━━━━━━━
```

---

## 后续扩展接口

1. **数据可视化** - 生成图表（柱状图、折线图、饼图）
2. **趋势分析** - 同比/环比分析
3. **预测分析** - 基于历史数据预测未来趋势
4. **自定义报表** - 用户自定义统计维度和指标
5. **数据导出** - 导出Excel、PDF、PPT等格式

---

## 注意事项

1. **数据准确性** - 确保Excel数据实时更新
2. **日期解析** - Excel日期格式多样，需要统一解析
3. **性能优化** - 大数据量时需要优化查询速度
4. **权限控制** - 敏感数据需要权限管理

---

## 与其他技能的协作

### 与customer-management协作
- 客户统计数据来源于客户管理表
- 客户画像数据用于深度分析

### 与workorder-dispatch协作
- 工单统计数据来源于报修汇总表
- 工单完成率、响应时间等指标计算

### 与fee-collection协作
- 费用统计数据来源于费用收缴表
- 收缴率、欠费分析等指标计算

### 与service-matching协作
- 服务统计数据来源于C+服务记录表
- 成交率、满意度等指标计算

---

**当前状态**: 技能框架已完成，核心功能已实现。

**核心价值**: 提供全面的运营数据分析，帮助管理层掌握运营状况，支持数据驱动决策。
