# alibaba.1688.customer.list

分页查询客户列表，支持多条件筛选、多字段排序。基于 OpenSearch 实现毫秒级检索。

## 前置条件

- AK 由框架通过环境变量 ALI_1688_AK 自动注入
- 使用固定字段时直接构造筛选条件；仅动态自定义属性需要先调用 `alibaba.1688.customer.attr.field.config`获取其他可用筛选维度

## 参数

| 参数 | CLI 选项 | 类型 | 必传 | 说明 |
|------|----------|------|------|------|
| filtersFile | `--filters-file` | 文件路径 | 否 | 筛选条件 JSON 文件路径（推荐；Windows 必须） |
| sortsFile | `--sorts-file` | 文件路径 | 否 | 排序规则 JSON 文件路径（推荐；Windows 必须） |
| filters | `--filters` | JSON数组 | 否 | 筛选条件列表（仅 Unix/macOS 兼容，推荐改用 `--filters-file`） |
| sorts | `--sorts` | JSON数组 | 否 | 排序规则列表（仅 Unix/macOS 兼容，推荐改用 `--sorts-file`） |
| pageNum | `--page-num` | int | 否 | 页码，从1开始，默认1 |
| pageSize | `--page-size` | int | 否 | 每页条数，默认20，最大100 |
| raw | `--raw` | flag | 否 | 输出当前页完整客户记录；默认仅输出 markdown 与分页元数据 |

`alibaba.1688.customer.list` 只支持上表 CLI 选项。禁止使用 `--items`、`--limit`、`--count` 等未定义参数；分页/条数请求统一使用 `--page-size`。

> ⚠️ **所有平台均推荐走 `--filters-file` / `--sorts-file` 文件入参**；Windows 环境下禁止直接传 JSON 字符串，避免 `>` / `<` 等字符被 cmd 解析为重定向符导致 `op` 丢失。

### filters 结构

```json
[{"field": "user_interest_level", "op": "=", "value": "高意愿"}]
```

- `field`：筛选字段名
- `op`：操作符，可选 `>` `<` `>=` `<=` `=` `like` `in` `not in`
- `value`：筛选值。`in`/`not in` 时传 JSON 数组字符串如 `["VIP","L3"]`

### sorts 结构

```json
[{"field": "last_inquiry_time", "order": "desc"}]
```

### 可排序字段

`last_inquiry_time`、`recent_30d_purchase_amount`、`gmt_create`、`pay_ord_amt_std_all`

### 可筛选字段

- 固定字段：`buyer_nick`、`site_flag`、`phone`、`follower`、`shop_ids`、`pay_ord_amt_std_all`、`recent_30d_purchase_amount`、`pay_ord_amt_1w`、`pay_mord_cnt_1w`、`recent_30d_activity_score`、`last_inquiry_time`、`gmt_create`
- 标签：`tags`（op=`in`，value=JSON数组字符串）
- 动态属性：直接使用 `alibaba.1688.customer.attr.field.config` 返回的 `attrKey`（不加 attr_ 前缀）

> 🚫 **地区信息禁用（合规要求）**：客户城市 / 省份 / 区县不可用于筛选，也不得在结果中透出。

### 业务状态规则

「询盘未转化」「询盘未下单」「有询盘但未下单」不是客户标签，禁止使用 `tags in ["询盘未转化"]` 或 `tags in ["询盘未下单"]` 近似。

- 近7天有询盘：`last_inquiry_time >= 当前日期 - 7天`
- 近7天新买家：`gmt_create >= 当前日期 - 7天`（带时间窗的新买家诉求统一用客户创建时间对比，不要用 30 天口径的 `procurement_mode_30d` 顶替；仅当用户明确说「30 天合作关系/新买家」时才用 `procurement_mode_30d`）
- 未下单/未转化：优先 `pay_mord_cnt_1w <= 0`，业务明确按金额判断时可用 `pay_ord_amt_1w <= 0`
- 默认排序：`last_inquiry_time desc`

### 业务语义映射（避免 LLM 猜测）

| 用户描述 | 对应字段 | 构造示例 |
|----------|----------|----------|
| L3 以上（不含 L3） | `tags` `in` | `{"field":"tags","op":"in","value":"[\"L4\",\"L5\",\"L6\"]"}` |
| L3 及以上（含 L3） | `tags` `in` | `{"field":"tags","op":"in","value":"[\"L3\",\"L4\",\"L5\",\"L6\"]"}` |
| 仅 L3 | `tags` `in` | `{"field":"tags","op":"in","value":"[\"L3\"]"}` |
| 中等意愿以上（含中等） | `user_interest_level` `in` | `{"field":"user_interest_level","op":"in","value":"[\"中意愿\",\"高意愿\"]"}` |
| 高意愿 | `user_interest_level` `in` | `{"field":"user_interest_level","op":"in","value":"[\"高意愿\"]"}` |
| 累计支付金额大于 1 万 | `pay_ord_amt_std_all` `>` | `{"field":"pay_ord_amt_std_all","op":">","value":"10000"}` |
| 近 30 天采购金额大于 1 万 | `recent_30d_purchase_amount` `>` | `{"field":"recent_30d_purchase_amount","op":">","value":"10000"}` |

推荐使用 `cli.py alibaba.1688.customer.list --filters-file` 方式传入筛选条件。

## 典型用法

```bash
# 推荐：所有平台都先把 JSON 写入文件，再用文件路径入参（Windows 必须）
python3 {baseDir}/cli.py alibaba.1688.customer.list \
  --filters-file /absolute/path/filters.json \
  --sorts-file /absolute/path/sorts.json \
  --page-size 20

# Windows 推荐：在同一条 python -c 内写文件并调用 CLI，完全避开 shell 引号/重定向解析
python -c "import json, os, subprocess, tempfile; d=os.environ.get('NEWTON_SCRATCH_DIR') or os.environ.get('TEMP') or tempfile.gettempdir(); os.makedirs(d, exist_ok=True); ff=os.path.join(d,'filters.json'); sf=os.path.join(d,'sorts.json'); json.dump([{'field':'user_interest_level','op':'=','value':'高意愿'},{'field':'tags','op':'in','value':'[\"VIP\"]'}], open(ff,'w',encoding='utf-8')); json.dump([{'field':'last_inquiry_time','order':'desc'}], open(sf,'w',encoding='utf-8')); print(ff); print(sf); subprocess.run(['python', r'{baseDir}/cli.py', 'alibaba.1688.customer.list', '--filters-file', ff, '--sorts-file', sf, '--page-size', '20'])"

# Unix / macOS 兼容：直接传 JSON 字符串（不推荐，复杂 JSON 仍建议走文件）
python3 {baseDir}/cli.py alibaba.1688.customer.list \
  --filters '[{"field":"user_interest_level","op":"=","value":"高意愿"},{"field":"tags","op":"in","value":"[\"VIP\"]"}]' \
  --sorts '[{"field":"last_inquiry_time","order":"desc"}]' \
  --page-size 20

# 翻页
python3 {baseDir}/cli.py alibaba.1688.customer.list --page-num 2 --page-size 20
```

> 文件内容示例 `filters.json`：
> ```json
> [{"field":"user_interest_level","op":"=","value":"高意愿"},{"field":"tags","op":"in","value":"[\"VIP\"]"}]
> ```

## 返回字段

> `--raw` 输出的客户字段名已统一为下划线 attrKey 风格，与 `alibaba.1688.customer.attr.field.config` 保持一致。

默认模式返回 `success`、`markdown` 和轻量分页元数据 `data`；`--raw` 模式不返回 `markdown`，客户记录位于 `data.items`。顶层的 `__state_update__`、`filters`、`sorts`、`action` 为框架内部状态字段。

| 字段 | 类型 | 说明 |
|------|------|------|
| data.recordCount | Integer | 匹配总记录数 |
| data.pageNo | Integer | 当前页码 |
| data.totalPage | Integer | 总页数 |
| data.items | Array | 当前页客户记录（仅 `--raw`） |
| data.items[].buyer_nick | String | 买家昵称 |
| data.items[].phone | String | 手机号（站内客户 site_flag=Y 时脱敏为 null） |
| data.items[].site_flag | String | 站内外标识（Y/N） |
| data.items[].tags | Array | 标签列表 |
| data.items[].recent_30d_purchase_amount | Number | 近30天成交金额 |
| data.items[].recent_30d_activity_score | String | 近30天活跃度 |
| data.items[].last_inquiry_time | String | 最近询盘时间 |
| data.items[].follower | String | 跟进人 |
| data.items[].shop_ids | Array | 归属店铺 |
| data.items[].gmt_create | Long | 客户创建时间（时间戳） |
| data.items[].extraAttrs | Map | 动态扩展属性（键均为下划线 attrKey） |

## 操作符对照

| op | 含义 | 示例 |
|----|------|------|
| `=` | 精确匹配 | `{"field":"site_flag","op":"=","value":"Y"}` |
| `>` `<` `>=` `<=` | 数值比较 | `{"field":"recent_30d_purchase_amount","op":">","value":"10000"}` |
| `like` | 模糊匹配 | `{"field":"buyer_nick","op":"like","value":"科技"}` |
| `in` | 包含任一 | `{"field":"tags","op":"in","value":"[\"VIP\",\"L3\"]"}` |
| `not in` | 不包含 | `{"field":"tags","op":"not in","value":"[\"黑名单\"]"}` |
