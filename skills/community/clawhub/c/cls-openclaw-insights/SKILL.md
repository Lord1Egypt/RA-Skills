---
name: cls-openclaw-insights
version: 1.0.0
description: |
  分析存储在腾讯云日志服务 (CLS) 中的 OpenClaw 监控数据。
  当用户需要查询、分析 OpenClaw 相关问题时，应使用此 skill，包括但不限于：
  - 成本分析：Token 消耗统计、费用趋势、模型调用成本对比
  - 性能问题：会话卡死、队列积压、响应延迟
  - 运行异常：Gateway 状态、Webhook 报错、实例异常
  - 行为审计：Agent 调用记录、工具使用情况、会话详情
  触发关键词包括 "OpenClaw监控"、"OpenClaw分析"、"OpenClaw日志"、"OpenClaw指标"、"OpenClaw成本"、
  "Token消耗"、"会话卡死"、"实例异常"、"OpenClaw报错"，或任何涉及 OpenClaw 监控数据分析的请求。
---
# OpenClaw 监控数据分析 Skill

此 skill 提供用于分析存储在腾讯云日志服务 (CLS) 中的 OpenClaw 监控数据的工具和工作流，
帮助用户排查成本、性能、异常等问题。

## 系统要求

- **Python**: >= 3.7
- **依赖安装**:
  ```bash
  pip install -r {SKILL_BASE}/requirements.txt
  ```

> **关于 `{SKILL_BASE}`**：文档中所有 `{SKILL_BASE}` 占位符会被 Skill 框架自动替换为此 skill 的实际安装目录路径，无需手动修改。

## 概述

OpenClaw 监控数据存储在腾讯云 CLS 中，包含两种类型的主题：

### 日志主题

存储 OpenClaw 运行日志，通过腾讯云 API 查询。包含以下数据：

| 日志类型         | 原始日志路径                              | 分析场景                                       |
| ---------------- | ----------------------------------------- | ---------------------------------------------- |
| Session 审计日志 | `~/.openclaw/agents/*/sessions/*.jsonl` | Agent 做了什么？调了什么工具？花了多少 Token？ |
| 应用运行日志     | `/tmp/openclaw/openclaw-YYYY-MM-DD.log` | Gateway 正不正常？Webhook 报错了吗？           |

### 指标主题

存储 OpenClaw 遥测指标，通过 Prometheus API 查询。包含以下数据：

| 指标类型      | 采集方式                               | 分析场景                             |
| ------------- | -------------------------------------- | ------------------------------------ |
| OTEL 遥测指标 | `openclaw diagnostics-otel` 插件采集 | Token 消耗趋势？队列积压？会话卡死？ |

### 综合分析

成本、性能等问题在日志及指标中均有相关的监控数据，需综合两部分数据进行问题分析。

## 前置条件（安装引导）

使用此 skill 需要腾讯云临时密钥。**在执行任何操作之前，必须先检查 TCCLI 是否已安装并完成授权，引导用户完成配置。**

### 凭证检查

使用专用脚本检测 TCCLI 安装状态和密钥配置：

```bash
python3 {SKILL_BASE}/scripts/check_credentials.py
```

根据检查结果（退出码）采取对应操作：

| 退出码 | 含义                | 操作                             |
| ------ | ------------------- | -------------------------------- |
| 0      | ✅ 凭证已配置且有效 | 直接进入工作流程                 |
| 1      | ❌ TCCLI 未安装     | 引导安装 TCCLI（见下方步骤 1）   |
| 2      | ❌ 凭证文件不存在   | 引导授权登录（见下方步骤 2）     |
| 3      | ❌ 凭证文件格式错误 | 引导重新授权登录（见下方步骤 2） |
| 4      | ❌ 临时密钥已过期   | 引导重新授权登录（见下方步骤 2） |

### 步骤 1: 安装 TCCLI

如果 TCCLI 未安装，执行以下命令安装：

```bash
pip install tccli
```

> 安装完成后可通过 `tccli --version` 验证是否安装成功。

### 步骤 2: 授权登录获取临时密钥

执行以下命令，TCCLI 会自动打开浏览器进行腾讯云账号授权：

```bash
tccli auth login
```

注意：通过对话方式与Agent进行交互时，Agent直接执行上述命令，无需用户自己执行

**授权流程：**

1. 执行命令后，浏览器会自动打开腾讯云登录页面
2. 用户在浏览器中登录腾讯云账号并确认授权
3. 授权成功后，命令行会显示「登录成功, 密钥凭证已被写入」
4. 临时密钥会自动保存到本地

> **如果浏览器未自动打开**，请复制命令行中打印的链接，手动在浏览器中打开完成登录。
>
> **如果运行在无浏览器的服务器上**，可使用 `tccli auth login --browser no`，然后在另一台有浏览器的机器上访问打印出的链接，完成授权后将验证码粘贴回终端。

## 工作流程

### 步骤 1: 获取 OpenClaw 实例信息

首先获取当前账号下启用了监控的 OpenClaw 实例列表，返回结果中的 `ServiceRegion` 即为监控数据保存的地域：

```bash
python3 {SKILL_BASE}/scripts/cls_api.py --action DescribeOpenClawApplications
```

> **说明**：`DescribeOpenClawApplications` 是全局接口，`--region` 参数不影响返回结果（脚本默认使用 `ap-guangzhou`，无需修改）。
>
> **注意**：后续步骤中的 `<地域>` 请使用此处返回的 `ServiceRegion` 值。

获取不到实例时，可能是用户未将 OpenClaw 监控数据接入 CLS，建议用户前往CLS应用中心（https://console.cloud.tencent.com/cls/cloud-product）进行接入。

### 步骤 2: 获取 OpenClaw 主题

使用 `scripts/cls_api.py` 脚本获取 OpenClaw 主题列表：

```bash
# 获取日志主题
python3 {SKILL_BASE}/scripts/cls_api.py --region <地域> --action DescribeTopics --biz-type 0

# 获取指标主题
python3 {SKILL_BASE}/scripts/cls_api.py --region <地域> --action DescribeTopics --biz-type 1
```

脚本会自动过滤 `assumerName=OpenClaw` 的主题。

获取不到主题时，可能是用户权限有问题，建议用户排查权限问题，是否有相关主题的查询权限。

### 步骤 3: 获取日志字段 Schema（推荐）

**⚠️ 重要：在构造查询语句前，建议先获取日志主题的索引字段信息，了解有哪些字段可用于查询和分析**

使用 `DescribeIndex` 接口获取日志主题的索引配置，包含所有已建索引的字段名、类型和分析能力：

```bash
python3 {SKILL_BASE}/scripts/cls_api.py --region <地域> --action DescribeIndex \
    --topic-id <日志主题ID>
```

返回结果中的关键信息：

- **`Rule.KeyValue.KeyValues`**: 键值索引字段列表，每个字段包含：
  - `Key`: 字段名（如 `message.model`、`message.usage.totalTokens`）
  - `Value.Type`: 字段类型（`text` 文本、`long` 整数、`double` 浮点数）
  - `Value.SqlFlag`: 是否开启 SQL 统计分析（`true`/`false`）
- **`Rule.Tag.KeyValues`**: 元数据（TAG）字段列表，通常包含 `__TAG__` 前缀的字段
- **`Rule.DynamicIndex.Status`**: 是否开启动态索引（`true` 表示新字段会自动建索引）

> **提示**：只有 `SqlFlag` 为 `true` 的字段才能在 SQL 分析语句（`| SELECT ...`）中使用。

### 步骤 4: 获取参考查询语句（推荐）

**⚠️ 重要：在执行分析前，建议先从仪表盘模板获取参考查询语句**

使用专用脚本获取 OpenClaw 仪表盘模板中的查询语句作为参考：

```bash
# 获取所有参考查询（分组显示）
# 注意：DescribeTemplates 是全局接口，--region 参数不影响结果（默认 ap-guangzhou）
python3 {SKILL_BASE}/scripts/get_dashboard_queries.py

# 只获取日志类型的查询（CQL/SQL）
python3 {SKILL_BASE}/scripts/get_dashboard_queries.py --type log

# 只获取指标类型的查询（PromQL）
python3 {SKILL_BASE}/scripts/get_dashboard_queries.py --type metric

# 输出 JSON 格式（便于程序处理）
python3 {SKILL_BASE}/scripts/get_dashboard_queries.py --format json
```

输出信息包含：

- **图表标题**: 代表查询的用途，可根据用户需求匹配相关查询
- **主题类型**: `log`（日志/CQL）或 `metric`（指标/PromQL）
- **查询语句**: 可直接使用或参考修改的查询语句

根据获取的参考查询，选择合适的语句执行数据分析。

### 步骤 5: 查询数据

#### 方式 A: 查询日志主题（通过 CLS API）

使用 `scripts/cls_api.py` 脚本搜索日志：

```bash
python3 {SKILL_BASE}/scripts/cls_api.py --region <地域> --action SearchLog \
    --topic-id <主题ID> \
    --query "<查询语句>" \
    --from-time <开始时间戳_毫秒> \
    --to-time <结束时间戳_毫秒> \
    --limit 100
```

参数说明：

- `--topic-id`: 步骤 2 获取的日志主题 ID
- `--query`: CQL 查询语句（使用 `*` 查询所有日志）
- `--from-time`: 开始时间，毫秒级 Unix 时间戳
- `--to-time`: 结束时间，毫秒级 Unix 时间戳
- `--limit`: 最大返回条数，仅当 Query 不包含SQL时有效，SQL结果的条数限制需使用SQL LIMIT语法（默认: 100，最大: 1000）
- `--sort`: 排序方式，`asc` 升序或 `desc` 降序（默认: desc）

#### 方式 B: 查询指标主题（通过 Prometheus API）

使用 `scripts/prometheus_query.py` 脚本查询指标数据。

**⚠️ 重要：如果不清楚有哪些指标或标签，请先查询元数据（见下方"元数据查询"部分）**

##### 元数据查询（探索可用指标和标签）

当不确定有哪些指标名称或标签时，应先通过元数据接口查询：

```bash
# 1. 获取所有指标名称（最常用）
python3 {SKILL_BASE}/scripts/prometheus_query.py --region <地域> --topic-id <指标主题ID> \
    --label-values __name__

# 2. 获取所有标签名称
python3 {SKILL_BASE}/scripts/prometheus_query.py --region <地域> --topic-id <指标主题ID> \
    --list-labels

# 3. 获取某个标签的所有值（如查看所有渠道）
python3 {SKILL_BASE}/scripts/prometheus_query.py --region <地域> --topic-id <指标主题ID> \
    --label-values openclaw_channel

# 4. 列出匹配某个模式的时间序列
python3 {SKILL_BASE}/scripts/prometheus_query.py --region <地域> --topic-id <指标主题ID> \
    --query "{__name__=~\"openclaw.*\"}" --list-series
```

##### 数据查询

确定指标名称后，执行数据查询：

```bash
# 范围查询（时间序列）
python3 {SKILL_BASE}/scripts/prometheus_query.py --region <地域> --topic-id <指标主题ID> \
    --query "<PromQL查询>" \
    --start <开始时间> \
    --end <结束时间> \
    --step <步长>
```

参数说明：

- `--region`: 腾讯云地域
- `--topic-id`: 步骤 2 获取的指标主题 ID
- `--query`: PromQL 查询语句
- `--start`: 开始时间（ISO 格式或 Unix 时间戳）
- `--end`: 结束时间（ISO 格式或 Unix 时间戳）
- `--step`: 查询步长（如 `15s`、`1m`、`5m`）

即时查询（单个时间点）：

```bash
python3 {SKILL_BASE}/scripts/prometheus_query.py --region <地域> --topic-id <指标主题ID> \
    --query "<PromQL查询>" \
    --instant
```

相对时间范围查询：

```bash
python3 {SKILL_BASE}/scripts/prometheus_query.py --region <地域> --topic-id <指标主题ID> \
    --query "<PromQL查询>" \
    --start-relative 1h \
    --step 1m
```

### 步骤 6: 生成查询建议（可选）

使用 AI 生成基于主题 schema 的查询建议：

```bash
python3 {SKILL_BASE}/scripts/cls_api.py --region <地域> --action ChatCompletions \
    --topic-id <主题ID> \
    --chat-question "如何统计日志条数变化趋势？"
```

## 时间范围辅助

将人类可读时间转换为毫秒时间戳：

- 使用 Python: `int(datetime.now().timestamp() * 1000)`
- 最近 1 小时: `--from-time $(python3 -c "import time; print(int((time.time()-3600)*1000))")`
- 最近 24 小时: `--from-time $(python3 -c "import time; print(int((time.time()-86400)*1000))")`
- 最近 7 天: `--from-time $(python3 -c "import time; print(int((time.time()-604800)*1000))")`

Prometheus 相对时间：

- 使用 `--start-relative` 参数，如 `1h`（1小时）、`24h`（24小时）、`7d`（7天）
