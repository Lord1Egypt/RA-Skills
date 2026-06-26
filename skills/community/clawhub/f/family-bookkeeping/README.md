# family-bookkeeping

一个基于 Feishu Bitable 的家庭共享记账 OpenClaw skill。  
An OpenClaw skill for shared household bookkeeping, powered by Feishu Bitable.

---

## 功能简介 / What it does

这个 skill 用来处理常见的家庭记账流程，包括：  
This skill is designed for common family bookkeeping workflows, including:

- 用自然语言记录收入和支出  
  Add expense or income records from natural language
- 查询月度 / 年度汇总  
  Query monthly or yearly summaries
- 查看最近账单  
  View recent records
- 轻量修改已有记录  
  Update existing records with lightweight matching
- 导入微信 / 支付宝账单  
  Import WeChat and Alipay bill exports
- 将原始账单标准化为统一账本结构  
  Normalize bill files into a consistent ledger schema
- 导出适合 Feishu Bitable 导入的 CSV  
  Export Feishu-importable CSV files
- 在需要时直接写入 Feishu Bitable  
  Optionally write records directly into Feishu Bitable

---

## 适用场景 / Supported workflows

### 1. 手动记账 / Manual bookkeeping

示例 / Examples:
- `今天午饭 32`
- `昨天咖啡 18`
- `报销到账 500`

### 2. 查询统计 / Query and reporting

示例 / Examples:
- `查这个月支出`
- `看下 3 月餐饮花了多少`
- `最近 10 笔账单`

### 3. 账单导入 / Bill import

支持 / Supports:
- 微信账单导出 (`.xlsx`) / WeChat bill exports (`.xlsx`)
- 支付宝账单导出 (`.csv`) / Alipay bill exports (`.csv`)
- 标准化中间文件 (`.json` / `.csv`) / Normalized intermediate files (`.json` / `.csv`)

典型流程 / Typical flow:
1. 标准化原始账单文件 / Normalize source bill file
2. 导入前去重检查 / Run duplicate precheck
3. 导出 Feishu 导入 CSV / Export Feishu import CSV
4. 通过 Feishu UI 导入，或直接通过 API 写入  
   Import through Feishu UI or write directly via API

---

## 项目结构 / Project structure

- `SKILL.md` — skill 说明与工作流规则 / skill instructions and workflow rules
- `scripts/` — 标准化、查询、导入、修改等辅助脚本 / helper scripts for normalization, querying, import, and updates
- `references/` — 分类、导入映射、统计说明等参考文档 / supporting notes for categories, import mapping, reporting, and usage

---

## 环境变量 / Required environment variables

请在本地环境中配置以下变量：  
Configure the following variables in your local environment:

- `FEISHU_APP_ID`
- `FEISHU_APP_SECRET`
- `FAMILY_BOOKKEEPING_APP_TOKEN`
- `FAMILY_BOOKKEEPING_TABLE_ID`
- `FAMILY_BOOKKEEPING_BITABLE_URL`

---

## 示例命令 / Example commands

### 标准化账单 / Normalize a bill file

```bash
python3 skills/family-bookkeeping/scripts/normalize_bills.py bill.xlsx \
  --bookkeeper 张三 \
  --format json \
  --output normalized.json
```

### 导入前检查 / Precheck before import

```bash
python3 skills/family-bookkeeping/scripts/import_precheck.py normalized.json \
  --app-token "$FAMILY_BOOKKEEPING_APP_TOKEN" \
  --table-id "$FAMILY_BOOKKEEPING_TABLE_ID" \
  --output-dir ./precheck-out
```

### 运行完整导入链路 / Run the full import pipeline

```bash
python3 skills/family-bookkeeping/scripts/import_bills_pipeline.py bill.xlsx \
  --bookkeeper 张三
```

### 查询最近记录 / Query recent records

```bash
python3 skills/family-bookkeeping/scripts/recent_records.py --limit 10
```

---

## 说明 / Notes

- 本仓库不包含任何凭证或生产环境账本配置  
  This repository does not include credentials or live production ledger configuration.
- 使用 Feishu 能力前需要先配置环境变量  
  Environment variables are required for Feishu access.
- 删除类操作应始终要求用户明确确认  
  Deletion workflows should always require explicit confirmation.
- 分类不确定时，默认回退到 `其他 / 暂未分类`  
  For uncertain classifications, the default fallback is `其他 / 暂未分类`.

---

## License

MIT License
