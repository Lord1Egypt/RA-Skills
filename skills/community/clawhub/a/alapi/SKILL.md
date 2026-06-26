---
name: alapi
description: 'ALAPI 接口对接助手。帮助开发者搜索 ALAPI 接口、读取 ALAPI 文档、提取参数、生成 ALAPI 对接代码，并在用户明确提供 token 且确认后调用 ALAPI 接口。当用户提到 "ALAPI"、"alapi.cn"、ALAPI 文档 URL、ALAPI token、ALAPI 接口示例、或希望接入 ALAPI 平台接口时触发。'
---

# ALAPI 接口对接助手

## Overview

使用这个 skill 处理 ALAPI 平台的接口检索、文档读取、参数提取、代码生成和按需真实调用。

ALAPI 的关键平台约定：

```json
{
  "success": true,
  "code": 200,
  "message": "success",
  "data": { ... },
  "request_id": "xxx",
  "time": 1700000000
}
```

- Base URL: `https://v3.alapi.cn`
- 文档页: `https://www.alapi.cn/api/{id}/introduction`
- Token 创建: `https://www.alapi.cn/dashboard/data/token`
- 所有接口都要传 `token` 参数，通常放在 GET query 或 POST body
- token 优先级：显式 `--token` 高于环境变量 `ALAPI_TOKEN`

所有接口数据获取通过 [alapi.py](./scripts/alapi.py) 完成。脚本零依赖，优先用它，不要手工拼 ALAPI 的内部文档接口。

不要假设当前工作目录一定是 skill 仓库根目录，也不要写死旧的仓库内相对路径。优先从当前 skill 目录推导脚本路径：

```bash
SKILL_DIR=/absolute/path/to/alapi
SCRIPT="$SKILL_DIR/scripts/alapi.py"
python3 "$SCRIPT" --json search "IP查询"
```

## Quick Workflow

### 用户给了 ALAPI 文档 URL

从 URL 中提取 `api/{id}`，然后直接读取 OpenAPI：

```bash
python3 "$SCRIPT" --json openapi {id}
```

### 用户只描述了功能

先搜索，再决定是否继续：

```bash
python3 "$SCRIPT" --json search "用户描述的关键词"
```

如果搜索结果为空，不要立刻放弃。按这个顺序做关键词回退：

1. 去掉修饰词，只保留核心名词
2. 改用更短的同义词或上位词重新搜索
3. 对组合词拆词搜索，例如先搜“视频”，再搜“解析”，再搜“短视频”

只有在 2 到 3 轮回退后仍然没有结果时，才告诉用户当前没有匹配接口。

如果命中多个结果，先列出 2 到 5 个候选，不要擅自选一个。用户确认后再读取 OpenAPI：

```bash
python3 "$SCRIPT" --json openapi {id}
```

### 用户要浏览全部接口

```bash
python3 "$SCRIPT" --json explore
```

### 用户要代码，不要真实请求

优先读取 `openapi`，再从结果中提取：

- 请求路径
- 请求方法
- 必填参数
- 可选参数
- 响应结构
- 文档链接 `https://www.alapi.cn/api/{id}/introduction`

如果当前只是候选阶段，不要直接给“最终确定版代码”。最多只给：

- 候选列表
- 候选差异
- 确认后会生成哪种语言的代码

除非只有单一明确命中，或者用户已经确认了具体接口。

### 用户明确要求真实调用

仅在用户明确要求“直接调用/测试接口”且已提供 token 时执行：

```bash
python3 "$SCRIPT" --json call {path} --token {用户的token} --param key=value
```

如果用户没有 token，引导去创建：
> 请先在 https://www.alapi.cn/dashboard/data/token 创建 API Token。

如果用户没有显式给出 token，但环境里已经有 `ALAPI_TOKEN`，可以直接使用；如果两者都存在，始终以显式 token 为准。

## Critical Rules

- 默认优先做只读操作：`search`、`detail`、`openapi`、`explore`
- 优先使用 `--json`，再基于 JSON 结果生成自然语言说明
- 不要手工猜 ALAPI 文档接口路径，优先使用 `scripts/alapi.py`
- 不要假设 cwd 一定在 skill 根目录
- 不要在最终回复中回显用户的真实 token
- 支持从环境变量 `ALAPI_TOKEN` 读取 token，但显式 `--token` 优先级最高
- 搜索结果不唯一时，先列候选，不要擅自决定接口
- 搜索 0 结果时，先做关键词回退，不要第一步就判定不存在
- 用户只要“文档”或“代码示例”时，不要真实调用接口
- 候选未确认前，不要输出“最终定稿代码”；先输出候选和差异
- 如果用户没有提供足够参数，不要猜值，明确指出缺失参数
- 如果 OpenAPI 没有写清楚，不要补脑生成不存在的参数名、默认值或响应字段
- `call` 失败时，优先保留平台原始错误结构，再结合错误码给出下一步建议
- 对需要真实参数才能调用的接口，如果用户未给足参数，先说明缺什么，不要猜值

## Command Reference

| 命令 | 用途 |
|------|------|
| `search <keyword>` | 搜索接口 |
| `explore` | 浏览全部接口 |
| `detail <id>` | 读取接口基础信息 |
| `openapi <id>` | 读取 OpenAPI 规格 |
| `call <path>` | 发起真实请求 |
| `--json` | 输出稳定 JSON，供 agent 继续处理 |

## Code Generation Rules

- Token 占位符统一使用 `ALAPI_TOKEN`
- 默认生成最小可运行版本，不要过度封装
- 保留响应解析和错误处理逻辑，覆盖 `success/code/message/data/request_id/time`
- Python 用 `requests`；JS/TS 用 `fetch`；PHP 用 `curl`；Go 用 `net/http`
- 不引入非必要依赖
- 如果用户在服务端项目中接入，优先建议把 token 放到环境变量或服务端配置，不要放前端
- 如果参数或方法来自 OpenAPI，就按 OpenAPI 生成；如果 OpenAPI 缺失，不要伪造
- 详细模板见 [code-examples.md](./references/code-examples.md)

前端/后端分层规则：

- 浏览器端或 Next.js Client Component 默认不要直连 ALAPI
- Node.js 服务端、PHP 后端、Python 后端可以直接读取 `ALAPI_TOKEN`
- 如果用户说“前端项目接入”，优先给服务端代理方案，除非用户明确说明是在纯后端环境运行

## Reporting Template

当文档不完全、存在候选、或存在不确定字段时，优先按这个结构输出：

### 已确认

- 从 OpenAPI 或真实调用中明确确认的接口路径、方法、参数、返回字段

### 待确认

- 当前还需要用户确认的候选接口或业务选择

### 不要假设

- 文档未写清楚，因此不能主动编造的参数、默认值、返回字段或平台行为

## Live Call Rules

执行真实调用后，优先保留这些信息：

- 接口名和路径
- token 来源：显式 `--token` 还是环境变量 `ALAPI_TOKEN`
- 请求里实际传入的业务参数
- 原始响应中的关键字段：`success`、`code`、`request_id`、`data` 摘要

不要保留这些信息：

- token 原文
- 不必要的敏感上下文
- 会导致凭证泄露的命令历史

## Real Usage Examples

- `帮我查一下 IP: 8.8.8.8`
  先定位 IP 查询接口，再在用户明确要求真实调用且 token 可用时执行查询，或先给出查询代码。

- `帮我生成视频解析的代码`
  先搜索“视频解析”相关接口，若命中多个候选先列给用户确认，再基于对应 OpenAPI 生成最小可运行代码。

## Failure Handling

| code | 含义 | 建议 |
|------|------|------|
| 200 | 成功 | — |
| 401 | Token 无效或未传 | 检查 token |
| 403 | 套餐不含此接口 | 升级套餐 |
| 422 | 参数校验失败 | 优先指出缺失或格式错误的参数 |
| 429 | 频率超限 | 降频、加缓存，必要时延迟重试 |
| 500 | 服务端错误 | 保留原始错误，建议重试 |

如果搜索结果为空，直接说明没有匹配接口，并提示改用更明确的关键词。

如果 `openapi` 缺失但 `detail` 或文档页存在，明确告诉用户规范不完整，并退回基础信息 + 文档链接。
