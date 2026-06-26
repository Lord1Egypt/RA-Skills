# 腾讯云 CLS API 参考文档（OpenClaw）

本文档提供查询 OpenClaw 监控数据的详细 API 参考。

## 通用参数

所有 API 调用需要以下参数：

- **Region（地域）**: 腾讯云地域代码（如 `ap-guangzhou`、`ap-shanghai`、`ap-beijing`）
- **凭证**: 通过 TCCLI 凭证读取（执行 `tccli auth login` 获取临时密钥）

## 支持的地域

| 地域           | 地域简称         |
| -------------- | ---------------- |
| 北京           | ap-beijing       |
| 广州           | ap-guangzhou     |
| 上海           | ap-shanghai      |
| 成都           | ap-chengdu       |
| 南京           | ap-nanjing       |
| 重庆           | ap-chongqing     |
| 中国香港       | ap-hongkong      |
| 硅谷           | na-siliconvalley |
| 弗吉尼亚       | na-ashburn       |
| 新加坡         | ap-singapore     |
| 曼谷           | ap-bangkok       |
| 法兰克福       | eu-frankfurt     |
| 东京           | ap-tokyo         |
| 首尔           | ap-seoul         |
| 雅加达         | ap-jakarta       |
| 圣保罗         | sa-saopaulo      |
| 深圳金融       | ap-shenzhen-fsi  |
| 上海金融       | ap-shanghai-fsi  |
| 北京金融       | ap-beijing-fsi   |
| 上海自动驾驶云 | ap-shanghai-adc  |

## API: DescribeTopics（获取主题列表）

获取日志或指标主题列表。

### 请求参数

| 参数名        | 是否必须 | 类型            | 说明                                                                      |
| ------------- | -------- | --------------- | ------------------------------------------------------------------------- |
| Filters.N     | 否       | Array of Filter | 过滤条件                                                                  |
| Offset        | 否       | Integer         | 分页偏移量（默认: 0）                                                     |
| Limit         | 否       | Integer         | 分页大小（默认: 20，最大: 100）                                           |
| PreciseSearch | 否       | Integer         | 0: 模糊匹配，1: topicName 精确匹配，2: logsetName 精确匹配，3: 都精确匹配 |
| BizType       | 否       | Integer         | 0: 日志主题（默认），1: 指标主题                                          |

### OpenClaw 过滤条件

获取 OpenClaw 主题时，使用以下过滤条件：

```json
{
  "Filters": [
    {
      "Key": "assumerName",
      "Values": ["OpenClaw"]
    }
  ]
}
```

### 响应字段

| 字段名     | 类型    | 说明         |
| ---------- | ------- | ------------ |
| Topics     | Array   | 主题信息列表 |
| TotalCount | Integer | 主题总数     |

#### Topic 对象

| 字段名      | 类型    | 说明                                         |
| ----------- | ------- | -------------------------------------------- |
| TopicId     | String  | 主题 ID                                      |
| TopicName   | String  | 主题名称                                     |
| LogsetId    | String  | 日志集 ID                                    |
| LogsetName  | String  | 日志集名称                                   |
| Partition   | Integer | 分区数量                                     |
| StorageType | String  | 存储类型: hot（标准存储）或 cold（低频存储） |
| Period      | Integer | 保存天数                                     |
| CreateTime  | String  | 创建时间                                     |

## API: SearchLog（检索分析日志）

搜索和分析日志。

### 请求参数

| 参数名       | 是否必须 | 类型    | 说明                                         |
| ------------ | -------- | ------- | -------------------------------------------- |
| TopicId      | 是*      | String  | 日志主题 ID（*或使用 Topics）                |
| Query        | 是       | String  | 搜索查询语句（CQL 或 Lucene 语法）           |
| From         | 是       | Integer | 开始时间（Unix 毫秒时间戳）                  |
| To           | 是       | Integer | 结束时间（Unix 毫秒时间戳）                  |
| SyntaxRule   | 否       | Integer | 0: Lucene 语法，1: CQL 语法（推荐）          |
| Sort         | 否       | String  | 排序方式: asc 升序或 desc 降序（默认: desc） |
| Limit        | 否       | Integer | 最大返回条数（默认: 100，最大: 1000）        |
| Offset       | 否       | Integer | 分页偏移量                                   |
| Context      | 否       | String  | 上次响应返回的分页上下文                     |
| SamplingRate | 否       | Float   | 分析采样率（0-1）                            |

### 查询语法（CQL）

CQL（CLS Query Language）是推荐的查询语法。

#### 基础搜索

- `*` - 匹配所有日志
- `fieldName:value` - 字段等于某值
- `fieldName:(value1 OR value2)` - 字段等于其中任一值
- `NOT fieldName:value` - 字段不等于某值
- `fieldName>100` - 数值比较

#### 分析语句（SQL）

使用管道符 `|` 分隔搜索条件和 SQL 分析语句：

```sql
-- 统计日志总数
* | SELECT count(*) as total

-- 统计成功请求数
status:200 | SELECT count(*) as success_count

-- 按状态码分组统计
* | SELECT status, count(*) as cnt GROUP BY status

-- 按时间统计趋势
* | SELECT histogram(cast(__TIMESTAMP__ as timestamp), interval 1 minute) as time, count(*) GROUP BY time ORDER BY time
```

### 响应字段

| 字段名          | 类型    | 说明                 |
| --------------- | ------- | -------------------- |
| Results         | Array   | 日志搜索结果         |
| AnalysisResults | Array   | SQL 分析结果         |
| Context         | String  | 分页上下文           |
| Analysis        | Boolean | 响应是否包含分析结果 |
| ColNames        | Array   | 分析结果的列名       |
| SamplingRate    | Float   | 实际使用的采样率     |

## API: ChatCompletions（生成查询建议）

使用 AI（text2sql 模型）生成查询建议。

### 请求参数

| 参数名   | 是否必须 | 类型    | 说明              |
| -------- | -------- | ------- | ----------------- |
| Model    | 是       | String  | 必须为 "text2sql" |
| Messages | 是       | Array   | 对话消息列表      |
| Stream   | 否       | Boolean | 是否流式响应      |
| Metadata | 是       | Array   | 主题元数据        |

### Message 对象

| 字段名  | 类型   | 说明                  |
| ------- | ------ | --------------------- |
| Role    | String | "user" 或 "assistant" |
| Content | String | 消息内容              |

### Metadata 对象

| Key          | Value       |
| ------------ | ----------- |
| topic_id     | 日志主题 ID |
| topic_region | 地域代码    |

### 请求示例

```json
{
  "Model": "text2sql",
  "Messages": [
    {
      "Content": "如何统计日志条数变化趋势？",
      "Role": "user"
    }
  ],
  "Stream": false,
  "Metadata": [
    {"Key": "topic_id", "Value": "your-topic-id"},
    {"Key": "topic_region", "Value": "ap-guangzhou"}
  ]
}
```

## API: DescribeTemplates（获取仪表盘模板）

获取预置的仪表盘模板。

### 请求参数

| 参数名    | 是否必须 | 类型            | 说明     |
| --------- | -------- | --------------- | -------- |
| Filters.N | 否       | Array of Filter | 过滤条件 |

### OpenClaw 仪表盘过滤条件

```json
{
  "Filters": [
    {
      "Key": "ResourceType",
      "Values": ["DASHBOARD"]
    }
  ]
}
```

从返回结果中筛选 `SubType == "CLS_Openclaw"` 即可获取 OpenClaw 专用仪表盘。

## Prometheus API（指标主题查询）

指标主题可通过兼容 Prometheus 的 API 进行查询。

### 基础 URL

```
https://{地域}.cls.tencentcs.com/prometheus/{主题ID}
```

### 认证方式

Basic Auth 认证：

- 用户名: `TENCENTCLOUD_SECRET_ID`
- 密码: `TENCENTCLOUD_SECRET_KEY`

### 元数据 API（探索指标和标签）

在不确定有哪些指标或标签时，应先使用元数据 API 进行探索。

#### 列出所有标签名称

```
GET /api/v1/labels
```

返回所有可用的标签名称列表。

**脚本调用：**

```bash
python3 scripts/prometheus_query.py --region <地域> --topic-id <主题ID> \
    --list-labels
```

#### 列出指定标签的所有值

```
GET /api/v1/label/{标签名}/values
```

返回指定标签的所有可能值。

**常用示例：**

```bash
# 获取所有指标名称（__name__ 是特殊标签，存储指标名）
python3 scripts/prometheus_query.py --region <地域> --topic-id <主题ID> \
    --label-values __name__

# 获取所有渠道
python3 scripts/prometheus_query.py --region <地域> --topic-id <主题ID> \
    --label-values openclaw_channel

# 获取所有模型
python3 scripts/prometheus_query.py --region <地域> --topic-id <主题ID> \
    --label-values openclaw_model

# 获取所有供应商
python3 scripts/prometheus_query.py --region <地域> --topic-id <主题ID> \
    --label-values openclaw_provider

# 获取所有主机名
python3 scripts/prometheus_query.py --region <地域> --topic-id <主题ID> \
    --label-values hostname
```

#### 列出时间序列

```
GET /api/v1/series
```

参数：

- `match[]`: 序列选择器（支持正则匹配）
- `start`: 开始时间戳（可选）
- `end`: 结束时间戳（可选）

**常用示例：**

```bash
# 列出所有 openclaw 开头的指标
python3 scripts/prometheus_query.py --region <地域> --topic-id <主题ID> \
    --query "{__name__=~\"openclaw.*\"}" --list-series

# 列出所有系统指标
python3 scripts/prometheus_query.py --region <地域> --topic-id <主题ID> \
    --query "{__name__=~\"system.*\"}" --list-series

# 列出特定指标的所有时间序列（包含所有标签组合）
python3 scripts/prometheus_query.py --region <地域> --topic-id <主题ID> \
    --query "openclaw_message_processed_total" --list-series
```

### 数据查询 API

#### 即时查询

```
GET /api/v1/query
```

参数：

- `query`: PromQL 表达式
- `time`: 查询时间点（可选，默认为当前时间）

**脚本调用：**

```bash
python3 scripts/prometheus_query.py --region <地域> --topic-id <主题ID> \
    --query "<PromQL>" --instant
```

#### 范围查询

```
GET /api/v1/query_range
```

参数：

- `query`: PromQL 表达式
- `start`: 开始时间戳
- `end`: 结束时间戳
- `step`: 查询步长

**脚本调用：**

```bash
# 使用绝对时间
python3 scripts/prometheus_query.py --region <地域> --topic-id <主题ID> \
    --query "<PromQL>" --start <开始时间> --end <结束时间> --step 1m

# 使用相对时间
python3 scripts/prometheus_query.py --region <地域> --topic-id <主题ID> \
    --query "<PromQL>" --start-relative 1h --step 1m
```

## 错误处理

### 常见错误码

| 错误码           | 说明         | 解决方案           |
| ---------------- | ------------ | ------------------ |
| AuthFailure      | 认证失败     | 检查凭证是否正确   |
| InvalidParameter | 参数无效     | 检查参数格式       |
| ResourceNotFound | 主题不存在   | 验证主题 ID 和地域 |
| LimitExceeded    | 超过频率限制 | 降低请求频率       |
| InternalError    | 内部错误     | 稍后重试           |

### HTTP 状态码（Prometheus API）

| 状态码 | 说明                     |
| ------ | ------------------------ |
| 200    | 成功                     |
| 400    | 请求错误（查询语句无效） |
| 401    | 未授权                   |
| 422    | 无法处理的实体           |
| 503    | 服务不可用               |
