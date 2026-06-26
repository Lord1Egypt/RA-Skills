---
name: "accounting"
description: 智能记账助手。用户提到记账、支出、收入、账本、流水、应收、应付、发票、票据、报销等关键词时使用此技能。支持文字直接记账，也可调用其他技能预处理图片/语音/文件后进行记账。
metadata: { "openclaw": { "emoji": "💰", "requires": { "bins": ["python"], "env": ["ACCOUNTING_API_TOKEN"] }, "primaryEnv": "ACCOUNTING_API_TOKEN" } }
---

# 智能记账助手

基于自有记账服务 API 的 OpenClaw 技能，负责记账的核心逻辑。

**本技能支持以下输入方式**：
1. **文字记账** — 用户直接用文字说明金额、类型等信息
2. **预处理后记账** — 先调用其他技能解析多媒体内容，然后进行记账

## 记账相关信息检测

无论用户输入是文字还是经过预处理的内容，都必须先检测是否包含记账相关信息。

**记账相关信息检测规则**：

1. **金额检测**：必须识别到有效的金额数字（> 0）
2. **收支类型检测**：必须能判断交易类型（收入/支出/应收/应付）
3. **记账关键词检测**：内容需包含以下任一类关键词：
   - 收入类：收到、收款、入账、回款、存入、转入、工资、奖金、提成、分红、利息、退回、退款
   - 支出类：支付、付款、买、采购、花、花了、花费、消费、报销、支出、花费、购买、订购
   - 应收类：应收、待收、别人欠我、借出、赊账
   - 应付类：应付、待付、我欠、借入、赊购
   - 票据类：发票、收据、票据、小票、账单、账单号、报销单

**检测逻辑**：
- 如果检测到记账相关信息，进入记账流程
- 如果未检测到记账相关信息，回复用户「该内容未发现记账相关信息，无法进行记账」，结束流程

## 环境变量

```bash
# 必填：记账 API Token
export ACCOUNTING_API_TOKEN="agent_4...25"
```

## 脚本路径

- 记账主脚本：`{baseDir}/scripts/accounting.py`

---

## 一、记账相关的CLI工具

### 1. 记账（新增交易）

```bash
python {baseDir}/scripts/accounting.py add '{
  "ledgerName": "日常开销",
  "amount": 35.5,
  "transactionType": "支出",
  "categoryName": "餐饮",
  "description": "午餐"
}'
```

transactionType 取值：`收入`、`支出`、`应收`、`应付`。

完整参数示例：

```bash
python {baseDir}/scripts/accounting.py add '{
  "ledgerName": "公司账本",
  "accountName": "招商银行",
  "amount": 10000,
  "transactionType": "收入",
  "categoryName": "服务收入",
  "handlerName": "张三",
  "companyName": "XX科技有限公司",
  "description": "3月咨询服务费",
  "transactionDate": "2025-03-20",
  "needInvoice": true,
  "fee": 6.5
}'
```

应收/应付时 `dueDate` 必填：

```bash
python {baseDir}/scripts/accounting.py add '{
  "ledgerName": "公司账本",
  "amount": 5000,
  "transactionType": "应收",
  "companyName": "客户A",
  "description": "待收货款",
  "dueDate": "2025-04-30"
}'
```

### 2. 查账（查询交易流水）

```bash
python {baseDir}/scripts/accounting.py query '{
  "ledgerName": "日常开销",
  "startTime": "2025-03-01",
  "endTime": "2025-03-31",
  "transactionType": "支出",
  "pageNum": 1,
  "pageSize": 10
}'
```

### 3. 查账本列表

```bash
python {baseDir}/scripts/accounting.py ledgers
```

### 4. 查记账账户

```bash
python {baseDir}/scripts/accounting.py accounts '{"ledgerName": "日常开销"}'
```

### 5. 查收支分类

```bash
python {baseDir}/scripts/accounting.py categories '{"type": "支出"}'
```

type 取值：`收入`/`支出`/`应收`/`应付`。

### 6. 查经手人

```bash
python {baseDir}/scripts/accounting.py handlers
```

### 7. 查关联企业

```bash
python {baseDir}/scripts/accounting.py companies
```

---

## 二、文字记账工作流

**步骤 1：记账相关信息检测**

检测用户输入的文字是否包含记账相关信息（金额、收支类型、记账关键词）。

如果未检测到记账相关信息，回复用户「该内容未发现记账相关信息，无法进行记账」，结束流程。

**步骤 2：提取记账关键字**

从文字中抽取：
- 金额（必须 > 0）
- 交易类型（收入/支出/应收/应付）
- 账本、账户、收支分类、经手人、企业
- 是否有发票、记账时间、逾期时间、手续费等

**步骤 3：查询记账元数据**

并行调用以下命令，获取当前系统中已有的账本、收支分类、经手人、企业等信息：

```bash
python {baseDir}/scripts/accounting.py ledgers
python {baseDir}/scripts/accounting.py categories '{"type": "支出"}'
python {baseDir}/scripts/accounting.py categories '{"type": "收入"}'
python {baseDir}/scripts/accounting.py handlers
python {baseDir}/scripts/accounting.py companies
```

**步骤 4：AI 对齐记账信息**

根据提取的文字内容，结合步骤 3 查到的元数据列表，对齐以下字段：

| 字段 | 对齐规则 |
|------|----------|
| ledgerName | 最近匹配已有账本名称，未匹配使用默认账本 |
| amount | 从文字中提取，必须 > 0 |
| transactionType | 根据文字判断（收入/支出/应收/应付） |
| categoryName | 根据文字最近匹配已有收支分类 |
| handlerName | 匹配已有经手人列表 |
| companyName | 匹配已有企业列表 |
| description | 用文字摘要生成 |
| transactionDate | 从文字提取，格式 yyyy-MM-dd，默认今天 |
| needInvoice | 如果识别出是发票，设为 true |

**步骤 5：记账**

```bash
python {baseDir}/scripts/accounting.py add '<json>'
```

字段按最近匹配，未匹配的使用默认值，直接完成记账，不用向用户确认。

---

## 三、多媒体内容预处理记账

当用户发送图片、语音、文件并要求记账时，按以下流程处理：

### 预处理阶段：调用对应技能解析内容

根据用户发送的内容类型，调用对应的其他技能进行预处理：

| 内容类型 | 调用技能 | 获取内容 |
|----------|-----------|----------|
| 图片 | `ocr` 技能 | 调用 ocr 或类似技能获取图片识别的文本内容 |
| 语音 | `stt` 技能 | 调用 stt 或类似技能获取语音转写的文本内容 |
| PDF/Excel/Docx | `parse_file` 技能 | 调用 parse_file 技能获取文件提取的文本内容 |

**注意**：如果调用其他技能失败或返回结果为空，提示用户「抱歉，目前无法处理此格式的内容」，结束流程。

### 预处理阶段：记账相关信息检测

基于预处理获得的文本内容，检测是否包含记账相关信息：
- 如果未检测到有效金额或记账相关信息，回复用户「内容中未发现记账相关信息，无法进行记账」，结束流程

### 记账阶段

检测到记账相关信息后，进入标准的记账流程：

**步骤 1：查询记账元数据**

```bash
python {baseDir}/scripts/accounting.py ledgers
python {baseDir}/scripts/accounting.py categories '{"type": "支出"}'
python {baseDir}/scripts/accounting.py categories '{"type": "收入"}'
python {baseDir}/scripts/accounting.py handlers
python {baseDir}/scripts/accounting.py companies
```

**步骤 2：AI 对齐记账信息**

根据预处理获得的文本内容，结合元数据列表，对齐记账字段：

| 字段 | 对齐规则 |
|------|----------|
| ledgerName | 最近匹配已有账本名称 |
| amount | 从文本中提取，必须 > 0 |
| transactionType | 根据文本判断（如发票通常是支出） |
| categoryName | 根据文本最近匹配已有收支分类 |
| handlerName | 如果文本有经手人信息，匹配已有列表 |
| companyName | 从文本的销售方/购买方等提取，匹配已有列表 |
| description | 用文本摘要生成（如"XX公司开具的增值税发票"） |
| transactionDate | 从文本提取，格式 yyyy-MM-dd，默认今天 |
| needInvoice | 如果识别出是发票，设为 true |

**步骤 3：记账**

```bash
python {baseDir}/scripts/accounting.py add '<json>'
```

字段按最近匹配，未匹配的使用默认值，直接完成记账，不用向用户确认。

### 示例场景

**场景 1：用户发送增值税发票图片要求记账**

1. 调用 `ocr` 或类似技能获取识别文本
2. OCR 识别出：金额 20000.00、销售方 江苏XX公司、日期 2025-04-26
3. 检测到记账相关信息（金额 + 票据关键词）
4. 查询账本列表 ["公司账本", "日常开销"]
5. 对齐：ledgerName="公司账本"、amount=20000、transactionType="支出"、companyName="江苏XX公司"、transactionDate="2025-04-26"、needInvoice=true
6. 调用 add 记账

**场景 2：用户发送语音要求记账**

1. 调用 `STT` 或类似技能获取转写文本
2. 转写结果：「今天午饭花了35块」
3. 检测到记账相关信息（金额 + 支出关键词）
4. 对齐：amount=35、transactionType="支出"、categoryName="餐饮"、description="午饭"
5. 调用 add 记账

**场景 3：用户发送 Excel 报销单要求记账**

1. 调用 `parse_file` 或类似技能获取文件内容
2. 提取文本包含多行报销数据
3. 检测到记账相关信息（金额 + 报销关键词）
4. 逐行提取并批量记账
5. 如果某行无法提取完整信息，跳过该行

---

## 四、记账参数说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| ledgerName | String | 是 | 账本名称（不确定时先调用 `ledgers` 查询） |
| accountName | String | 否 | 结算账户名称 |
| amount | Number | 是 | 交易金额（>0） |
| transactionType | String | 是 | 收入/支出/应收/应付 |
| categoryName | String | 否 | 收支分类名称（可先调用 `categories` 查询） |
| handlerName | String | 否 | 经手人名称 |
| companyName | String | 否 | 关联企业名称 |
| description | String | 否 | 描述 |
| transactionDate | String | 否 | 交易时间（yyyy-MM-dd，默认今天） |
| needInvoice | Boolean | 否 | 是否需要发票 |
| dueDate | String | 条件必填 | 到期时间（应收/应付时必填） |
| fee | Number | 否 | 手续费 |

---

## 五、注意事项

### 通用注意事项

- 金额 amount 必须大于 0
- 应收和应付类型必须提供 dueDate
- 不确定账本名称时，务必先查询 ledgers 再记账
- 预处理后记账时，提取的信息务必先展示给用户确认，再执行记账

### 预处理相关

- **图片预处理**：调用 `ocr` 或类似技能，依赖该技能的处理能力
- **语音预处理**：调用 `stt` 或类似技能，依赖该技能的处理能力
- **文件预处理**：调用 `parse_file` 或类似技能，依赖该技能的处理能力

### 无法处理的情况

以下情况应直接提示用户，结束流程：

- 调用预处理技能失败或返回结果为空
- 预处理后的内容未发现记账相关信息（无金额、无收支类型、无记账关键词）
- 预处理技能不支持该格式
