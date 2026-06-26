---
name: fault-handling
description: 当用户需要故障处理、远程主机执行脚本、服务重启、磁盘清理等运维操作时使用。通过 run-script API 执行脚本，并轮询 execution-history 获取执行结果。
---

# 故障处理 Skill

## Overview

用纯 Python 流程完成一次故障处理操作：

1. 根据用户提供的主机 IP（或从告警上下文获取）构建执行参数
2. 调用 `run-script` API 执行脚本
3. 轮询 `execution-history` API 等待执行完成
4. 输出执行结果报告

## Files

- 主入口: `skills/fault-handling/run_script.py`（完全独立，内置签名、请求等工具函数）
- 配置文件: `skills/fault-handling/.env`

## Default Workflow

用户说"故障处理""执行脚本""重启服务""重启 nginx"时，按以下顺序执行：

### 1. 确认执行参数

必须确认以下信息后才能执行：

- **主机 IP**（`ansible_host`）：从用户提供的 IP、告警上下文、或对话历史中获取。必须至少有一个主机 IP。
- **脚本**：默认使用预置脚本 `服务重启-nginx服务重启（场景演示）`（script_id=187）。用户可指定其他脚本 ID 或脚本内容。
- **organize**（主机所属组织）：可选，默认为空字符串。

如果缺少主机 IP，必须询问用户。

### 2. 执行脚本

运行：

```bash
python3 skills/fault-handling/run_script.py \
  --hosts '192.168.3.76' \
  --script-id 187
```

多主机用逗号分隔：

```bash
python3 skills/fault-handling/run_script.py \
  --hosts '192.168.3.76,192.168.3.75' \
  --script-id 187
```

也可以直接传脚本内容代替脚本 ID：

```bash
python3 skills/fault-handling/run_script.py \
  --hosts '192.168.3.76' \
  --script-type 1 \
  --script-content 'systemctl restart nginx'
```

### 3. 等待执行完成

脚本内部会：
1. 调用 `run-script` API 提交任务，获取 `execution_id`
2. 每 3 秒轮询 `execution-history` API 检查任务状态
3. 任务完成后（`is_running=false`）输出 JSON 结果

### 4. 输出结果

脚本输出 JSON 格式的执行结果，包含：
- `execution_id`: 任务 ID
- `task_name`: 任务名称
- `status`: 执行状态（1=成功，2=失败，3=部分成功，4=正在执行）
- `status_label`: 状态中文标签
- `consuming`: 耗时（秒）
- `steps`: 每个步骤的详细输出，包含每台主机的 stdout 和执行状态

### 5. 向用户汇报

基于执行结果，在回复中给出：

```text
🔧 故障处理执行报告
任务名称：{task_name}
任务ID：{execution_id}
执行状态：{status_label}
执行耗时：{consuming}秒

📋 步骤执行详情
步骤    主机IP    主机名    状态    输出
{step_name}    {ansible_host}    {host_name}    {status}    {stdout}

📌 执行结论
● ✅ {成功数}台主机执行成功
● ❌ {失败数}台主机执行失败
```

## API Reference

### run-script（执行脚本）

- URL: `/api/v6/devops/run-script`
- Method: POST
- 参数通过 `data` 字段传递 JSON 字符串

请求参数：
| 参数名 | 必选 | 类型 | 说明 |
|--------|------|------|------|
| steps>>hosts | 是 | object[] | 主机数据 |
| steps>>hosts>>ansible_host | 是 | string | 主机IP |
| steps>>hosts>>organize | 是 | string | 主机所属组织 |
| steps>>script_type | 是 | int | 脚本类型[1.shell，2.python，3.playbook，4.powershell，5.network] |
| steps>>script_id | 是 | int/string | 脚本ID，传了脚本ID，以脚本ID对应脚本内容优先 |

返回：`{ "code": 0, "data": { "execution_id": 970, "task_name": "..." } }`

### execution-history（执行历史）

- URL: `/api/v6/devops/execution-history`
- Method: POST

请求参数：
| 参数名 | 必选 | 类型 | 说明 |
|--------|------|------|------|
| execution_id | 是 | int | 任务ID |

返回参数：
| 参数名 | 类型 | 说明 |
|--------|------|------|
| is_running | boolean | 任务是否执行中 |
| detail>>status | int | 执行结果[1.成功，2.失败，3.部分成功，4.正在执行] |
| detail>>output | object[] | 步骤输出列表 |
| detail>>output>>hosts | object[] | 每台主机的输出 |
| detail>>output>>hosts>>stdout | string | 输出内容 |
| detail>>output>>hosts>>status | int | 执行状态[1.成功，2.失败，3.部分成功，4.正在执行] |

## Preset Scripts

| 脚本名称 | 脚本ID | 脚本类型 | 说明 |
|----------|--------|----------|------|
| 服务重启-nginx服务重启 | 187 | 1 (shell) | nginx服务重启脚本 |
| 主机磁盘空间清理 | 197 | 1 (shell) | 磁盘空间清理脚本 |

## Hard Rules

- 这是纯 Python skill。不要调用 `node`、`tsx`、`index.ts`。
- 执行前必须确认主机 IP，不能猜测或使用占位 IP。
- `run-script` API 的 `data` 字段是 JSON 字符串，不是嵌套对象。脚本已处理此序列化。
- 轮询 `execution-history` 时最多等待 300 秒（5 分钟），超时则报告任务仍在执行中。
- 不要在脚本执行完成前就声称"执行成功"，必须等到轮询结果确认。
- 如果 API 返回错误或 `code != 0`，必须立即报告错误，不要重试。
- 默认脚本 ID 为 187（nginx 服务重启场景演示），用户可通过参数覆盖。

## Configuration

需要以下环境变量：

- `LWJK_API_URL`
- `LWJK_API_SECRET`

从 `skills/fault-handling/.env` 读取。

## Common Commands

使用预置脚本执行故障处理：

```bash
python3 skills/fault-handling/run_script.py --hosts '192.168.3.76' --script-id 187
```

指定主机组织：

```bash
python3 skills/fault-handling/run_script.py \
  --hosts '192.168.3.76' \
  --organizes '' \
  --script-id 187
```

仅提交任务不等待结果：

```bash
python3 skills/fault-handling/run_script.py \
  --hosts '192.168.3.76' \
  --script-id 187 \
  --no-wait
```

查询已有任务执行结果：

```bash
python3 skills/fault-handling/run_script.py --query 970
```

## Completion Checklist

完成前必须自检：

- 已确认主机 IP 来源合法（用户提供或告警上下文）
- 已成功调用 `run-script` API 并获取 `execution_id`
- 已轮询 `execution-history` 直到任务完成或超时
- 已向用户展示完整的执行结果报告
- 报告包含每台主机的执行状态和输出内容
- 如果执行失败，已明确说明失败原因
