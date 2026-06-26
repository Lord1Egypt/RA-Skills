---
name: apm-performance-analysis
description: "APM 性能分析工具，通过 ApmClient.SendMCPMessage 连接腾讯云 APM MCP Server，提供业务系统查询、调用链追踪、火焰图、Span 耗时分析等能力。Trigger when user mentions APM, 性能分析, 调用链, 火焰图, Span, or 耗时分析."
agent_created: true
allowed-tools:
  - Bash
  - Read
---

# APM 性能分析

通过腾讯云官方 SDK `ApmClient.SendMCPMessage` 接口连接 APM MCP Server，自动发现并调用 APM 性能分析工具，实现智能化性能诊断。

## 初始回答规范

用户首次提问（如「能做什么」「有什么功能」）时，按以下要点生成回答：

1. 说明通过腾讯云官方 SDK `ApmClient.SendMCPMessage` 连接远程 APM MCP Server
2. 说明需配置腾讯云凭证（SecretId/SecretKey），通过云API标准签名（TC3-HMAC-SHA256）自动鉴权
3. 末尾以表格形式列出 4–5 条示例引导，至少包含一条「查看 MCP 支持哪些操作」

## 快速开始

使用内嵌（vendored）官方 SDK，**无需虚拟环境和 pip 安装**：

```bash
python scripts/apm_mcp_client.py <command>
```

## 执行流程

1. 检查凭证 → 执行 `echo $TENCENTCLOUD_SECRET_ID`，缺失则按 `references/credential_guide.md` 中的格式模板引导配置
2. 验证连通性 → `python scripts/apm_mcp_client.py ping`
3. 发现工具 → `python scripts/apm_mcp_client.py list-tools --output json`
4. 展示工具列表 → 按 `references/interaction_guide.md` 格式规范呈现
5. 确认功能和参数 → 按 `references/interaction_guide.md` 交互规范与用户确认
6. 执行调用 → `python scripts/apm_mcp_client.py call-tool --name <name> --args '{...}'`
7. 解读结果 → 给出性能分析建议

## 核心命令

```bash
# 检测连通性
python scripts/apm_mcp_client.py ping

# 列出所有可用工具
python scripts/apm_mcp_client.py list-tools --output json

# 调用指定工具（JSON dict 自动转换为 APMKVItem 列表）
python scripts/apm_mcp_client.py call-tool --name <tool_name> --args '{"param1": "value1"}'
```

## 工具调用核心原则

1. 不得在未确认功能和参数的情况下直接调用工具
2. 上下文已有信息优先复用，避免重复询问
3. 可选参数必须列出，敏感参数一律通过环境变量配置

> 交互规范详见 `references/interaction_guide.md`

## 凭证与安全（强制规则）

凭证通过 **shell 环境变量**管理，不使用 `.env` 文件。通过云API标准签名（TC3-HMAC-SHA256）自动鉴权。

**安全底线**：
1. 禁止硬编码密钥，一律通过 shell 环境变量引用
2. 文档和对话中使用占位符 `<your_secret_id>` / `<your_secret_key>`
3. 用户提供密钥明文时不得回显，提示在终端中配置
4. 密钥不会写入任何项目文件或日志
5. 凭证缺失时，**必须按 `references/credential_guide.md` 中定义的格式模板引导配置**，不得自行编造格式

> 完整凭证配置与安全规则见 `references/credential_guide.md`

## 移动端兼容（强制规则）

本 Skill 支持移动端远程使用，**全流程不得触发 IDE 确认弹窗**。三条核心禁令：

1. **禁止创建临时文件** — 不得写入任何辅助脚本或数据文件
2. **禁止删除文件** — 不得执行 `rm` 等危险命令
3. **数据必须在对话中直接处理** — 使用 Markdown 表格/代码块/树形结构展示，不得借助外部脚本

> 完整规范与示例见 `references/mobile_compat_guide.md`

## 错误处理

调用失败时错误写入 `./logs/apm_error.log`（JSON 格式，含错误码、RequestId、堆栈）。日志权限 `600`，不记录密钥。

> 日志格式和排错指引见 `references/error_log_guide.md`

## 调用决策表

| 条件 | 操作 |
|------|------|
| 凭证已配置且 ping 成功 | 正常执行工具调用 |
| 凭证未配置 | 按 `references/credential_guide.md` 模板引导配置 |
| 返回服务角色授权失败错误 | 按 `references/error_log_guide.md` 中"服务角色授权失败"章节引导用户前往控制台授权 |
| ping 失败 | 检查网络和 Endpoint，参考 `references/cloud_api_guide.md` 排查 |

## Resources

### scripts/

| 文件 | 说明 |
|------|------|
| `apm_mcp_client.py` | 云API 客户端：`ping`、`list-tools`、`call-tool` |
| `venv_manager.py` | 脚本运行器（向后兼容） |
| `tencentcloud/` | 内嵌（vendored）腾讯云官方 Python SDK v3.1.93 |

### references/

| 文档 | 说明 |
|------|------|
| `interaction_guide.md` | 工具调用交互规范（三种场景）和工具列表展示格式 |
| `credential_guide.md` | 凭证配置步骤、引导模板、环境变量、安全规则 |
| `cloud_api_guide.md` | SendMCPMessage 接口详情、SDK架构、Endpoint、参数格式、错误码 |
| `error_log_guide.md` | 错误日志格式、排错指引 |
| `mobile_compat_guide.md` | 移动端兼容强制规则（禁止创建/删除文件、数据直接处理） |
