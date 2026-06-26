---
name: agent-ready-scanner
description: |
  扫描网站是否为 AI Agent 做好准备。检查 robots.txt、llms.txt、MCP、Agent Skills 等 15+ 项标准。
  触发方式：用户说"扫描 example.com 是否 agent ready"、"检查网站是否为 AI 准备好"、"帮我检查 xxx.com 的 agent readiness"。
  输出：生成 HTML 报告，包含评分、状态和修复建议。
---

# Agent Ready Scanner

扫描网站是否为 AI Agent 做好准备，参考 [isitagentready.com](https://isitagentready.com)。

## 使用方式

```
扫描 example.com 是否 agent ready
检查 https://mywebsite.com 的 agent readiness
帮我检查 xxx.com 是否为 AI 准备好
```

## 检查项目

扫描覆盖 **5 大类 15+ 项检查**：

### 1. Discoverability（可发现性）
- **robots.txt** — 是否存在，是否包含 AI bot 规则和 sitemap
- **Sitemap** — sitemap.xml 是否存在且有效
- **Link Headers** — Link 响应头是否包含发现信息

### 2. Content Accessibility（内容可访问性）
- **llms.txt** — 是否提供 Markdown 格式的网站摘要
- **Markdown Negotiation** — 是否支持 Markdown 内容协商

### 3. Bot Access Control（Bot 访问控制）
- **AI Bot Rules** — robots.txt 中是否配置 AI 爬虫规则（GPTBot、Claude-Web 等）
- **Content Signals** — 是否支持 Content Signals

### 4. Protocol Discovery（协议发现）
- **MCP Server Card** — /.well-known/mcp.json 是否存在
- **Agent Skills** — Agent Skills 定义是否存在
- **WebMCP** — 是否支持 WebMCP
- **API Catalog** — OpenAPI/Swagger 文档是否存在
- **OAuth Discovery** — OAuth/OpenID Connect 发现是否配置
- **A2A Agent Card** — A2A Agent Card 是否存在

### 5. Commerce（商业协议）
- **x402** — 是否支持 x402 支付协议
- **UCP** — 是否支持 Universal Commerce Protocol
- **ACP** — 是否支持 Agentic Commerce Protocol

## 输出

生成 HTML 报告，包含：

1. **总评分** — 0-100% 的准备度评分
2. **分类得分** — 每个类别的得分情况
3. **检查详情** — 每项检查的状态和详情
4. **修复建议** — 针对未通过项的具体修复代码/配置建议（可一键复制）

## 执行流程

1. 解析用户提供的 URL
2. 运行 `scripts/scan.py` 执行所有 HTTP 检查
3. 生成 JSON 报告
4. 运行 `scripts/generate_html.py` 生成 HTML 报告
5. 将 HTML 报告保存到用户指定位置或当前工作目录

## 脚本

### scripts/scan.py

主扫描脚本，执行所有检查。

```bash
python3 scripts/scan.py <url> --output report.json
```

参数：
- `url` — 要扫描的网站 URL
- `--timeout` — 请求超时时间（默认 10 秒）
- `--output, -o` — 输出 JSON 文件路径
- `--format` — 输出格式（json 或 text）

### scripts/generate_html.py

将 JSON 报告转换为 HTML。

```bash
python3 scripts/generate_html.py report.json --output report.html
```

## 评分规则

| 状态 | 得分 |
|------|------|
| ✅ Pass | 2 分 |
| ⚠️ Warning | 1 分 |
| ❌ Fail | 0 分 |

总分 = 所有检查项得分之和 / (检查项数量 × 2) × 100%

## 示例

**输入：**
```
扫描 https://example.com 是否 agent ready
```

**输出：**
生成 `agent-ready-report-example.com.html`，包含完整的检查报告。

## 依赖

- Python 3.8+
- requests 库（如未安装会提示）

## 参考

- [isitagentready.com](https://isitagentready.com) — 原始灵感来源
- [llms.txt](https://llmstxt.org/) — LLM 可读的网站摘要标准
- [MCP](https://modelcontextprotocol.io/) — Model Context Protocol
- [Agent Skills](https://agentskills.io/) — Agent Skills 标准
