# Agent Ready Scanner

> 扫描网站是否为 AI Agent 做好准备

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

一个用于检测网站是否为 AI Agent（智能体）做好准备的工具，参考 [isitagentready.com](https://isitagentready.com) 的检测标准。

## 🤔 什么是 "Agent Ready"？

随着 AI Agent（如 ChatGPT、Claude、Perplexity 等）越来越普及，网站需要为这些智能体提供更好的支持，包括：

- **可发现性**：让 AI 能找到网站的内容
- **内容可访问性**：提供 AI 可理解的格式
- **Bot 访问控制**：明确告诉 AI 哪些可以访问
- **协议支持**：支持 MCP、Agent Skills 等新兴协议
- **商业协议**：支持 AI 驱动的支付和交易

Agent Ready Scanner 帮你检测网站在这些方面的准备程度。

## ✨ 功能特性

- **15+ 项检查**：覆盖 5 大类别
- **真实 HTTP 检测**：实际请求网站端点，不做猜测
- **详细报告**：HTML 报告包含评分、状态、详情
- **修复建议**：针对未通过项提供具体修复代码（可一键复制）
- **评分系统**：0-100% 准备度评分

## 📦 安装

### 作为 OpenClaw Skill 使用

将此技能克隆到你的 skills 目录：

```bash
cd ~/.qclaw/skills
git clone https://github.com/1cloudy/agent-ready-scanner.git
```

### 独立使用

```bash
git clone https://github.com/1cloudy/agent-ready-scanner.git
cd agent-ready-scanner
pip install requests  # 唯一依赖
```

## 🚀 使用方式

### 命令行

```bash
# 扫描网站（文本输出）
python3 scripts/scan.py https://example.com --format text

# 生成 JSON 报告
python3 scripts/scan.py https://example.com -o report.json

# 生成 HTML 报告
python3 scripts/scan.py https://example.com -o report.json
python3 scripts/generate_html.py report.json -o report.html
```

### 作为 OpenClaw Skill

在 OpenClaw 中直接说：

```
扫描 example.com 是否 agent ready
检查 https://mywebsite.com 的 agent readiness
帮我检查 xxx.com 是否为 AI 准备好
```

## 🔍 检查项目

### 1. Discoverability（可发现性）

| 检查项 | 说明 |
|--------|------|
| **robots.txt** | 是否存在，是否包含 AI bot 规则和 sitemap 指令 |
| **Sitemap** | sitemap.xml 是否存在且有效 |
| **Link Headers** | Link 响应头是否包含发现信息 |

### 2. Content Accessibility（内容可访问性）

| 检查项 | 说明 |
|--------|------|
| **llms.txt** | 是否提供 Markdown 格式的网站摘要（[llmstxt.org](https://llmstxt.org/)） |
| **Markdown Negotiation** | 是否支持 Markdown 内容协商 |

### 3. Bot Access Control（Bot 访问控制）

| 检查项 | 说明 |
|--------|------|
| **AI Bot Rules** | robots.txt 中是否配置 AI 爬虫规则（GPTBot、Claude-Web、Applebot 等） |
| **Content Signals** | 是否支持 Content Signals |

### 4. Protocol Discovery（协议发现）

| 检查项 | 说明 |
|--------|------|
| **MCP Server Card** | `/.well-known/mcp.json` 是否存在 |
| **Agent Skills** | Agent Skills 定义是否存在 |
| **WebMCP** | 是否支持 WebMCP |
| **API Catalog** | OpenAPI/Swagger 文档是否存在 |
| **OAuth Discovery** | OAuth/OpenID Connect 发现是否配置 |
| **A2A Agent Card** | A2A Agent Card 是否存在 |

### 5. Commerce（商业协议）

| 检查项 | 说明 |
|--------|------|
| **x402** | 是否支持 x402 支付协议 |
| **UCP** | 是否支持 Universal Commerce Protocol |
| **ACP** | 是否支持 Agentic Commerce Protocol |

## 📊 评分规则

| 状态 | 得分 | 说明 |
|------|------|------|
| ✅ Pass | 2 分 | 完全符合要求 |
| ⚠️ Warning | 1 分 | 部分符合或需要改进 |
| ❌ Fail | 0 分 | 不符合或不存在 |

**总分计算**：
```
总分 = (所有检查项得分之和 / (检查项数量 × 2)) × 100%
```

## 📄 输出示例

### 文本输出

```
🔍 扫描 https://example.com ...
Agent Ready Report for https://example.com
==================================================
Score: 10/32 (31%)

❌ 网站尚未准备好，得分 31%，6 项未通过

## Discoverability
Score: 1/6
  ❌ robots.txt: robots.txt 不存在或无法访问
  ❌ Sitemap: Sitemap 不存在或无效
  ⚠️ Link Headers: Link 响应头未设置

...
```

### HTML 报告

生成精美的 HTML 报告，包含：

- 🎯 总评分圆环图
- 📊 分类得分卡片
- ✅❌ 每项检查状态和详情
- 💡 修复建议（可一键复制）

## 🛠️ 快速改进指南

### 添加 llms.txt

在网站根目录创建 `llms.txt`：

```markdown
# example.com

> 一个示例网站的描述

## 主要内容

- /about - 关于我们
- /products - 产品列表
- /blog - 博客文章

## 联系方式

- email: contact@example.com
```

### 配置 AI Bot 规则

在 `robots.txt` 中添加：

```txt
# AI Crawlers
User-agent: GPTBot
Disallow: /private/

User-agent: Claude-Web
Disallow: /private/

User-agent: Applebot
Allow: /

Sitemap: https://example.com/sitemap.xml
```

### 添加 MCP Server Card

在 `/.well-known/mcp.json` 创建：

```json
{
  "name": "Example MCP Server",
  "description": "提供示例网站的 MCP 接口",
  "transport": {
    "type": "sse",
    "url": "https://api.example.com/mcp/sse"
  }
}
```

## 📚 参考资料

- [isitagentready.com](https://isitagentready.com) — 原始灵感来源
- [llms.txt](https://llmstxt.org/) — LLM 可读的网站摘要标准
- [MCP](https://modelcontextprotocol.io/) — Model Context Protocol
- [Agent Skills](https://agentskills.io/) — Agent Skills 标准
- [x402](https://www.x402.org/) — HTTP 402 Payment Protocol
- [A2A](https://a2a.io/) — Agent-to-Agent Protocol

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

```bash
git clone https://github.com/1cloudy/agent-ready-scanner.git
cd agent-ready-scanner
# 做出改进
git commit -am "Your improvement"
git push
```

## 📝 License

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- [isitagentready.com](https://isitagentready.com) — 提供了检测标准的灵感
- OpenClaw — 提供了 Skill 框架支持
