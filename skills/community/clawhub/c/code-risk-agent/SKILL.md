---
name: code-risk-agent
description: "当用户需要扫描代码安全漏洞、审计代码、分析 C/Python 风险、检查依赖漏洞、或生成安全报告时触发。支持云端 LLM 语义分析和本地 GPU 回退。"
version: 1.0.0
author: a9320
---

# 🔒 CodeRisk Agent — 代码安全审计 Skill

## 脚本文件清单

本 Skill 包含以下脚本文件，由 package.json 中的 MCP server 配置自动调用：

| 文件路径 | 说明 | 用途 |
|----------|------|------|
| `mcp-server/server.py` | MCP 服务器入口脚本 | 提供 `coderisk_scan_code` 和 `coderisk_lookup_cve` 两个 Tool |
| `mcp-server/requirements.txt` | Python 依赖清单 | 声明 MCP Server 运行所需的第三方包 |

## 触发条件（匹配任意一条即触发）

| 触发词 | 示例 |
|--------|------|
| 扫描/分析 + 代码/安全/漏洞 | "扫描这段代码的安全漏洞" |
| 审计 + 代码/项目 | "审计这个项目的安全风险" |
| CWE/CVE + 查询/分析 | "检查 CWE-78 在这个文件中的情况" |
| 依赖 + 漏洞/安全 | "检查项目依赖有没有漏洞" |
| 安全 + 报告 | "生成安全审计报告" |
| audit / scan + code / security | "scan this directory for vulnerabilities" |

## 执行方式

**只调用 1 个 Tool：`coderisk_scan_code`**

参数构造规则：
- `target_path`: 用户提供的路径（必须是绝对路径）
- `enable_ai`: 默认 **false**（纯本地静态分析）。用户主动传 true 开启 AI 语义分析（需配置 API key，代码会发送至云端 LLM）
- `enable_semgrep`: 默认 true
- `scan_dependencies`: 如果路径是目录，默认 true
- `output_format`: **必须传 "json"**，便于你解析后渲染为 Markdown

如需单独查询 CVE 信息，调用 **`coderisk_lookup_cve`**（参数：`cwe_id`, `max_results`）。

## SSE 模式安全说明

`mcp-server/server.py` 支持 `--sse` 参数启用 SSE 传输模式，**仅供本地调试使用**：
- 强制绑定 `127.0.0.1`，拒绝任何非回环地址
- 必须配置环境变量 `CODERISK_SSE_API_KEY`（强随机字符串），否则拒绝启动
- 所有 SSE 请求必须在 HTTP Header 中携带 `Authorization: Bearer <CODERISK_SSE_API_KEY>`
- Starlette 运行在生产模式（`debug=False`），不泄露堆栈/路径信息
- **生产环境请使用 stdio 模式（默认）**

## 结果解读规范

Tool 返回的是完整 JSON 报告，你必须按以下结构向用户展示：

### 1. 执行摘要（必须展示）

```
📊 CodeRisk 安全扫描结果
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
文件数: {files_analyzed}
总风险: {total_risks}
耗时: {analysis_time_ms}ms
模型: {model_used}

严重级别分布:
🔴 Critical: {risk_breakdown.critical}
🟠 High: {risk_breakdown.high}
🟡 Medium: {risk_breakdown.medium}
🔵 Low: {risk_breakdown.low}
⚪ Info: {risk_breakdown.info}
```

### 2. 关键风险详情（Critical / High 必须逐条展示）

对每一条 Critical / High 风险，展示：
- **风险 ID**: `{id}`
- **严重级别**: 🔴 Critical / 🟠 High
- **CWE**: `{cwe}` + 链接 `https://cwe.mitre.org/data/definitions/{num}.html`
- **文件**: `{file}` 第 `{line_start}` 行
- **描述**: `{description}`
- **修复建议**: `{suggestion}`
- **证据来源**: `{evidence[].source}`（pattern_match / semgrep / ai / taint_analysis / dependency_scan）

### 3. 如果有 CVE 关联

调用 `coderisk_lookup_cve` 查询该 CWE 的 CVE 信息，补充展示：

```
🔗 关联 CVE:
- CVE-2024-XXXX (High, CVSS 8.1): ...
```

### 4. 报告文件

如果用户要求保存报告，告知：
- JSON 报告已保存（如果配置了输出目录）
- 可重新调用生成 SARIF / Markdown 格式

## 降级策略

| 场景 | 处理方式 |
|------|----------|
| LLM API 未配置 / 调用失败 | 自动降级为纯静态分析（27 规则 + Semgrep + Taint），告知用户"AI 语义分析未启用" |
| Semgrep 未安装 | 自动跳过，不影响核心功能 |
| CVE 数据库未构建 | 查询返回空，不影响静态分析 |
| 目标路径不存在 | 直接报错，不执行 |
| 无支持的文件 | 说明支持 .c / .h / .py，停止执行 |

## 约束

- **语言支持**: 仅 C (.c/.h) 和 Python (.py)
- **隐私**: 默认使用云端 LLM API，代码内容会发送到 API 提供商。如需完全本地，指导用户配置 `CODERISK_LLM_BACKEND=local` + ROCm GPU
- **API 费用**: 语义分析阶段会消耗 token，大文件可能产生较高费用

## 示例对话

**用户**: "扫描 ./src/ 的安全问题"
→ 调用 `coderisk_scan_code(target_path="/abs/path/to/src", output_format="json")`
→ 解析 JSON，渲染为上述 Markdown 格式
→ 展示摘要 + Critical/High 详情 + 修复建议

**用户**: "这个项目的依赖安全吗"
→ 同上，但重点展示 `source="dependency_scan"` 的风险

**用户**: "CWE-120 有什么已知的 CVE"
→ 调用 `coderisk_lookup_cve(cwe_id="CWE-120")`
→ 展示 CVE 列表
