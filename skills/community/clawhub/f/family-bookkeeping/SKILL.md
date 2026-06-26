---
name: family-bookkeeping
description: Manage a family bookkeeping workflow backed by Feishu Bitable. Use when the user wants to record an expense or income, say things like "记一笔""记账""入账""查本月支出""看年度统计""修改这笔账""删除这笔账", or import/export household transactions from WeChat or Alipay bills. Also use when the user wants monthly or yearly summaries, category breakdowns, member-based spending analysis, duplicate-safe bill imports, or natural-language CRUD for a shared family ledger.
metadata: { "openclaw": { "requires": { "env": ["FEISHU_APP_ID", "FEISHU_APP_SECRET", "FAMILY_BOOKKEEPING_APP_TOKEN", "FAMILY_BOOKKEEPING_TABLE_ID", "FAMILY_BOOKKEEPING_BITABLE_URL"] } } }
---

# Family Bookkeeping

## Overview

Use this skill as the default workflow for household bookkeeping tasks.

This skill assumes the primary ledger is provided by environment variables unless the user explicitly asks to change it:
- **App token env**: `FAMILY_BOOKKEEPING_APP_TOKEN`
- **Table ID env**: `FAMILY_BOOKKEEPING_TABLE_ID`
- **Bitable URL env**: `FAMILY_BOOKKEEPING_BITABLE_URL`

Primary goals:
1. Record income and expenses from natural language
2. Support update, query, and delete flows safely
3. Prepare for WeChat and Alipay batch bill import
4. Keep category and statistics logic consistent

## Core Ledger Schema

Use these fields as the canonical schema:
- `日期`
- `金额`
- `记账人`
- `一级类型`
- `二级类型`
- `备注`
- `收支类型`
- `支付平台`
- `导入来源`
- `流水号`
- `创建时间`
- `更新时间`

Normalization rules:
- Store `金额` as a positive number
- Batch imports must skip rows where `金额 = 0`
- Use `收支类型` to distinguish `收入` vs `支出`
- Use `流水号` as the preferred dedupe key for imported bills
- If classification is unclear, use `一级类型=其他` and `二级类型=暂未分类`

## Trigger Phrases

Prefer this skill when the user says or implies any of the following:
- `记账`
- `记一笔`
- `入账`
- `今天花了 28`
- `今天午饭 32，记王某`
- `帮我查下这个月花了多少`
- `看下 3 月餐饮支出`
- `把昨天那笔改成交通`
- `删掉今天那杯咖啡`
- `导入支付宝账单`
- `导入微信账单`
- `统计一下今年总支出`
- `按类别看本月开销`

## Default Category System

Use this default mapping unless the user later overrides it.

### 餐饮
- 早饭
- 午饭
- 晚饭
- 外卖
- 饮料
- 咖啡
- 零食
- 聚餐

### 交通
- 打车
- 地铁
- 公交
- 火车
- 高铁
- 机票
- 加油
- 停车
- 过路费
- 共享单车

### 日用购物
- 买菜
- 超市
- 日用品
- 家居用品
- 清洁用品
- 母婴用品
- 宠物用品

### 生活缴费
- 房租
- 水费
- 电费
- 燃气费
- 物业费
- 宽带
- 维修
- 家电
- 话费

### 医疗健康
- 挂号
- 药品
- 检查
- 治疗
- 保健
- 运动

### 教育成长
- 学费
- 书籍
- 课程
- 培训
- 文具

### 娱乐休闲
- 电影
- 游戏
- KTV
- 演出
- 景点
- 旅游
- 酒店
- 兴趣消费

### 人情社交
- 红包
- 礼物
- 聚会
- 请客
- 孝敬父母
- 人情往来

### 服饰美妆
- 衣服
- 鞋包
- 配饰
- 护肤
- 彩妆
- 理发

### 孩子 / 家庭专项
- 奶粉
- 尿不湿
- 玩具
- 学习用品
- 家庭公共支出

### 金融支出
- 信用卡还款
- 手续费
- 利息支出
- 保险

### 收入
- 工资
- 奖金
- 报销
- 兼职
- 红包收入
- 转账收入
- 理财收益
- 退款
- 其他收入

### 其他
- 暂未分类
- 其他支出
- 其他收入

## Workflow Decision Tree

### 1. New record flow

Use when the user wants to add a new transaction.

Extract these fields if possible:
- 日期
- 金额
- 记账人
- 收支类型
- 一级类型
- 二级类型
- 支付平台
- 备注

Rules:
- If amount is missing, ask for it
- If date is missing, infer from user wording like `今天/昨天/前天`; otherwise ask
- If `收支类型` is not explicit, infer from wording; if ambiguous, ask
- If category is unclear, add the record with `其他 / 暂未分类` rather than blocking
- If platform is unknown, leave empty or set `其他`
- Prefer concise confirmation after successful creation

Example interpretations:
- `今天午饭 32` → 支出 / 餐饮 / 午饭
- `老婆买菜 86` → 支出 / 日用购物 / 买菜 / 记账人=老婆
- `报销到账 500` → 收入 / 收入 / 报销

### 2. Update flow

Use when the user wants to change an existing transaction.

Locate the target record using the smallest reliable candidate set based on:
- 日期
- 金额
- 备注关键词
- 记账人
- 平台

Rules:
- If one record matches, update directly
- If multiple plausible records match, present candidates and ask the user to choose
- If the request is vague, ask one short clarifying question
- Preserve untouched fields

Example requests:
- `把昨天那笔咖啡改成 28`
- `把今天那笔买菜改成日用购物`
- `备注改成请同事喝咖啡`

### 3. Delete flow

Use when the user wants to delete a transaction.

Safety rule:
- **Always confirm before deletion** unless the user already identified the exact single record and explicitly reaffirmed deletion in the same turn

Process:
1. Find candidate records
2. If none, say so clearly
3. If one, describe it briefly and ask for confirmation if needed
4. If many, list short candidates and ask which one to delete

### 4. Query and statistics flow

Use when the user asks for summaries or breakdowns.

Common query intents:
- Monthly total income / expense / net balance
- Yearly total income / expense / net balance
- Breakdown by `一级类型`
- Breakdown by `二级类型`
- Breakdown by `记账人`
- Filter by date range, member, platform, category, income/expense

Response style:
- Lead with the answer first
- Then show the main breakdown
- Keep it compact unless the user asks for detail

Suggested summary format:
- 时间范围
- 总支出
- 总收入
- 结余
- Top 3 categories
- Optional member breakdown

### 5. Import flow

Use when the user wants to import WeChat or Alipay bills.

Current policy:
- Do not pretend there is direct account access
- The expected workflow is: user exports a statement file, then provides it for processing

Import rules:
- Prefer using bill platform transaction id as `流水号`
- Deduplicate by `流水号`
- If no transaction id exists, fallback to `日期 + 金额 + 交易对方/备注 + 支付平台`
- Preserve original source in `导入来源`
- Auto-classify conservatively; unclear rows should fall back to `其他 / 暂未分类`

### WeChat mapping
- `日期` ← 交易时间
- `金额` ← 金额(元)
- `收支类型` ← 收/支
- `支付平台` ← 微信
- `流水号` ← 交易单号
- `导入来源` ← 微信账单
- `备注` ← 商品 + 交易对方 + 原备注（可拼接）

### Alipay mapping
- `日期` ← 优先交易付款时间，没有则用交易创建时间
- `金额` ← 金额（元）
- `收支类型` ← 收/支
- `支付平台` ← 支付宝
- `流水号` ← 交易订单号
- `导入来源` ← 支付宝账单
- `备注` ← 商品名称 + 交易对方 + 原备注（可拼接）

## Classification Heuristics

Read `references/category-system.md` when detailed category mapping is needed.
Read `references/usage.md` when practical command examples or operator-facing usage details are needed.

If confidence is low, prefer `其他 / 暂未分类`.

## Operational Notes

- Use Feishu Bitable as the source of truth for this household ledger
- Default live ledger should be read from environment variables:
  - `FAMILY_BOOKKEEPING_APP_TOKEN`
  - `FAMILY_BOOKKEEPING_TABLE_ID`
  - `FAMILY_BOOKKEEPING_BITABLE_URL`
- Default Feishu credentials should be read from environment variables:
  - `FEISHU_APP_ID`
  - `FEISHU_APP_SECRET`
- Those variables are expected to be available in the runtime environment so cross-channel runs do not need to pass explicit credentials each time
- Keep user-visible replies short and practical
- For deletions, require confirmation
- For ambiguous updates, ask one precise question instead of guessing
- Do not silently invent fields outside the canonical schema
- When a future classification dictionary table exists, prefer it over hardcoded keyword rules

## Scripts

### `scripts/normalize_bills.py`

Use this script to normalize exported WeChat or Alipay bill files into the canonical family-bookkeeping schema.

Example usage:

```bash
python3 skills/family-bookkeeping/scripts/normalize_bills.py bill.xlsx --bookkeeper 张三 --format json --output normalized.json
python3 skills/family-bookkeeping/scripts/normalize_bills.py bill.csv --platform alipay --bookkeeper 李四 --format csv --output normalized.csv
```

Behavior:
- Detect or accept platform type (`wechat` / `alipay`)
- Support `.csv` and `.xlsx`
- For WeChat Excel exports, skip the descriptive preface area and locate the real header row automatically
- For Alipay CSV exports, support GB18030 encoding and descriptive prefaces before the real header row
- Normalize source columns into canonical output fields
- Keep `金额` as positive numbers
- Infer `收支类型`
- Skip `不计收支` Alipay rows by default
- Apply lightweight keyword classification
- Deduplicate rows within the import batch

### `scripts/export_feishu_import_csv.py`

Use this script to convert normalized rows into a CSV that Feishu Bitable can import directly.

Example usage:

```bash
python3 skills/family-bookkeeping/scripts/export_feishu_import_csv.py normalized.json --output feishu-import.csv
```

Read `references/feishu-import.md` for the end-to-end import flow and the target ledger mapping.

## Future Expansion

This first version can later be extended with:
- A dedicated category dictionary table
- Direct Feishu batch-write helper scripts
- Saved monthly/yearly reporting templates
- Better duplicate detection and fuzzy merchant normalization
- Shared household member profiles and defaults
