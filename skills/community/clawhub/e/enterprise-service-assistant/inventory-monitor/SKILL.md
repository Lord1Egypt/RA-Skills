# SKILL.md

**License:** MIT  
**Copyright:** 2026 perrykono-debug

---

---
name: inventory-monitor
description: 库存监控与补货提醒技能。基于真实Excel台账（示例产业园AC+服务.xlsx）监控库存水位，计算可用月数，生成补货提醒。触发场景：(1) 实时监听库存变化（出入库操作），(2) 定时任务每日09:00检查库存状态，(3) 手动触发库存检查（@企服助手 库存检查）。
---

# 库存监控与补货提醒技能 (Inventory Monitor Skill)

## 功能概述

本技能用于实时监控园区库存物资的水位，基于示例产业园A真实Excel台账，自动计算可用月数，当库存低于安全阈值时生成补货提醒并推送到企微。

---

## 数据源配置

**数据文件**: `/Users/mac/示例产业园AC+服务.xlsx`

**工作表映射**:
| 功能模块 | 工作表名 | 用途 |
|---------|---------|------|
| **秩序环境库存** | 📦库存管理📦秩序环境 | 主数据源（日常消耗品） |
| **固定资产库存** | 📦库存管理📦固定资产 | 补充数据（固定资产） |
| **工程库存** | 📦库存管理📦工程 | 补充数据（工程工具） |

---

## 数据接口（真实Excel字段映射）

### 秩序环境库存表字段（11个）

**关键字段**:
| Excel列序号 | 字段名 | 类型 | 说明 | 示例值 |
|-------------|--------|------|------|--------|
| 1 | 名称 | TEXT | 物资名称 | 香薰液 |
| 2 | 规格/单位 | TEXT | 规格 | 桶 / 5片/包 |
| 3 | 总库存 | NUMERIC | 总量 | 9 |
| 4 | 可用月数 | NUMERIC/TEXT | 计算字段 | 9 或 "计算错误" |
| 5 | 图片 | TEXT | 图片链接 | （可选） |
| 6 | 入库 | NUMERIC | 入库数量 | 0 |
| 7 | 出库 | NUMERIC | 出库数量 | 0 |
| 8 | 部门 | TEXT | 所属部门 | 环境 / 安管 |
| 9 | 现库存 | NUMERIC | 当前库存 | 9 |
| 10 | 月使用量 | NUMERIC | 月消耗量 | 1 |
| 11 | 备注 | TEXT | 备注 | 常用物资 |

### 固定资产库存表字段（11个）

| Excel列序号 | 字段名 | 用途 |
|-------------|--------|------|
| 1 | 名称 | 物资名称 |
| 2 | 规格/单位 | 规格 |
| 3 | 总库存 | 总量 |
| 4 | 图片 | 图片链接 |
| 5 | 现库存 | 当前库存 |
| 6 | 入库 | 入库数量 |
| 7 | 入库日期 | 入库时间 |
| 8 | 出库 | 出库数量 |
| 9 | 出库日期 | 出库时间 |
| 10 | 部门 | 所属部门 |
| 11 | 备注 | 备注 |

---

## 核心逻辑

### 1. 库存水位计算

```python
def calculate_inventory_status():
    """
    计算所有物资的库存水位
    
    Returns:
        dict: 分级库存状态
    """
    wb = openpyxl.load_workbook('/Users/mac/示例产业园AC+服务.xlsx')
    
    inventory_status = {
        "缺货": [],     # 可用月数 ≤ 0
        "预警": [],     # 可用月数 ≤ 2
        "关注": [],     # 可用月数 ≤ 3
        "正常": []      # 可用月数 > 3
    }
    
    # 1. 检查秩序环境库存
    ws_env = wb['📦库存管理📦秩序环境']
    
    for row in ws_env.iter_rows(min_row=2, values_only=True):
        name = row[0]           # 名称
        spec = row[1]           # 规格/单位
        current_stock = row[8]  # 现库存
        monthly_usage = row[9]  # 月使用量
        
        # 计算可用月数
        if monthly_usage and monthly_usage > 0:
            available_months = current_stock / monthly_usage
        else:
            available_months = 999  # 无使用量，视为无限
        
        # 分级归档
        item = {
            "名称": name,
            "规格/单位": spec,
            "现库存": current_stock,
            "月使用量": monthly_usage,
            "可用月数": f"{available_months:.1f}",
            "部门": row[7]
        }
        
        if available_months <= 0:
            inventory_status["缺货"].append(item)
        elif available_months <= 2:
            inventory_status["预警"].append(item)
        elif available_months <= 3:
            inventory_status["关注"].append(item)
        else:
            inventory_status["正常"].append(item)
    
    return inventory_status
```

---

### 2. 补货提醒生成

```python
def generate_replenishment_alert():
    """
    生成补货提醒清单
    
    Returns:
        list: 需要补货的物资列表
    """
    inventory_status = calculate_inventory_status()
    
    alerts = []
    
    # 1. 缺货物资（紧急）
    for item in inventory_status["缺货"]:
        alerts.append({
            "物资名称": item["名称"],
            "规格": item["规格/单位"],
            "当前库存": item["现库存"],
            "月使用量": item["月使用量"],
            "可用月数": item["可用月数"],
            "紧急程度": "🚨 缺货",
            "建议采购量": f"{item['月使用量'] * 3}（3个月用量）" if item["月使用量"] else "建议采购"
        })
    
    # 2. 预警物资（高优先级）
    for item in inventory_status["预警"]:
        alerts.append({
            "物资名称": item["名称"],
            "规格": item["规格/单位"],
            "当前库存": item["现库存"],
            "月使用量": item["月使用量"],
            "可用月数": item["可用月数"],
            "紧急程度": "⚠️ 预警",
            "建议采购量": f"{item['月使用量'] * 2}（2个月用量）" if item["月使用量"] else "建议采购"
        })
    
    # 3. 关注物资（中优先级）
    for item in inventory_status["关注"]:
        alerts.append({
            "物资名称": item["名称"],
            "规格": item["规格/单位"],
            "当前库存": item["现库存"],
            "月使用量": item["月使用量"],
            "可用月数": item["可用月数"],
            "紧急程度": "📢 关注",
            "建议采购量": f"{item['月使用量'] * 1}（1个月用量）" if item["月使用量"] else "建议采购"
        })
    
    return alerts
```

---

### 3. 出入库记录更新

```python
def update_stock_transaction(item_name, transaction_type, quantity, department):
    """
    更新出入库记录
    
    Args:
        item_name: 物资名称
        transaction_type: 类型（入库/出库）
        quantity: 数量
        department: 部门
    
    Returns:
        bool: 更新是否成功
    """
    wb = openpyxl.load_workbook('/Users/mac/示例产业园AC+服务.xlsx')
    ws_env = wb['📦库存管理📦秩序环境']
    
    # 查找物资
    for row_idx in range(2, ws_env.max_row + 1):
        if ws_env.cell(row=row_idx, column=1).value == item_name:
            # 更新库存
            current_stock = ws_env.cell(row=row_idx, column=9).value
            
            if transaction_type == "入库":
                new_stock = current_stock + quantity
                ws_env.cell(row=row_idx, column=9).value = new_stock
                ws_env.cell(row=row_idx, column=6).value = quantity  # 入库
            elif transaction_type == "出库":
                new_stock = current_stock - quantity
                ws_env.cell(row=row_idx, column=9).value = new_stock
                ws_env.cell(row=row_idx, column=7).value = quantity  # 出库
            
            # 更新可用月数
            monthly_usage = ws_env.cell(row=row_idx, column=10).value
            if monthly_usage and monthly_usage > 0:
                available_months = new_stock / monthly_usage
                ws_env.cell(row=row_idx, column=4).value = available_months
            
            # 保存Excel
            wb.save('/Users/mac/示例产业园AC+服务.xlsx')
            
            return True
    
    return False
```

---

## 库存监控推送模板

### 每日库存检查

```
━━━━━━━━━━━━━━━
【库存监控日报】2026-05-28

━━━ 🚨 缺货物资 ━━━
{缺货清单}

━━━ ⚠️ 预警物资 ━━━
{预警清单}

━━━ 📢 关注物资 ━━━
{关注清单}

━━━ 统计 ━━━
物资总数：XX个
缺货：XX个 | 预警：XX个 | 关注：XX个

⚡ 操作链接：[腾讯文档-库存管理]
━━━━━━━━━━━━━━━
```

### 紧急补货提醒

```
⚠️⚠️⚠️ 【紧急补货提醒】⚠️⚠️⚠️

物资名称：{name}
规格：{spec}
当前库存：{current_stock}
月使用量：{monthly_usage}
可用月数：{available_months}

建议采购量：{purchase_quantity}

@采购人员 请尽快安排采购

━━━━━━━━━━━━━━━
```

---

## 执行流程

```
Step 1 → 读取Excel库存管理表
         工作表：📦库存管理📦秩序环境
         字段：名称、现库存、月使用量

Step 2 → 计算可用月数
         可用月数 = 现库存 / 月使用量
         特殊情况：月使用量=0 → 视为无限

Step 3 → 分级判断
         ├─ 可用月数 ≤ 0  → 缺货
         ├─ 可用月数 ≤ 2  → 预警
         ├─ 可用月数 ≤ 3  → 关注
         └─ 可用月数 > 3  → 正常

Step 4 → 生成补货提醒
         缺货 → 紧急采购（3个月用量）
         预警 → 高优先级（2个月用量）
         关注 → 中优先级（1个月用量）

Step 5 → 推送企微
         发送给采购人员
```

---

## 定时任务配置

```json
{
  "name": "库存监控检查",
  "schedule": {
    "kind": "cron",
    "expr": "0 9 * * *",
    "tz": "Asia/Shanghai"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "检查所有物资的库存水位，生成补货提醒并推送到企微"
  },
  "sessionTarget": "isolated"
}
```

---

## 手动触发方式

1. **企微 @提及**: `@企服助手 库存检查`
2. **OpenClaw指令**: `检查库存`
3. **出入库操作**: `入库 {物资名称} {数量}` / `出库 {物资名称} {数量}`

---

## 配置参数

```json
{
  "inventory_monitor": {
    "excel_path": "/Users/mac/示例产业园AC+服务.xlsx",
    "sheets": {
      "秩序环境": "📦库存管理📦秩序环境",
      "固定资产": "📦库存管理📦固定资产",
      "工程": "📦库存管理📦工程"
    },
    "alert_thresholds": {
      "缺货": 0,
      "预警": 2,
      "关注": 3
    },
    "wecom_webhook": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx"
  }
}
```

---

## 使用示例

### 示例1：检查库存

**用户输入**: `@企服助手 库存检查`

**输出**:
```
━━━━━━━━━━━━━━━
【库存监控日报】2026-05-28

━━━ 🚨 缺货物资 ━━━
无

━━━ ⚠️ 预警物资 ━━━
1. 洗手液
   规格：桶 | 现库存：2
   月使用量：1 | 可用月数：2.0
   建议采购量：2（2个月用量）

━━━ 📢 关注物资 ━━━
1. 香片
   规格：5片/包 | 现库存：60
   月使用量：11 | 可用月数：5.5

━━━ 统计 ━━━
物资总数：8个
预警：1个 | 关注：1个 | 正常：6个

⚡ 操作链接：[腾讯文档-库存管理]
━━━━━━━━━━━━━━━
```

### 示例2：出入库操作

**用户输入**: `@企服助手 入库 洗手液 5`

**输出**:
```
━━━━━━━━━━━━━━━
【入库操作成功】

物资名称：洗手液
入库数量：5桶
更新后库存：7桶
可用月数：7.0

⚡ 操作链接：[腾讯文档-库存管理]
━━━━━━━━━━━━━━━
```

---

## 后续扩展接口

1. **库存预测** - 基于历史消耗数据预测未来需求
2. **自动采购单** - 当库存低于阈值时自动生成采购单
3. **供应商管理** - 维护供应商信息，快速下单
4. **成本分析** - 分析物资消耗成本，优化采购策略

---

## 注意事项

1. **数据准确性** - 出入库记录需要及时更新
2. **月使用量更新** - 定期更新月使用量数据
3. **采购周期** - 考虑采购周期，提前安排补货
4. **保质期管理** - 某些物资有保质期，需要特殊管理

---

**当前状态**: 技能已调整，数据源已映射到真实Excel库存管理表（3个工作表）。

**核心改进**: 从独立的知识库查询 → 改为直接读取Excel库存管理表 + 水位计算逻辑。
