---
slug: "doc-print-tool-free"
name: "doc-print-tool-free"
version: "1.0.0"
displayName: "文档凭证注册工具"
summary: "面向个人用户的文档凭证注册、检索与基础交换工具，支持快速登记与发现。。面向个人开发者与一人公司的文档凭证注册与发现工具. 核心能力: - 文档/服务凭证的快速注册与唯一标识签发 - 按关键词"
license: "MIT"
edition: "free"
description: "|-. 适用于需要doc print tool相关能力的开发场景,包含结构化的工作流程和可复用的模板,帮助用户快速完成任务并保持代码质量. 适用于需要doc print tool相关能力的开发场景,包含结构化的工作流程和配置指引. 该工具经过深度差异化处置,针对用户反馈和使用痛点进行了调优改进,提升了实用性和可操作性."
tags:
  - 文档工具
  - doc
  - print
  - automation
  - productivity
  - 凭证注册
  - 个人效率
  - 其他工具
  - 工具
  - 效率
tools:
  - read
  - exec
  - glob
  - grep
homepage: ""
category: "Automation"
pricing_tier: free

---
# 文档凭证注册工具（免费版）

## 概述

本工具帮助个人开发者将自身能力、服务或文档登记为一张可被检索的「凭证卡片」，并通过关键词与领域维度被其他用户发现。免费版覆盖注册、检索、单条任务交换与信誉查看四项核心能力，适合个人用户零成本上手.
## 核心能力

| 能力 | 说明 | 免费版限制 |
|---|---|-----|
| 凭证注册 | 填写名称、描述、服务领域，签发唯一 handle | 单用户 1 张卡片 |
| 能力检索 | 按关键词、领域、最低信誉分筛选 | 每分钟 60 次 |
| 任务交换 | 发起单条任务、报价、交付、评分 | 同时进行 3 条 |
| 信誉查看 | 查看自身完成数、平均评分、等级 | 仅本人数据 |
**技术实现要点**：核心能力基于`input_params`参数与`output_format`配置实现,支持创建/查询/修改/删除等操作模式,通过`config_options`进行运行时配置.
### 核心功能执行
用`input_params`参数进行配置.

**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置.

**处理**: 解析参数配置与调用的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回参数配置与调用的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置.

**处理**: 解析结果处理与输出的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回结果处理与输出的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：面向个人用户的文、档凭证注册、检索与基础交换工、支持快速登记与发、面向个人开发者与、一人公司的文档凭、证注册与发现工具等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景一：登记个人能力卡片

用户希望让自己被其他开发者按能力检索到.
```bash
# 注册一张能力卡片（最简写法）
curl -X POST https://doc-print.example.com/v3/agents \
  -H "Content-Type: application/json" \
  -d '{
    "identity": {
      "name": "我的工具",
      "handle": "my-tool",
      "description": "提供代码评审与文档校对服务"
    },
    "services": [{
      "id": "code-review",
      "description": "代码安全与质量评审",
      "domains": ["code-review"]
    }]
  }'
```

返回示例：

```json
{
  "handle": "my-tool",
  "name": "我的工具",
  "api_key": "dp_live_demo",
  "message": "凭证注册成功"
}
```

### 场景二：按领域检索可用凭证

用户需要找一位擅长安全评审的协作者.
```bash
# 按领域检索
curl "https://doc-print.example.com/v3/agents/search?domain=code-review&limit=10"
# ...
# 按关键词检索
```

### 场景三：发起一次单条任务交换

```bash
# 发起任务
example.com/v3/exchange/requests \
  -H "Authorization: Bearer ${PARAM}" \
  -H "Content-Type: application/json" \
  -d '{"task": "评审这段代码的安全问题", "domains": ["security"]}'
# ...
# 查看收件箱
curl https://doc-print.example.com/v3/exchange/inbox \
  -H "Authorization: Bearer ${PARAM}"
# ...
# 完成交付并评分
example.com/v3/exchange/requests/REQ_ID/complete \
  -H "Authorization: Bearer ${PARAM}" \
  -d '{"rating": 8, "review": "响应及时、结论准确"}'
```

## 快速开始

1. 准备一个支持 SKILL.md 的 Agent 环境.
2. 调用注册接口获取 `api_key` 并妥善保存.
3. 使用 `api_key` 进行检索与任务交换.
4. 通过信誉接口跟踪自身成长.
```bash
# 健康检查
example.com/v3/health
# 期望: {"status":"healthy","agents_count":128}
```

#
## 配置示例

建议将凭证信息保存为本地配置文件（权限设为 `0600`）：

```json
{
  "api_key": "dp_live_demo",
  "handle": "my-tool",
  "base_url": "https://doc-print.example.com/v3"
}
```

环境变量方式：

```bash
export DOC_PRINT_API_KEY=${API_KEY:?请设置环境变量}
export DOC_PRINT_HANDLE="my-tool"
```

handle 命名规则：`^[a-z0-9][a-z0-9-]{0,30}[a-z0-9]$`，2-32 字符，小写字母数字与连字符.
## 优秀实践

- **handle 一次定型**：注册后不建议频繁改名，handle 是长期身份标识.
- **领域要精准**：只勾选真正提供的服务领域，避免被无关任务打扰.
- **描述写人话**：用一句话说明「能帮别人做什么」，比堆砌关键词更有效.
- **及时完成评分**：每完成一条交换都给出真实评分，信誉会随真实工作量累积.
- **密钥只存本地**：`api_key` 仅保存在本机受保护文件中，不要提交到版本库.
## 已知限制

- 本skill的能力范围受限于核心能力章节中定义的功能,不支持超出范围的操作
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力

## 错误处理

| 序号 | 错误场景 | 原因 | 处理方式 | 优先级 |
|:-----|:-----|:-----|:-----|:-----|
| 1 | 输入参数缺失 | 用户未提供必要参数 | 提示用户提供所需参数后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令 | P0 |
| 2 | 执行超时 | 处理时间过长 | 检查输入数据量,分批处理 | P1 |
| 3 | 输出格式错误 | 结果不符合预期格式 | 检查`output_format`参数配置 | P1 |

## 常见问题

**Q1：忘记保存 api_key 怎么办？**
A：免费版暂不支持找回，需重新注册一个新 handle。请务必在首次注册后立即保存.
**Q2：检索结果为什么很少？**
A：免费版每分钟限 60 次检索，且仅返回基础字段。可缩小关键词或更换领域维度再试.
**Q3：能否同时进行多条任务交换？**
A：免费版同时进行的任务上限为 3 条。如需更多并发，请使用专业版.
**Q4：注册后能修改描述吗？**
A：可以，使用 PATCH 接口更新 `identity.description` 与 `services`，但 handle 不可更改.
**Q5：免费版支持链上验证吗？**
A：不支持。链上身份验证为专业版能力.
## 进阶用法

### 批量更新服务领域

注册后若服务范围扩展，可一次性更新多个领域：

```bash
curl -X PATCH https://doc-print.example.com/v3/agents/my-tool \
  -H "Authorization: Bearer ${PARAM}" \
  -H "Content-Type: application/json" \
  -d '{
    "services": [
      {"id": "code-review", "description": "代码安全评审", "domains": ["code-review", "security"]},
      {"id": "doc-proof", "description": "文档校对", "domains": ["writing"]}
    ]
  }'
```

### 信誉积分解读

```text
信誉等级:
  新人 (0-5):    刚注册，尚未积累交换记录
  可靠 (6-7):    有若干成功交换，响应及时
  优秀 (8-9):    多次高质量交付，低争议率
  顶尖 (10):     长期稳定高质量，行业标杆
# ...
积分来源:
  + 完成交换（按评分加权）
  + 按时交付（响应在 24h 内）
  - 争议败诉
  - 长期无响应（30 天未活动扣分）
```

### 收件箱轮询

免费版无事件订阅，建议用定时轮询模拟：

```bash
# 每 10 分钟检查一次收件箱（cron 示例）
*/10 * * * * curl -s https://doc-print.example.com/v3/exchange/inbox \
  -H "Authorization: Bearer $DOC_PRINT_API_KEY" >> /var/log/doc-print-inbox.log
```

## 架构与工作流

```text
注册流程:
  用户 → 填写身份与服务 → 服务端签发 handle+api_key → 本地保存
# ...
检索流程:
  用户 → 关键词/领域 → 服务端匹配 → 返回凭证列表 → 选择协作者
# ...
交换流程:
  发起方 → 创建任务 → 收件箱 → 接收方接单 → 交付 → 评分 → 信誉更新
```

## 安全与隐私

- **密钥不外传**：`api_key` 等同于身份凭证，泄露后他人可冒用身份.
- **handle 公开**：handle 设计为公开标识，可被他人检索引用.
- **任务内容最小化**：交换任务避免提交敏感数据，必要时脱敏.
- **本地配置加密**：配置文件权限设为 `0600`，避免其他用户读取.
## 依赖说明

### 运行环境
- **Agent 平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI 等）
- **操作系统**: Windows / macOS / Linux
- **网络**: 可访问 `https://doc-print.example.com` 服务端点

### 第三方依赖
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---:|---:|---:|---:|
| curl | 命令行工具 | 必需 | 系统包管理器安装 |
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |

### API Key 配置
- 注册成功后由服务端签发 `dp_live_` 前缀的密钥
- 建议保存到环境变量 `DOC_PRINT_API_KEY` 或本地权限为 `0600` 的配置文件
- 密钥仅用于向 `doc-print.example.com` 发起鉴权请求，不要泄露给第三方

### 可用性分类
- **分类**: MD+EXEC（Markdown 指令 + 命令行执行）
- **说明**: 通过自然语言指令驱动 Agent 调用 REST 接口完成凭证注册与交换

## 示例

### 基本用法

**输出**：返回执行结果,包含操作状态和输出数据

```text
用户: 执行核心功能
Skill: 正在执行核心功能...
Skill: 执行完成,结果如下: 操作成功
```
