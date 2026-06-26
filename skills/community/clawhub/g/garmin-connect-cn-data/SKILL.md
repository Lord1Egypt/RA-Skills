---
name: garmin-cn
description: >
  查询 Garmin Connect CN（佳明中国）的个人健康与运动数据。只要用户提到
  Garmin/佳明、询问跑步配速/睡眠质量/HRV/Body Battery/VO2 Max/训练状态等
  任何健康指标，或想导出 FIT/GPX/TCX 文件、分析某次活动的分段数据，都应
  优先激活此技能——即使用户没有明说"查 Garmin"或"用佳明"。
---

# garmin-cn — 佳明中国数据查询技能

连接 Garmin Connect CN（佳明中国，connect.garmin.cn），查询个人健康与运动数据。

## 阅读说明（给任何读取本文档的模型或 Agent）

无论你是 Claude Code、其他 LLM、还是自动化 Agent，读完本文档后需要完成三件事：

1. **确定 SKILL_DIR**（本技能脚本所在目录的绝对路径）
2. **确定 RUNNER**（运行 `garmin_cli.py` 的命令前缀）
3. **按需调用命令**（见"命令详解"节）

**关于"用户/调用方"**：文中"用户"指向你发出请求的一方，可能是人类，也可能是上层 Agent 或自动化流程。相关描述同样适用于 Agent 间调用场景。

**如果你没有 Shell 执行权限**（纯 API 环境、沙箱、只读上下文），跳到"环境准备"节末尾的"无 Shell 执行权限"段落。

---

## 适用场景

当用户的请求涉及以下任意内容时，激活此技能：

- 查看佳明 / Garmin 数据、运动记录、活动记录（跑步、骑行、游泳等）
- 查询指定日期或日期范围的睡眠、HRV、静息心率、心率数据
- 查询压力水平、Body Battery、血氧（SpO2）、呼吸率
- 查询训练状态、训练负荷、训练准备度、VO2 Max
- 查询步数、卡路里、运动距离
- 导出或下载运动数据文件（FIT、GPX、TCX、CSV）
- 查看某次活动的详细分段、配速、心率分区、跑步分析

---

## 环境准备（每次任务开始前执行一次）

在执行任何数据查询命令前，先完成以下两步，确定本次任务使用的 **SKILL_DIR** 和 **RUNNER**。
确定后全程不重新检测——如某条命令失败，先检查参数或登录状态，而非切换 RUNNER。

### 第一步：确定 SKILL_DIR

SKILL_DIR 是包含 `scripts/garmin_cli.py` 的目录绝对路径。按以下策略依次尝试，找到即停止：

**策略 1（Claude Code 技能注入）**
技能系统会在上下文中注入完整路径，直接使用。

**策略 2（从上下文提取文件路径）**
如果你的上下文中包含本文档的路径（如 `/some/path/garmin-cn/SKILL.md`），则：
```
SKILL_DIR = 该路径去掉末尾的 /SKILL.md
```

**策略 3（搜索文件系统）**
```bash
find ~ -maxdepth 8 -name "garmin_cli.py" -path "*/garmin-cn/*" 2>/dev/null | head -1 | xargs -I{} dirname {}
```

**策略 4（当前工作目录）**
```bash
test -f "$(pwd)/scripts/garmin_cli.py" && echo "$(pwd)"
```

找到候选路径后，验证有效性：
```bash
test -f <SKILL_DIR>/scripts/garmin_cli.py && echo "confirmed"
```

后续所有命令中的 `<SKILL_DIR>` 均替换为此绝对路径。

### 第二步：检测 RUNNER

按优先级依次尝试，**找到第一个可用方式后停止**，本次任务全程使用该方式。

#### 方式 A（首选）：uv + project 模式

```bash
uv run --project <SKILL_DIR>/scripts <SKILL_DIR>/scripts/garmin_cli.py status
```

输出 JSON 含 `"status"` 字段 → 使用方式 A。后续命令格式：

```
uv run --project <SKILL_DIR>/scripts <SKILL_DIR>/scripts/garmin_cli.py <命令> [参数]
```

#### 方式 B（备选）：uv + 内联依赖

```bash
uv run --python 3.11 --with garminconnect <SKILL_DIR>/scripts/garmin_cli.py status
```

输出 JSON 含 `"status"` 字段 → 使用方式 B。后续命令格式：

```
uv run --python 3.11 --with garminconnect <SKILL_DIR>/scripts/garmin_cli.py <命令> [参数]
```

#### 方式 C（无 uv）：系统 Python

```bash
# 1. 确认可用的 python（优先 python3，否则 python）
python3 --version 2>/dev/null || python --version

# 2. 安装依赖（已安装则跳过）
python3 -m pip install -q garminconnect

# 3. 验证
python3 <SKILL_DIR>/scripts/garmin_cli.py status
```

输出 JSON 含 `"status"` 字段 → 使用方式 C。后续命令格式（以 `python3` 为例）：

```
python3 <SKILL_DIR>/scripts/garmin_cli.py <命令> [参数]
```

#### 均不可用时

向调用方报告：「当前环境缺少 Python 运行时，无法执行 Garmin 数据查询。请安装 uv（推荐）或 Python 3.9+。」

### 无 Shell 执行权限

如果你所在的环境无法直接执行 Shell 命令（纯 API 调用、沙箱、只读上下文），采用以下方式：

1. 将需要执行的命令告知调用方，请其运行并返回输出
2. 根据输出判断 RUNNER 类型，继续后续步骤
3. 如需多步执行，每次提供下一条命令并等待返回结果

示例交互：
> 「我需要确认你的运行环境，请执行以下命令并把输出粘贴给我：`uv --version`」
> 「请执行：`python3 --version`」
> 「请执行：`python3 <SKILL_DIR>/scripts/garmin_cli.py status`，把完整 JSON 输出给我。」

### FIT_RUNNER（仅在使用 fit-parse 命令时检测）

fit-parse 依赖 `fitparse`，与主脚本独立检测：

| 优先级 | 方式 | 命令 |
|--------|------|------|
| A | uv + 内联 fitparse | `uv run --python 3.11 --with fitparse python <SKILL_DIR>/scripts/fit_file_parser.py --help` |
| B | 系统 Python | `python3 -m pip install -q fitparse && python3 <SKILL_DIR>/scripts/fit_file_parser.py --help` |

确定后，fit-parse 命令格式（方式 A 示例）：

```
uv run --python 3.11 --with fitparse python <SKILL_DIR>/scripts/fit_file_parser.py <参数>
```

---

## 初始设置（仅需一次）

用户需先登录佳明中国账号：

```
<RUNNER> login <邮箱> <密码>
```

凭据保存在 `~/.config/garmin-cn/credentials.json`（权限 600，仅本人可读）。

---

## 命令详解

以下所有命令均使用"环境准备"节确定的 `<RUNNER>` 前缀。

### login — 登录佳明中国

```
<RUNNER> login <邮箱> <密码>
```

连接 connect.garmin.cn（中国区），登录成功后保存凭据供后续命令使用。登录前会自动清除旧的 SSO 缓存以避免 401 错误。

### status — 检查登录状态

```
<RUNNER> status
```

验证当前凭据是否有效，返回登录状态和区域信息。

### summary — 每日综合健康摘要

```
<RUNNER> summary [--date YYYY-MM-DD]
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--date` | 指定日期 | 今天 |

返回指定日期的综合健康数据，包含：
- 步数、距离（km）、卡路里
- 心率（静息心率、最高心率）
- Body Battery（最高值、最低值、当前值）
- 压力水平（平均值、等级）
- 睡眠（总时长、深睡/浅睡/REM/清醒时长、睡眠评分、HRV、HRV 状态）
- VO2 Max
- 训练状态（状态标签、运动类型、起始日期）
- 训练负荷（急性/慢性负荷、ACWR 比率、状态）
- 训练准备度（评分、等级、恢复时间）
- 本周强度分钟（中等/剧烈、目标）
- 最后同步时间

### activities — 查询活动列表

```
<RUNNER> activities [--start YYYY-MM-DD] [--end YYYY-MM-DD] [--days N] [--type 类型]
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--start` | 起始日期（指定后 `--days` 被忽略） | 根据 `--days` 计算 |
| `--end` | 结束日期 | 今天 |
| `--days` | 最近天数 | 7 |
| `--type` | 活动类型筛选 | 全部类型 |

活动类型可选值：`running`、`treadmill_running`、`cycling`、`swimming`、`walking`、`hiking`、`strength_training` 等。

每条活动记录包含：`activity_id`（用于 detail/run/export 命令）、名称、类型、日期时间、距离、时长、配速、平均/最高心率、卡路里、速度、爬升、有氧/无氧训练效果。

### detail — 活动详细数据

```
<RUNNER> detail <activity_id>
```

适用于所有活动类型，返回完整的活动数据：
- 基本信息：距离、时长、配速/速度、心率、卡路里、功率、步频/踏频、爬升/下降
- 训练效果：有氧 TE、无氧 TE、训练负荷、VO2 Max
- 分段/圈数：每圈的距离、时长、配速、心率、功率、步频、爬升
- 心率分区：各心率区间时间分布
- 天气：温度、天气状况、湿度、风速、风向
- 装备：使用的装备名称和 UUID

`activity_id` 可从 `activities` 命令的输出中获取。

### run — 跑步专项分析

```
<RUNNER> run [activity_id]
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `activity_id` | 活动 ID（可选） | 最近 30 天内的最新一次跑步；若 30 天内无跑步记录，返回空数组并附提示信息 |

返回跑步活动的专项数据：
- 总体：距离、时长、配速、心率、功率、步频、爬升、训练效果、VO2 Max、训练负荷
- 分圈数据：每公里的配速、心率、功率、步频、爬升
- 近期对比：最近 5 次跑步的距离、配速、心率、训练效果、VO2 Max

### sleep — 睡眠数据查询

```
<RUNNER> sleep [--start YYYY-MM-DD] [--end YYYY-MM-DD] [--days N]
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--start` | 起始日期 | 根据 `--days` 计算 |
| `--end` | 结束日期 | 今天 |
| `--days` | 最近天数 | 7 |

返回指定日期范围内每天的睡眠记录：
- 睡眠时长（总时长、深睡、浅睡、REM、清醒）
- 睡眠评分
- 静息心率
- 夜间 HRV（平均值、周平均、5 分钟最高值、HRV 状态）
- Body Battery（最高值、最低值）

附带日期范围内的汇总统计（睡眠评分均值、HRV 均值、Body Battery 均值、静息心率均值）。

### health — 健康指标查询

```
<RUNNER> health [--start YYYY-MM-DD] [--end YYYY-MM-DD] [--days N] [--metrics 指标列表]
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--start` | 起始日期 | 根据 `--days` 计算 |
| `--end` | 结束日期 | 今天 |
| `--days` | 最近天数 | 7 |
| `--metrics` | 逗号分隔的指标代码 | 全部指标 |

可选指标代码：

| 代码 | 指标 | 返回数据 |
|------|------|----------|
| `hrv` | 心率变异性 | 周平均、昨夜平均、昨夜 5 分钟最高值、状态（BALANCED/LOW/等）、基线范围 |
| `rhr` | 静息心率 | 当日静息心率值 |
| `stress` | 全天压力 | 总体压力等级、休息/活动/低/中/高压力时长 |
| `bb` | Body Battery | 充电量、消耗量、最高值、最低值 |
| `spo2` | 血氧饱和度 | 平均值、最低值、最新值 |
| `respiration` | 呼吸率 | 清醒平均、睡眠平均、最高值、最低值 |

用法示例：`--metrics hrv,rhr,stress`（仅查询这三项）。不指定则查询全部 6 项。

返回每天一条记录，附带日期范围内的汇总统计（均值、最小值、最大值）。

### export — 导出活动数据文件

```
<RUNNER> export <activity_id> [--format 格式] [--output 目录]
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `activity_id` | 活动 ID（必填） | — |
| `--format` | 导出格式：`fit`、`gpx`、`tcx`、`csv` | `fit` |
| `--output` | 输出目录路径 | `.`（当前目录） |

- `fit`：原始 FIT 文件（从 Garmin 返回的 zip 中自动解压）
- `gpx`：GPS 交换格式，包含轨迹点、心率、海拔等
- `tcx`：Training Center XML 格式
- `csv`：分段数据的 CSV 格式

导出成功后返回文件的绝对路径和文件大小（字节）。

### fit-parse — 解析 FIT 文件

使用 Python SDK `fitparse` 解析 FIT 文件，输出标准化 JSON（含 FIT 头信息、消息统计、HR/步频/步幅可得性、公里抽样）。

使用前请先完成"环境准备"节的 **FIT_RUNNER** 检测。

```
<FIT_RUNNER> <SKILL_DIR>/scripts/fit_file_parser.py <fit_file_path> [参数...]
```

#### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--targets` | 公里抽样点，逗号分隔（如 `1,5,10,last`） | `1,5,10,last` |
| `--max-messages` | 最多扫描的 FIT 消息数（超大文件保护） | `500000` |
| `--output` | 输出 JSON 文件路径（不指定则打印到 stdout） | 无 |
| `--pretty` | 美化 JSON 输出 | 关闭 |
| `--strict` | 若 HR 或步频不可用则返回错误码 | 关闭 |

#### 输出字段（成功）

- `status`: `success`
- `fit_header`: FIT 头信息（协议版本、profile、data_size、magic 校验）
- `parse.message_counts`: 各消息类型计数（如 `record`、`lap`）
- `parse.metrics`: 指标可得性（`hr` / `cadence` / `stride`）
  - `direct`：原生字段直接可得
  - `estimated`：由距离 + 时长 + 步频估算
  - `unavailable`：不可得
- `km_samples`: 公里抽样结果（默认 `km_1`、`km_5`、`km_10`、`km_last`）

#### 退出码

- `0`: 成功
- `1`: 解析失败或 strict 校验失败
- `2`: 参数错误、输入文件缺失、依赖不可用

---

## 端到端批量测试

需要进行长周期数据查询、批量导出或赛事分析时，参见：
`references/advanced-usage.md`

该文件包含完整的目录结构、命令序列和结果判读口径。
使用前请先完成本文档"环境准备"节的 RUNNER 检测，模板中的 `<RUNNER>` 已与本文档保持一致。

---

## 使用示例

> 执行前请先完成"环境准备"节，确定 SKILL_DIR 和 RUNNER。

查询指定日期范围的活动：
```
<RUNNER> activities --start 2026-02-01 --end 2026-02-28
```

查询最近 3 天的跑步活动：
```
<RUNNER> activities --days 3 --type running
```

查询 7 天的 HRV 和静息心率趋势：
```
<RUNNER> health --days 7 --metrics hrv,rhr
```

查询指定一周的睡眠数据：
```
<RUNNER> sleep --start 2026-02-24 --end 2026-03-02
```

导出活动为 GPX 文件：
```
<RUNNER> export 12345678 --format gpx
```

查看过去某一天的综合摘要：
```
<RUNNER> summary --date 2026-02-15
```

查看某次活动的完整详情（先获取 activity_id）：
```
<RUNNER> activities --days 1
<RUNNER> detail <从上面获取的 activity_id>
```

解析 FIT 文件并输出详细 JSON：
```
<FIT_RUNNER> <SKILL_DIR>/scripts/fit_file_parser.py /path/to/activity.fit --pretty
```

解析 FIT 文件并写入结果文件（自定义公里抽样）：
```
<FIT_RUNNER> <SKILL_DIR>/scripts/fit_file_parser.py /path/to/activity.fit --targets 1,3,5,10,last --output /tmp/fit_parse_result.json --pretty
```

---

## 输出格式

所有命令输出标准化 JSON：

成功时：
```json
{
  "status": "success",
  "command": "命令名",
  "data": { "...": "..." },
  "warnings": ["部分子查询失败的提示（可选）"]
}
```

失败时：
```json
{
  "status": "error",
  "command": "命令名",
  "message": "错误描述"
}
```

关键约定：
- `warnings` 数组仅在部分子查询失败但整体结果可用时出现，不影响主数据
- 查询结果为空时返回 `"data": []` 并附带描述性 `"message"`（如"范围内无活动"）
- 日期格式错误、无效参数等会立即返回错误，并提示正确格式
- 所有日期参数格式为 `YYYY-MM-DD`
- 当 `--start` 与 `--days` 同时指定时，`--start` 优先，`--days` 被忽略
