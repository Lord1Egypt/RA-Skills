---
name: family-expense-intent
description: "家庭消费意图识别 V4 - 智能家庭财务管理，支持收入管理、储蓄目标、消费洞察、定期订阅、趋势分析、购物比价。"
homepage: https://github.com/openclaw/skills
metadata:
  clawdbot:
    emoji: "💰"
    requires:
      bins: ["python3"]
---

# 家庭消费意图识别 V4

智能家庭财务管理助手，整合多款优秀技能功能。

## 功能特性 (V4 新增)

- 🤖 **智能识别** - 自动识别消费金额、类别、意图
- 👨‍👩‍👧‍👦 **多人管理** - 支持家庭成员独立档案
- 💰 **收入管理** - 记录工资、兼职、投资收益
- 🎯 **储蓄目标** - 设置目标、追踪进度
- 📊 **模式学习** - 从历史记录中学习消费习惯
- ⚠️ **消费洞察** - AI智能分析消费异常
- 🔄 **定期订阅** - 管理会员、订阅、房租等周期性支出
- 📈 **趋势分析** - 月度/年度消费趋势对比
- 🛒 **购物比价** - 淘宝/京东/拼多多比价
- ⚡ **预算管理** - 设置预算，超支提醒

## 快速开始

### 1. 初始化
```bash
python3 expense_tracker.py add-member "爸爸" "户主"
python3 expense_tracker.py add-member "妈妈" "配偶"
```

### 2. 设置预算
```bash
python3 expense_tracker.py set-budget "餐饮" 3000
python3 expense_tracker.py set-budget "购物" 2000
```

### 3. 记录消费/收入
```bash
# 消费（自动NLP）
python3 expense_tracker.py add-conv member_1 "买了件衣服300块"

# 收入
python3 expense_tracker.py add-income member_1 5000 "工资"

# 订阅
python3 expense_tracker.py add-subscription member_1 "Netflix" 30 "娱乐" "月付"
```

## 命令参考

### 消费记录
```bash
python3 expense_tracker.py add-conv member_1 "消费描述" [--amount N] [--category X]
python3 expense_tracker.py get-convs [--member X] [--days N] [--category X]
python3 expense_tracker.py stats [--member X] [--days N]
```

### 收入管理 (新增)
```bash
python3 expense_tracker.py add-income member_1 5000 "工资"
python3 expense_tracker.py add-income member_1 1000 "兼职"
python3 expense_tracker.py get-income [--member X] [--days N]
```

### 储蓄目标 (新增)
```bash
python3 expense_tracker.py add-goal "旅游基金" 10000 --deadline "2026-12-31"
python3 expense_tracker.py add-goal "紧急备用金" 50000 --priority high
python3 expense_tracker.py contribute-goal "旅游基金" 2000
python3 expense_tracker.py goals
python3 expense_tracker.py goal-progress
```

### 定期订阅 (新增)
```bash
python3 expense_tracker.py add-subscription member_1 "Netflix" 30 "娱乐" "月付"
python3 expense_tracker.py add-subscription member_1 "房租" 2000 "住房" "月付"
python3 expense_tracker.py subscriptions
python3 expense_tracker.py process-recurring
```

### 消费洞察 (新增)
```bash
python3 expense_tracker.py insights [--member X]
python3 expense_tracker.py compare-months
```

### 趋势分析 (新增)
```bash
python3 expense_tracker.py trends 6
python3 expense_tracker.py monthly-report
python3 expense_tracker.py year-report
```

### 购物比价 (新增)
```bash
python3 expense_tracker.py compare "iPhone 15"
python3 expense_tracker.py compare "吹风机" --source taobao
```

### 预算管理
```bash
python3 expense_tracker.py set-budget "餐饮" 3000
python3 expense_tracker.py budgets
python3 expense_tracker.py check-budget "餐饮"
python3 expense_tracker.py budget-alerts
```

### 储蓄建议 (新增)
```bash
python3 expense_tracker.py suggest-savings
```

## 消费/收入类别

### 消费类别
| 类别 | 关键词 |
|------|--------|
| 餐饮 | 买菜、做饭、外卖、下馆子 |
| 购物 | 买衣服、网购、电子产品 |
| 交通 | 打车、加油、公交 |
| 教育 | 学费、培训班、买书 |
| 医疗 | 看病、买药、体检 |
| 娱乐 | 电影、游戏、旅游 |
| 通讯 | 话费、网费 |
| 住房 | 房租、水电、物业 |
| 人情 | 红包、礼物、请客 |

### 收入类别
| 类别 | 说明 |
|------|------|
| 工资 | 主业收入 |
| 兼职 | 副业外快 |
| 投资 | 理财收益 |
| 奖金 | 年终奖等 |
| 其他 | 礼金等 |

## 数据存储

```
~/.openclaw/skills-data/family-expense-intent/
├── profiles.json        # 家庭成员
├── conversations.json   # 消费记录
├── income.json         # 收入记录 (V4新增)
├── patterns.json       # 消费模式
├── budgets.json       # 预算设置
├── goals.json         # 储蓄目标 (V4新增)
├── subscriptions.json  # 定期订阅 (V4新增)
└── imported_data/     # 导入数据
```

## 使用示例

### 示例1: 记录收入
```bash
python3 expense_tracker.py add-income member_1 15000 "工资"
python3 expense_tracker.py add-income member_2 8000 "工资"
```

### 示例2: 设置储蓄目标
```bash
python3 expense_tracker.py add-goal "买房首付" 300000 --priority high
python3 expense_tracker.py add-goal "旅游" 20000 --deadline "2026-06-01"
python3 expense_tracker.py goal-progress
```

### 示例3: 管理订阅
```bash
python3 expense_tracker.py add-subscription member_1 "Netflix" 30 "娱乐" "月付"
python3 expense_tracker.py add-subscription member_1 "Apple Music" 10 "娱乐" "月付"
python3 expense_tracker.py subscriptions
```

### 示例4: 消费洞察
```bash
python3 expense_tracker.py insights
```

输出示例:
```
📊 消费洞察:
- ⚠️ 您本月餐饮支出 ¥3500，超出预算 16%
- 💡 您的娱乐支出连续3个月增长，建议关注
- 🏆 本月消费控制良好，超预算类别减少
- 💡 取消Netflix订阅可每月省 ¥30
```

### 示例5: 月度对比
```bash
python3 expense_tracker.py compare-months
```

输出示例:
```
📈 本月 vs 上月:
- 餐饮: +15% ↑
- 购物: -20% ↓
- 交通: 持平
- 总支出: -5% ↓
```

### 示例6: 趋势分析
```bash
python3 expense_tracker.py trends 6
```

输出示例:
```
📊 近6个月趋势:
1月: ¥8,500
2月: ¥9,200 (+8%)
3月: ¥7,800 (-15%)
4月: ¥8,900 (+14%)
5月: ¥8,300 (-7%)
6月: ¥8,500 (+2%)
```

### 示例7: 购物比价
```bash
python3 expense_tracker.py compare "iPhone 15 256GB"
```

输出示例:
```
🛒 iPhone 15 256GB 比价:
┌─────────────┬────────────┬────────────┐
│ 平台        │ 价格        │ 优惠       │
├─────────────┼────────────┼────────────┤
│ 淘宝        │ ¥6,499     │ 无         │
│ 京东        │ ¥6,499     │ 满减200    │
│ 拼多多      │ ¥6,299     │ 百亿补贴   │
└─────────────┴────────────┴────────────┘
推荐: 拼多多 ¥6,299
```

### 示例8: 完整月度报告
```bash
python3 expense_tracker.py monthly-report
```

输出:
```
═══════════════════════════════════════
     2026年3月 家庭消费报告
═══════════════════════════════════════

💰 收入: ¥23,000
💸 支出: ¥12,500
💵 结余: ¥10,500 (45%)

📊 支出明细:
  餐饮: ¥3,500 (28%) [预算¥3,000, 超16%]
  购物: ¥2,000 (16%) [预算¥2,000, 刚好]
  教育: ¥2,500 (20%) [预算¥2,500, 刚好]
  交通: ¥1,500 (12%) [预算¥1,200, 超25%]
  娱乐: ¥1,000 (8%)  [预算¥800, 超25%]
  其他: ¥2,000 (16%)

📈 趋势:
  vs上月: -5%
  vs今年均值: +2%

🎯 储蓄目标进度:
  买房首付: ¥50,000/¥300,000 (17%)
  旅游基金: ¥3,000/¥20,000 (15%)

⚠️ 提醒:
  - 餐饮、交通、娱乐超预算
  - 建议下月控制餐饮开支
```

## 触发方式

消费相关:
- "消费"、"花钱"、"买"、"花了"、"买了"
- "充了"、"交了"、"花了多少"

收入相关:
- "发工资了"、"赚了"、"兼职"、"奖金"

预算相关:
- "预算"、"超支"、"花了多少"

购物相关:
- "想买"、"比价"、"哪个便宜"

目标相关:
- "存钱"、"目标"、"储蓄"

## 学习自优秀技能

- expense-tracker-pro: 简洁的消费记录
- intelligent-budget-tracker: 收入/目标/订阅/洞察
- taobao: 购物比价

---

**V4 整合升级完成！** 🎉
