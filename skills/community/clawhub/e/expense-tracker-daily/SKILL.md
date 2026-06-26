---
name: expense-tracker-daily
description: |
  智能记账助手。当用户提到记账、花钱、支出、消费、花费、记录开销、查账、统计支出、账单等意图时触发。
  支持自然语言输入（"午饭花了35"、"打车25块"、"昨天买衣服200"），自动分类，多维度统计分析。
  关键词：记账, 花钱, 支出, 消费, 花费, 账单, 查账, 统计支出, 记录开销, 钱花哪了, 月度统计.
---

# 智能记账

## 核心脚本

所有数据操作通过 `scripts/expense_tracker.py` 完成：

```
SKILL_DIR = {SKILL_DIR}
PYTHON = python
SCRIPT = "{SKILL_DIR}/scripts/expense_tracker.py"
```

### 命令列表

| 命令 | 用途 | 示例 |
|------|------|------|
| `add` | 添加记录 | `--amount 35 --category 餐饮 --desc "午饭" --date 2026-04-09` |
| `list` | 列出记录 | `--limit 20 --category 餐饮 --from 2026-04-01 --to 2026-04-30` |
| `delete` | 删除记录 | `--id 3` |
| `stats` | 统计分析 | `--period month --date 2026-04-09` |
| `categories` | 查看分类 | （无参数） |
| `summary` | 全局总览 | `--top 5` |

### 执行模板

```bash
python "{SKILL_DIR}/scripts/expense_tracker.py" <command> [options]
```

## 处理流程

### 1. 记账

从用户自然语言中提取：金额、分类、描述、日期。

**金额提取规则**（按优先级）：
- `¥35` / `￥35` → 35
- `35元` / `35块` / `35块钱` → 35
- `花了35` / `花了35元` → 35
- `35.5元` → 35.5
- 纯数字 `35` → 35

**日期提取**：
- "今天" → 当天
- "昨天" → 前一天
- "前天" → 前两天
- "上周X" / "上个月" → 对应日期
- 无日期关键词 → 默认今天

**分类判断**：
优先看用户是否明确说了分类（"餐饮花了35"），没有则根据描述中的关键词自动匹配。参考 `references/categories.md` 中的完整关键词表。无法匹配时归入"其他"。

**执行示例**：
```bash
python "{SKILL_DIR}/scripts/expense_tracker.py" add --amount 35 --category 餐饮 --desc "午饭" --date 2026-04-09
```

### 2. 查询记录

```bash
# 最近20条
python "{SKILL_DIR}/scripts/expense_tracker.py" list --limit 20

# 按分类 + 日期范围
python "{SKILL_DIR}/scripts/expense_tracker.py" list --category 餐饮 --from 2026-04-01 --to 2026-04-30
```

### 3. 统计分析

```bash
# 本月统计
python "{SKILL_DIR}/scripts/expense_tracker.py" stats --period month

# 本周统计
python "{SKILL_DIR}/scripts/expense_tracker.py" stats --period week

# 某天统计
python "{SKILL_DIR}/scripts/expense_tracker.py" stats --period day --date 2026-04-09
```

stats 返回 `by_category`（按分类金额）和 `daily`（按日期金额），用来生成人类可读的报告。

### 4. 删除记录

先 list 找到要删除的记录 id，确认后执行：
```bash
python "{SKILL_DIR}/scripts/expense_tracker.py" delete --id 3
```

### 5. 全局总览

```bash
python "{SKILL_DIR}/scripts/expense_tracker.py" summary --top 5
```

## 输出格式

记账成功后回复格式：
```
✅ 已记录：餐饮 ¥35.00 — 午饭 (2026-04-09)
```

查询/统计回复要求简洁，用列表而非表格（适配移动端）：
```
📊 本月支出统计
💰 总计：¥1,280.50（23笔）

📂 分类排行：
  餐饮 ¥580.00 (45.3%)
  交通 ¥320.00 (25.0%)
  购物 ¥200.00 (15.6%)
  其他 ¥180.50 (14.1%)
```

## 数据存储

数据存储在 `~/.qclaw/workspace/expense-tracker-data/expenses.json`，纯本地，不联网。
