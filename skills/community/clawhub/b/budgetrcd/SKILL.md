---
name: budgetRcd
description: 个人记账预算管理（支持工作日/周末差异预算 + 动态预算更新机制）。Budget tracking & planning (weekday/weekend differentiated + dynamic budget carry-forward). 记账/设置预算/查余额/存钱目标。Record expenses, set budgets, check balance, savings goals.
triggers: 记账, 花了, 预算, 存钱, 花了多少, 剩余, 本月, record expense, budget, spent, save, remaining
version: 1.5.0
author: Kazuya-ECNU / Akira
license: MIT
---

# budgetRcd v1.4 - 个人记账预算管理 / Budget Tracking & Planning

---

## ⚠️ 执行前必读 / MANDATORY BEFORE ANY OPERATION

**每次执行skill时，必须先读取个人配置：**
```
~/.openclaw/workspace/skills/budgetRcd/budgetRcd.config.json
```

**所有文件操作只能在个人配置的 paths.root 目录下进行！**
**禁止使用任何硬编码路径或其他位置！**

---

## 个人配置 / Personal Config

配置文件：`~/.openclaw/workspace/skills/budgetRcd/budgetRcd.config.json`

```json
{
  "paths": {
    "root": "~/Documents/02_Personal/01_Budget",
    "data": "~/Documents/02_Personal/01_Budget/data",
    "config": "~/Documents/02_Personal/01_Budget/config",
    "images": "~/Documents/02_Personal/01_Budget/images"
  },
  "budget_rules": {
    "weekday": 100,
    "weekend": 200
  },
  "pools": { ... },
  "dynamic_budget": { "enabled": true },
  "pool_name_to_id": { ... }
}
```

---

## 预算规则 / Budget Rules

- 工作日（周一~五）/ Weekdays (Mon–Fri)：**100 元/天**
- 周末（周六/日）/ Weekends (Sat–Sun)：**200 元/天**

---

## 文件结构 / File Structure

所有路径基于 config 中的 `paths.root`：

```
~/Documents/02_Personal/01_Budget/
├── config/
│   └── pools.json          # 预算池配置
├── data/
│   ├── budget_YYYYMM.json  # 月度总预算
│   ├── expense_YYYYMM.json # 开销记录
│   └── goals.json          # 储蓄目标
└── images/
    └── YYYY-MM-DD_merchant.jpg  # 收据照片
```

---

## 操作 / Operations

### 1. 记账 / Record Expense
1. **读取配置** → 获取 paths.data
2. 解析日期/金额/类型
3. 读取 expense_YYYYMM.json
4. 追加新记录（amount 存负数）
5. 保存回 expense_YYYYMM.json
6. 返回剩余预算

### 2. 查状态 / Check Status
1. **读取配置** → 获取 paths.data
2. 读取 expense_YYYYMM.json 和 budget_YYYYMM.json
3. 按工作日/周末分别计算已花/剩余
4. 输出进度

### 3. 查开销 / Query Expenses
1. **读取配置** → 获取 paths.data
2. 读取 expense_YYYYMM.json
3. 按日期或分类聚合返回

### 4. 超支提醒 / Overspend Alert
记账后检查当日累计，超过日预算立即提醒

---

## 动态预算机制 / Dynamic Budget

### 公式
```
dynamic_budget = (remaining_budget + unused_or_overspend) / remaining_days
```

- 未用完的预算 → 加到剩余天数的日预算
- 超支（赤字） → 从剩余天数的日预算中扣除
- 工作日和周末分开计算，互不影响

### 示例 (4月7日查询)
- 已过: 1工作日(花100.7) + 1周末日(花240.7)
- 工作日赤字: 100.7 - 100 = -0.7 → 动态日预算 = (1800 + (-0.7)) / 18 = 99.96
- 周末赤字: 240.7 - 200 = -40.7 → 动态日预算 = (1200 + (-40.7)) / 6 = 193.22

---

## ⚠️ 注意事项 / Important

1. **每次操作前必须读取 config 文件获取最新路径**
2. **所有文件读写只在 paths.root 目录下进行**
3. **不使用统一日均预算，按工作日/周末区分计算**
4. **金额存储为负数（表示支出）**
5. **pool name 和 pool id 的映射使用 pool_name_to_id**

---

## 📖 使用示例 / Usage Examples

### 记账
```
用户: 食其家花了37块9
助手: 记上了！✅ 食其家 -37.9元 | 今日已花 37.9元
```

### 查今日花销
```
用户: 今天钱花哪了
助手: 4月5日花销汇总 💸
     食其家 鸡蛋灌饼  20元
     罗森 苏打水      4.8元
     今日合计: 66.8元 | 剩余预算: 3133.2元
```

### 查看本月预算状态
```
用户: 本月还剩多少
助手: 4月预算状态 📊
     总预算: 3300元 | 已花: 239.8元 | 剩余: 3060.2元
     工作日剩余: 1900元 | 周末剩余: 1400元
```

### 拍照记账
```
用户: [发送收据照片]
助手: 看到照片了！这是什么？花了多少？
用户: 便利店买了零食 23块
助手: 记上了！✅ 全家 -23元 | 剩余预算: 3122.2元
      📎 图片已保存: images/2026-04-06_family.jpg
```

### 超支提醒
```
用户: 罗森买水 8块
助手: 记上了！✅ 罗森 -8元
     ⚠️ 今日已花 244.8元，超过周日预算(200元) 44.8元！
```
