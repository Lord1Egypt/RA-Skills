---
name: cashbook
description: Local-first personal bookkeeping Skill (SQLite). Supports natural language and screenshot-based expense recording, account management, budget tracking, weekly/monthly reports, and CSV import (Alipay/WeChat). Trigger phrases include "record expense", "spent $X on Y", "set budget", "monthly report", "export transactions", "delete last entry", "import CSV", or upload a receipt/payment screenshot. Also responds to Chinese triggers like "记一笔", "花了多少", "出月报", "设置预算". Use for all personal bookkeeping and expense tracking tasks.
---

# cashbook

面向中文用户的本地记账 Skill。数据存储在本地 SQLite，用户拥有完整数据主权。

## 开箱即用

首次使用时数据库自动创建（建表 + 预置分类），无需手动初始化。

用户第一次记账时，若还没有账户，先引导创建一个默认账户：
```bash
python3 scripts/account.py add --nickname "默认钱包" --type wallet
python3 scripts/account.py default --id 1
```

数据库路径：`~/.local/share/cashbook/cashbook.db`（可通过 `CASHBOOK_DB` 环境变量覆盖）  
如需重置：`python3 scripts/init.py --force`

---

## 核心工作流

### 1. 自然语言记账

从用户输入提取结构化字段，调用 `scripts/add_tx.py`：

```bash
python3 scripts/add_tx.py \
  --amount 38 --type expense --category 餐饮 \
  --account "招行信用卡" --date today --note "星巴克"
```

**解析字段：** 金额、收/支类型、分类、账户（可选）、日期、备注/商户  
**时间表达：** 支持"今天/昨天/上周三/3月10日"等，统一转为 YYYY-MM-DD  
**确认流程：** 解析后先展示给用户确认，确认后再写入

**多语言支持：** 用户可用中文、英文或日文描述交易，分类传参支持英文别名（如 food→餐饮、transport→交通、shopping→购物）。无论用户用什么语言，`--category` 传中文分类名或英文别名均可。

### 2. 截图记账

用户上传图片时，使用 `image` tool 分析截图，提取关键字段后走确认流程入库。

**支持类型：** 微信支付截图、支付宝截图、POS 小票、外卖/电商订单截图

**工作流：**
1. 调用 `image` tool，prompt 示例：
   > 这是一张支付截图。请提取以下字段（JSON 格式返回）：amount（金额，数字）、merchant（商户名）、date（日期，YYYY-MM-DD，无法确定则用今天）、pay_method（支付方式，如微信/支付宝/银行卡）、type（expense/income）
2. 展示解析结果，请用户确认或修改：
   > 解析结果：支出 ¥38.00 / 星巴克 / 2026-03-16 / 微信支付  
   > 分类建议：餐饮。确认入账？（可修改分类/金额/日期）
3. 用户确认后调用 `add_tx.py` 写入，`--source screenshot`
4. **多张截图：** 逐张解析，全部展示后统一确认批量入库

**解析失败处理：** 图片模糊或字段缺失时，告知用户并请求补充信息，不强行入库。

### 3. 删除记录

```bash
python3 scripts/delete_tx.py --id 5          # 按 ID 删除
python3 scripts/delete_tx.py --last 1 --yes  # 删最新一条（跳过确认）
```

删除会自动回滚账户余额。先用 `query.py --last 10` 确认 ID 再删。

### 4. 账户管理

详见 [references/account.md](references/account.md)

```bash
python3 scripts/account.py add --nickname "招行储蓄卡" --type debit --last4 1234
python3 scripts/account.py list
python3 scripts/account.py default --id 1
python3 scripts/account.py edit --id 1 --nickname "新名字"
python3 scripts/account.py delete --id 2
```

### 5. 预算管理

详见 [references/budget.md](references/budget.md)

```bash
python3 scripts/budget.py set --category 餐饮 --amount 2000          # 月度分类预算
python3 scripts/budget.py set --amount 8000                          # 月度总预算
python3 scripts/budget.py query --all                                 # 查所有分类进度
python3 scripts/budget.py query --category 餐饮                       # 查单个分类
python3 scripts/budget.py list
python3 scripts/budget.py delete --category 餐饮
```

### 6. 查询流水

```bash
python3 scripts/query.py --last 10                          # 最近10条明细
python3 scripts/query.py --period month                     # 本月汇总
python3 scripts/query.py --period week --category 餐饮      # 本周餐饮
python3 scripts/query.py --from 2026-03-01 --to 2026-03-15
```

### 7. 周报 / 月报

```bash
python3 scripts/report.py --period week
python3 scripts/report.py --period month
python3 scripts/report.py --period month --year 2026 --month 2   # 指定月份
```

报告含：收支汇总、分类分布 + ASCII 进度条、预算执行情况（月报）、最高单笔。

### 8. CSV 导入（支付宝 / 微信）

```bash
python3 scripts/import_csv.py --file ~/Downloads/alipay_record.csv --account "支付宝"
python3 scripts/import_csv.py --file ~/Downloads/wechat_record.csv --account "微信钱包"
python3 scripts/import_csv.py --file xx.csv --dry-run   # 预览不写入
```

自动检测格式、分类映射、重复跳过。

### 9. 数据导出

```bash
python3 scripts/export.py --format csv
python3 scripts/export.py --format csv --from 2026-01-01 --to 2026-03-31
```

默认输出到 `~/Downloads/cashbook-YYYY-MM.csv`

---

## 分类

支出预置：餐饮、交通、购物、娱乐、医疗、住房、教育、旅行、其他  
收入预置：工资、奖金、副业、其他  
自定义：`python3 scripts/category.py add --name 宠物 --type expense`

## 不存储的敏感信息

完整卡号、CVV、密码、银行登录凭证。只存：昵称、卡类型、尾号（可选）。

## 数据模型

见 [references/schema.md](references/schema.md)
