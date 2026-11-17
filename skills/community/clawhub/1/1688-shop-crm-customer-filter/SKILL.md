---
name: 1688-shop-crm-customer-filter
version: 1.1.0
description: |
  1688 店铺 CRM 客户智能筛选 Skill。支持按标签、金额、活跃度、采购意愿、自定义属性等条件筛选客户，支持排序、分页、统计，以及查看和新增自定义属性。
  触发词：筛选客户、查找客户、客户列表、询盘未转化、询盘未成交、有成交客户、新增字段、自定义属性、帮我找客户、我的客户。
metadata: {"openclaw": {"emoji": "👥", "requires": {"anyBins": ["python3", "python"]}}}
---

# 1688 店铺 CRM 客户智能筛选

统一入口：

```bash
python3 {baseDir}/cli.py <command> [options]
```

只能通过 Bash/命令行执行 `cli.py`，不要把它当作 Python 函数调用。Python 运行时使用 `python3`，Windows 可使用 `python`；依赖第三方库 `requests`。

常规筛选、排序、分页和字段管理只需阅读本文件。仅在需要低频接口契约或排障细节时查看 `references/`。

## 核心工作流

1. 判断需求属于客户筛选、统计还是字段管理。
2. 将用户表述映射到本文件的字段和业务语义；只有预置字段无法覆盖时才查询动态字段配置。
3. 构造 filters / sorts，范围和同字段多值用一次 `in` 表达。
4. 执行一次查询并使用首次成功结果；只有明确错误或空结果需要诊断。
5. 默认直接展示返回的 `markdown`，再用业务语言补充必要说明。

典型查询通常只需 2～3 步，无需额外维护任务清单。

## 命令

| 命令 | 用途 | 示例 |
|------|------|------|
| `alibaba.1688.customer.list` | 筛选、排序、分页查询客户 | `cli.py alibaba.1688.customer.list --filters-file filters.json --page-size 20` |
| `alibaba.1688.customer.attr.field.config` | 查看最新动态字段和标签 | `cli.py alibaba.1688.customer.attr.field.config --raw` |
| `customer_attr_add` | 新增自定义属性 | `cli.py customer_attr_add --key credit_score --label 信用分` |

## 客户查询

### 参数

| 选项 | 说明 |
|------|------|
| `--filters-file <path>` | 筛选条件 JSON 文件，所有平台推荐，Windows 必须 |
| `--sorts-file <path>` | 排序条件 JSON 文件，所有平台推荐，Windows 必须 |
| `--filters <json>` | 直接传筛选 JSON，仅 Unix/macOS 兼容 |
| `--sorts <json>` | 直接传排序 JSON，仅 Unix/macOS 兼容 |
| `--page-num <int>` | 页码，从 1 开始，默认 1 |
| `--page-size <int>` | 每页 1～100 条，默认 20 |
| `--raw` | 在 `data.items` 返回当前页完整客户记录；默认仅返回摘要和分页元数据 |

不要使用 `--items`、`--limit`、`--count` 等未定义参数。

### 文件入参

filters 和 sorts 都必须写入 JSON 文件；把 JSON 串传给 `--filters-file` / `--sorts-file` 一定失败（直接传 JSON 只能分别使用 `--filters` / `--sorts`）。

```json
[{"field":"site_flag","op":"=","value":"Y"}]
```

```json
[{"field":"last_inquiry_time","order":"desc"}]
```

调用示例：

```bash
python3 {baseDir}/cli.py alibaba.1688.customer.list \
  --filters-file /absolute/path/filters.json \
  --sorts-file /absolute/path/sorts.json \
  --page-size 20
```

Windows 下禁止直接传 filters/sorts JSON，也不要用 shell `echo` 拼接 JSON。唯一稳定的形态是**在同一条 `python -c` 命令内完成写文件和调用**，把文件绝对路径通过 Python 变量直接传给 CLI：

```bash
python -c "import json,os,subprocess,tempfile; d=os.environ.get('NEWTON_SCRATCH_DIR') or os.environ.get('TEMP') or tempfile.gettempdir(); os.makedirs(d,exist_ok=True); f=os.path.join(d,'filters.json'); json.dump([{'field':'site_flag','op':'=','value':'Y'}],open(f,'w',encoding='utf-8')); print(f); subprocess.run(['python',r'{baseDir}/cli.py','alibaba.1688.customer.list','--filters-file',f,'--page-size','20'])"
```

**路径规范（违反必现文件找不到）：**

- 写文件和调用必须在同一条命令内完成；若平台强制分步，写文件命令必须 `print(f)` 出绝对路径，下一步只能使用这个打印出的字面路径。
- 禁止自行重新推导路径：不要用 `%TEMP%`、`$TEMP`、`$env:TEMP`、`/tmp`、`./filters.json` 等相对路径或 shell 变量。
- `NEWTON_SCRATCH_DIR` 与 `%TEMP%` 在 Newton/Windows 沙箱中指向不同目录，混用一定失败。
- 两个环境变量都缺失时，示例会 fallback 到 `tempfile.gettempdir()`，避免 `makedirs(None)` 崩溃。

### filters 与 sorts

filter 结构：

```json
{"field":"user_interest_level","op":"=","value":"高意愿"}
```

- `field`：筛选字段。
- `op`：`=`、`>`、`<`、`>=`、`<=`、`like`、`in`、`not in`。不支持 `or`，也没有跨字段 OR 能力；同字段多值请用 `in` 单次表达。
- `value`：筛选值；`in` / `not in` 必须传 JSON 数组字符串，例如 `"[\"VIP\",\"L3\"]"`。

sort 结构：

```json
{"field":"last_inquiry_time","order":"desc"}
```

`order` 只能是 `asc` 或 `desc`。可排序字段：

- `last_inquiry_time`
- `recent_30d_purchase_amount`
- `gmt_create`
- `pay_ord_amt_std_all`

### 可筛选字段

以下字段可直接使用，无需先查询字段配置：

| 字段 | 业务含义 | 常用值或操作符 |
|------|----------|----------------|
| `buyer_nick` | 买家昵称 | `like` |
| `site_flag` | 客户来源渠道 | `Y`=站内，`N`=站外 |
| `source` | 历史买卖关系 | `INQUIRY`=询盘未成交，`ORDER`=历史有成交 |
| `phone` | 手机号 | `=` / `like` |
| `follower` | 跟进人 | `=` |
| `shop_ids` | 归属店铺 | `=` |
| `tags` | 标签、买家等级 | `in` / `not in` |
| `recent_30d_activity_score` | 近 30 天活跃度 | 高、中、低 |
| `user_interest_level` | 采购意愿 | 高意愿、中意愿、低意愿 |
| `procurement_mode_30d` | 近 30 天合作关系 | 新买家、未复购老买家、复购老买家 |
| `user_label_preset` | 客户身份 | B类买家、非淘电商、个人买家、内容&社交电商、实体店、淘天电商、餐饮住宿店、国内跨境、海外买家、超市百货店、淘宝直播、微商、抖音小店、企业自采、超级买家；使用 `in` |
| `buyer_credit_level` | 买家等级 | L0～L6 |
| `lost_status` | 流失状态 | 未流失、已流失、稳定复购、即将流失 |
| `pay_ord_amt_std_all` | 历史累计支付金额 | 数值比较 |
| `pay_mord_cnt_std_all` | 历史累计支付订单数 | 数值比较 |
| `recent_30d_purchase_amount` | 近 30 天成交金额 | 数值比较 |
| `pay_ord_amt_1w` | 近 7 天支付金额 | 数值比较 |
| `pay_mord_cnt_1w` | 近 7 天支付订单数 | 数值比较 |
| `pay_ord_amt_1m` | 近 30 天支付金额 | 数值比较 |
| `last_inquiry_time` | 最近询盘时间 | 日期比较 |
| `gmt_create` | 客户创建时间 | 日期比较 |
| `web_action_1m_level` | 月度网站活跃度 | 高、中、低 |
| `ord_cnt_1m_level` | 月采购频率等级 | 高、中、低 |
| `gmv_1m_level` | 月采购金额等级 | 高、中、低 |
| `se_1m_level` | 月度搜索频率 | 高、中、低 |
| `interest_action_1m_level` | 月度兴趣行为 | 高、中、低 |
| `inq_action_1m_level` | 月度询盘频率 | 高、中、低 |
| `pay_action_1m_level` | 月度下单频率 | 高、中、低 |

`gmt_modified` 和 `last_order_time` 可能出现在结果中，但不可用于筛选。用户需要预置表以外的自定义属性时，调用 `alibaba.1688.customer.attr.field.config --raw`，直接使用返回的 `attrKey`，不要添加 `attr_` 前缀。

标签由商家维护，实际可用标签可能变化；只有需要确认最新标签时才查询字段配置，不要把 field_config 作为每次查询的固定前置步骤。

## 业务语义

### 范围和多值

- “X 以上”不包含 X；“X 及以上”包含 X。
- `L3 以上` → L4、L5、L6。
- `L3 及以上` → L3、L4、L5、L6。
- 即使上游括注与该规则冲突，也按“以上不含本级、及以上含本级”处理。
- 同字段多值和等级范围必须用一次 `in` 查询，不要拆成多次查询再汇总。
- 标签筛选固定使用 `tags` 和 `in`；单标签也使用数组字符串。

示例：

```json
{"field":"tags","op":"in","value":"[\"L3\",\"L4\",\"L5\",\"L6\"]"}
```

### 金额口径

| 用户表述 | 字段 |
|----------|------|
| 累计、总、历史、全部支付/采购/消费金额 | `pay_ord_amt_std_all` |
| 近 30 天、近一个月、近期成交金额 | `recent_30d_purchase_amount` |
| 近 7 天支付或成交金额 | `pay_ord_amt_1w` |
| 仅说“采购金额/消费金额”，无时间范围 | 默认 `pay_ord_amt_std_all` |

不要在累计口径和近 30 天口径之间替换。面向用户展示时说明所用口径；多轮追问若仍是相同金额维度，沿用上一轮字段，除非用户明确改变时间范围。

### 常见映射

| 用户意图 | 筛选条件 |
|----------|----------|
| 高意愿 | `user_interest_level in ["高意愿"]` |
| 中等意愿及以上 | `user_interest_level in ["中意愿","高意愿"]` |
| 近 7 天有成交 | `pay_mord_cnt_1w > 0` |
| 历史有成交 | `source = ORDER` |
| 询盘未成交/未转化 | `source = INQUIRY` |
| 近 7 天询盘未转化/未下单 | `last_inquiry_time >= 当前日期-7天` 且 `pay_mord_cnt_1w <= 0`，默认 `last_inquiry_time desc` |
| 流失风险 | `lost_status in ["即将流失","已流失"]` |
| 累计支付超过 1 万 | `pay_ord_amt_std_all > 10000` |
| 近 30 天成交超过 1 万 | `recent_30d_purchase_amount > 10000` |

`user_interest_level` 空值表示未评估，不得归为低意愿。

## 查询规则

### 首次结果与重试

- 首次调用成功后直接使用结果，不重复执行相同查询。
- 只有参数、网络、限流等明确错误才修正后重试，最多 3 次。
- 空结果先检查字段、操作符、枚举值、范围换算和金额口径。
- 如需拆解空结果，每个子条件最多查询一次且 `page-size=1`，总诊断不超过 3 次。
- 不要通过反复更换 page-size、重复 raw 查询或臆造字段探测后端能力。
- 多轮追问仍指向同一业务维度时沿用上一轮字段；只有用户明确切换维度时才重新映射。

### 探索预算

- 常规查询直接执行，不预先探测字段。
- 只有预置字段无法覆盖时才查询一次 field_config。
- 只有需要确认返回样例字段时才使用一次 `--raw`。
- 若字段不存在，明确告诉用户数据源没有该字段，不得静默省略或用相近字段冒充。

### 能力边界

- 只能使用本文件「命令」表中列出的能力；禁止尝试加载或探测不存在的命令、参数或能力。
- 不要为了满足用户而臆造字段、枚举值或操作符。

## 输出

所有命令输出 JSON，稳定包含 `success` 和 `data`。

- 默认 alibaba.1688.customer.list 返回 `success`、`markdown` 和轻量分页元数据。
- `--raw` 不返回 markdown，当前页客户位于 `data.items`。
- raw 客户字段使用下划线 attrKey，如 `buyer_nick`、`site_flag`、`last_inquiry_time`；`extraAttrs` 的键也使用 attrKey。
- `__state_update__`、`filters`、`sorts`、`action` 是框架内部状态字段。Agent 不解析、不展示，存在时原样保留。

展示时直接输出 `markdown`，不要改写或把分析混入表格。补充说明使用业务语言，不向用户暴露命令名、filters、sorts、原始 JSON、接口字段结构、调用过程或内部思考过程。

若用户要求的结果字段不存在，必须说明数据缺口。例如只有流失状态而没有具体流失原因时，应明确说明无法直接提供原因。

退出码：`0`=成功，`1`=参数/业务错误，`2`=认证失败，`3`=限流/网络/服务异常。

## 字段管理

### 查看字段

仅当需求涉及未知自定义属性或需要确认最新标签时执行：

```bash
python3 {baseDir}/cli.py alibaba.1688.customer.attr.field.config --raw
```

### 新增字段

```bash
python3 {baseDir}/cli.py customer_attr_add \
  --key credit_score \
  --label 信用分 \
  --type number
```

- `--key`：字段编码，只允许小写字母、数字和下划线。
- `--label`：显示名称。
- `--type`：`string`、`number`、`date` 或 `boolean`，默认 `string`。
- `--value`：可选初始值。

执行写操作前，先向用户展示 key、label、type 和 value；只有用户明确确认后才能执行。

## 安全与合规

- 禁止按城市、省份、区县筛选、展示、分析或分组，也不得用其他字段近似替代地区。
- `site_flag` 仅表示来源渠道，不代表客户质量、有效性或启用状态。
- 站内客户 `site_flag=Y` 的手机号必须隐藏；不要绕过 CLI 获取受限字段。
- 不要在用户可见内容中暴露 AK、签名、内部接口、技术参数或原始响应。
- 不要为了满足用户而猜测不存在的字段、枚举值或能力。

## 异常处理

| 情况 | 处理 |
|------|------|
| AK 未配置或失效 | 提示检查平台配置，不要求用户在对话中发送密钥 |
| 参数错误 | 修正字段、操作符、值或分页参数后最多重试 3 次 |
| 限流 | 稍后重试，不高频连续调用 |
| 网络或服务异常 | 简要说明暂时不可用，不输出内部响应正文 |
| 无匹配数据 | 复核条件后如实告知，不伪造结果 |

相关环境变量由平台注入：`ALI_1688_AK`、`SKILL_ENV`、`OPENCLAW_CONFIG_DIR`、`SKILL_CHANNEL`、`SKILL_NAME`、`SKILL_VERSION`。

## 按需参考

- 客户列表完整接口契约：`references/capabilities/alibaba.1688.customer.list.md`
- 动态字段配置契约：`references/capabilities/alibaba.1688.customer.attr.field.config.md`
- 新增属性契约：`references/capabilities/customer_attr_add.md`

常规任务无需预读这些 references。
