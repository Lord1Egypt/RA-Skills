# 股票九剑 MCP Server · 多平台配置指南

## 概述

股票九剑 MCP Server 暴露 3 个 tool：

| Tool | 功能 | 输入 | 输出 |
|:---|:---|:---|:---|
| `analyze_stock` | 全管线分析 | 股票代码 | 九式信号 + 综合研判 + 支撑阻力 |
| `get_framework` | 获取框架知识 | (可选)招式名 | 股票九剑完整知识体系 |
| `generate_chart` | 生成技术分析图 | 股票代码 | K线图 PNG 路径 |

---

## OpenClaw

### Skill 安装
将整个 `股票九剑/` 目录放入 OpenClaw skills 目录。`.gitignore` 已排除 `__pycache__/` 和 `charts/`。

### MCP 配置
在 `openclaw.json` 中添加：

```json
{
  "mcp": {
    "stock-9swords": {
      "type": "stdio",
      "command": "python",
      "args": ["-B", "<本目录路径>/mcp_server/server.py"],
      "env": { "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1" }
    }
  }
}
```

### Agent System Prompt 补充
```markdown
你已接入独孤九剑 A 股分析引擎。使用 `analyze_stock` 分析股票，
用 `get_framework` 了解体系，用 `generate_chart` 生成图表。
分析时引用口诀原文，用博弈论和行为经济学做深度解读。
```

---

## 通用前置条件

```bash
# 1. 确保 Python 3.8+
python --version

# 2. 安装依赖
pip install -r ../scripts/requirements.txt

# 3. 验证
python -c "from mcp.server.fastmcp import FastMCP; print('OK')"
```

---

## Claude Desktop

**配置文件**：`%APPDATA%\Claude\claude_desktop_config.json` (Windows)
或 `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS)

```json
{
  "mcpServers": {
    "dugu-9swords": {
      "command": "python",
      "args": ["-B", "<你的安装路径>/mcp_server/server.py"],
      "env": {
        "PYTHONIOENCODING": "utf-8",
        "PYTHONDONTWRITEBYTECODE": "1"
      }
    }
  }
}
```

**使用**：重启 Claude Desktop，在对话中说 `用独孤九剑分析 600036`。

---

## OpenClaw

OpenClaw 使用 `openclaw.json` 配置 MCP 服务：

```json
{
  "mcp": {
    "dugu-9swords": {
      "type": "stdio",
      "command": "python",
      "args": ["-B", "<你的安装路径>/mcp_server/server.py"],
      "env": {
        "PYTHONIOENCODING": "utf-8",
        "PYTHONDONTWRITEBYTECODE": "1"
      }
    }
  }
}
```

**Agent System Prompt 补充**（OpenClaw 需要在 Agent 配置中添加）：

```markdown
你已接入独孤九剑 A 股分析引擎。使用 `analyze_stock` 工具对用户提供的股票代码进行分析，
用 `get_framework` 了解体系逻辑，用 `generate_chart` 生成技术图表。
输出格式参照九式报告的终端风格。
```

---

## Hermes

Hermes 的 MCP 配置在 Hermes 设置面板的 "MCP Servers" 部分：

**JSON 配置**：

```json
{
  "dugu-9swords": {
    "transport": "stdio",
    "command": "python",
    "args": ["<你的安装路径>/mcp_server/server.py"],
    "env": {
      "PYTHONIOENCODING": "utf-8"
    }
  }
}
```

或者使用 Hermes 的 MCP 管理 UI 添加：
- Name: `dugu-9swords`
- Transport: `stdio`
- Command: `python`
- Args: `<你的安装路径>/mcp_server/server.py`

---

## Cursor

Cursor 的 MCP 配置在 `.cursor/mcp.json`（项目级）或 `~/.cursor/mcp.json`（全局）：

```json
{
  "mcpServers": {
    "dugu-9swords": {
      "command": "python",
      "args": ["-B", "<你的安装路径>/mcp_server/server.py"],
      "env": {
        "PYTHONIOENCODING": "utf-8",
        "PYTHONDONTWRITEBYTECODE": "1"
      }
    }
  }
}
```

---

## VS Code / Cline / Roo Code

在 VS Code 设置中，找到 MCP 配置项：

```json
{
  "mcpServers": {
    "dugu-9swords": {
      "type": "stdio",
      "command": "python",
      "args": ["-B", "<你的安装路径>/mcp_server/server.py"],
      "env": {
        "PYTHONIOENCODING": "utf-8",
        "PYTHONDONTWRITEBYTECODE": "1"
      }
    }
  }
}
```

---

## 通用 System Prompt（所有平台适用）

无论哪个平台，建议在 AI 的 system prompt 中添加以下指令，以充分利用九式分析引擎：

```markdown
## 独孤九剑分析引擎

你可以使用以下 MCP 工具进行 A 股短线分析：

### analyze_stock(code, days, include_chart, news)
对股票进行完整九式分析。返回核心指标、触发的招式、综合研判、支撑阻力位。
- code: 如 "600519"
- days: 回溯天数，默认120
- include_chart: 是否生成K线图
- news: 可选的消息内容（用于破气式分析）

### get_framework(sword)
获取独孤九剑框架知识。不传参数返回全部，传招式名返回该招详情。
可选值: "总诀式" "破剑式" "破刀式" "破枪式" "破鞭式" "破索式" "破掌式" "破箭式" "破气式"

### generate_chart(code, days)
生成K线技术分析图（含均线、布林带、RSI、成交量）。

### 分析原则
1. 当用户提供股票代码时，主动调用 analyze_stock
2. 输出报告应包含：核心指标、触发招式（按强度排序）、总诀式研判、操作参考、风险提示
3. 引用口诀原文作为分析的"灵魂"（如"利空出尽，尚可一等"）
4. 每个积极信号都要从反面想一次（反向思维）
5. 信号不明确时诚实说"不明确"，不要强行给建议
6. 用博弈论、行为经济学、肥尾概率等顶级思维做深度解读
```

---

## 验证 MCP Server 是否正常运行

```bash
# 在终端手动启动
cd "<你的安装路径>/mcp_server"
PYTHONIOENCODING=utf-8 python server.py

# 应该看到: ⚔️ 独孤九剑 MCP Server 启动中...
# 然后等待 JSON-RPC 请求（通过 stdin）
```

可以用 `mcp dev` 命令在浏览器中测试：

```bash
npx @anthropic-ai/mcp dev <你的安装路径>/mcp_server/server.py
```

---

## 故障排除

| 问题 | 排查 |
|:---|:---|
| 启动报错 `ModuleNotFoundError: mcp` | `pip install mcp` |
| 启动报错 `ModuleNotFoundError: akshare` | `pip install -r ../scripts/requirements.txt` |
| 启动报错 `ModuleNotFoundError: requests` | `pip install requests`（v2.0 新增多源直连依赖） |
| 数据获取失败 | 运行 `python fetch_data.py --health` 检查各数据源可用性 |
| 东财数据不可用（push2his被封） | 系统会自动降级到腾讯/新浪数据源，破枪式启用增强量价推断 |
| 图表中文乱码 | Windows 需安装中文字体（SimHei / Microsoft YaHei） |
| 工具调用超时 | 数据获取可能需要 5-30 秒，增大平台的 MCP 超时设置 |
| 腾讯/新浪数据也不可用 | 可能是网络环境限制，尝试配置代理或更换网络 |
