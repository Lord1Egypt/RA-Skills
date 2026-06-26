---
name: family-finances
description: 家庭财务管理系统——资产负债表、现金流量表、投资组合追踪与财务健康报告。当用户提到：管理家庭资产/负债、查看净资产、资产负债表、现金流表、投资组合、财务健康评分、家庭财务报表、月度收支报告时触发。
---

# 家庭财务管理系统

管理家庭资产负债表、现金流量表、投资组合，生成中文财务健康报告。

## 数据存储

- **路径**：`~/.openclaw/workspace/data/family-finances/`
- **文件**：
  - `balance_sheet.json` — 资产负债表
  - `cashflow.json` — 现金流量表（月度）
  - `portfolio.json` — 投资组合
- **脚本**：`scripts/finances.py`

## 核心功能

### 1. 资产负债表

| 操作 | 方法 |
|------|------|
| 查看当前报表 | `python scripts/finances.py balance` |
| 计算净资产 | `python scripts/finances.py net-worth` |
| 添加/更新资产 | `update_asset(name, amount, category, note)` |
| 添加/更新负债 | `update_liability(name, amount, category, note)` |
| 删除科目 | `delete_asset(name)` / `delete_liability(name)` |

**资产/负债分类**：
- 资产：现金存款、股票、基金、债券、保险、房产、车辆、数字资产、应收账款、其他
- 负债：房贷、消费贷、车贷、信用卡负债、亲友借款、其他

**添加示例**：
```bash
python scripts/finances.py add-asset "招商银行存款" 150000 "现金存款" ""
python scripts/finances.py add-asset "自住房产" 5000000 "房产" "北京朝阳"
python scripts/finances.py add-liability "房贷余额" 2800000 "房贷" "公积金贷款"
```

### 2. 现金流量表

| 操作 | 方法 |
|------|------|
| 查看月度报表 | `python scripts/finances.py cashflow YYYY-MM` |
| 收入/支出记录 | `add_cashflow_item(year_month, "income"/"expense", category, amount, description)` |

**收入分类**：工资收入、奖金、兼职、投资收益、租金、其他收入  
**支出分类**：餐饮、日用、交通、医疗、教育、住房、娱乐、购物、旅游、保险、税费、其他支出

**添加示例**：
```bash
python scripts/finances.py add-cashflow 2026-04 income "工资" 35000 "月薪"
python scripts/finances.py add-cashflow 2026-04 expense "餐饮" 3000 "在家做饭"
python scripts/finances.py add-cashflow 2026-04 expense "房贷" 12000 "公积金贷款"
```

### 3. 投资组合

| 操作 | 方法 |
|------|------|
| 查看组合汇总 | `python scripts/finances.py portfolio` |
| 添加/更新持仓 | `update_holding(name, amount, category, note)` |
| 删除持仓 | `delete_holding(name)` |

**分类**：股票、基金、债券、保险、房产、车辆、现金存款、数字资产、其他

### 4. 综合报告

生成带财务健康评分的完整报告：

```bash
python scripts/finances.py report YYYY-MM
```

**财务健康评分**（满分100）：
- 储蓄率（满分25）：年储蓄率 ≥40% 满分
- 净资产（满分25）：净资产 ≥100万满分
- 资产结构（满分25）：负债率越低分越高
- 投资比率（满分25）：投资资产占比 ≥50%满分

| 评分 | 等级 |
|------|------|
| ≥90 | 优秀 |
| 70-89 | 良好 |
| 50-69 | 一般 |
| <50 | 需改善 |

## 对话式工作流

当用户请求时，通过对话收集数据，调用脚本读写 JSON：

**初始化/录入数据**：
- 用户说"录入我的资产"→询问具体科目，逐条添加到资产负债表
- 用户说"录入本月收支"→逐笔记录收入和支出

**查询报表**：
- 用户说"我的净资产是多少"→运行 net-worth 命令并解读
- 用户说"本月花了多少钱"→运行 cashflow 命令并解读
- 用户说"生成财务报告"→运行 report 命令，生成完整中文报告

**格式规则**：
- 所有金额单位：人民币（元）
- 报告使用中文，数字加千分位分隔符
- 定期（每月初）提醒用户更新资产快照

## 首次使用引导

首次触发时，引导用户建立基础数据：
1. 先录入主要资产（存款、房产、车辆等）
2. 录入负债（房贷、车贷等）
3. 录入投资组合（股票、基金、保险等）
4. 建议每月固定日期更新一次快照
