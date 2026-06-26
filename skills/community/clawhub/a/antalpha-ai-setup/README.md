[🇺🇸 English](#english) · [🇨🇳 中文](#chinese)

---

<a name="english"></a>

# Antalpha AI Setup

Setup guide for the Antalpha Skills MCP Server — 60+ Web3 tools for DEX swaps, smart money tracking, Polymarket prediction markets, Hyperliquid perpetuals, and DeFi analytics.

## What is this?

An [OpenClaw](https://github.com/openclaw/openclaw) skill that connects your AI agent to the Antalpha Skills MCP server with 60+ tools.

## Quick Install

### Option 1: mcporter (Recommended)

```bash
npx mcporter list https://mcp-skills.ai.antalpha.com/mcp --name antalpha
```

Output:

```
✓ MCP server "antalpha" connected

→ Registering agent...
 ✓ agent_id: "a3f1c8e7-4d2b-4a9f-b6e5-7c8d9e0f1a2b"
 ✓ api_key: "sk_4f7a2e...b2c3d4e5f6a7b8c9d"

 62 tools ready.
```

> Then add the returned `agent_id` and `api_key` to your MCP client config.

### Option 2: OpenClaw Skill Install

```bash
openclaw skill install https://github.com/AntalphaAI/antalpha-ai-setup
```

## MCP Server URL

```
https://mcp-skills.ai.antalpha.com/mcp
```

## Supported Clients

- Claude.ai (web)
- Claude Code (terminal)
- Codex (terminal)
- Claude Desktop / Cursor / Windsurf
- Gemini CLI
- OpenCode
- OpenClaw

## What You Get

60+ tools across these categories:

- **DEX Swaps** — swap-quote, swap-full, smart-swap-* — *"Get a quote for 1 ETH to USDC"*
- **Smart Money** — smart-money-signal, smart-money-watch — *"Show whale trading signals"*
- **Polymarket** — poly-trending, poly-buy, poly-master-* — *"What's trending on Polymarket?"*
- **Hyperliquid** — hl-positions, hl-limit-order, hl-market-order — *"Show my perp positions"*
- **DeFi** — investor_discover, investor_analyze — *"Find stablecoin yields above 5%"*
- **Settlement** — settlement-gas-prediction, settlement-track-tx — *"What's the gas on Arbitrum?"*

## Related

- [Antalpha MCP Documentation](https://github.com/antalpha-com/antalpha-skills)
- [Antalpha Website](https://www.antalpha.com/)

## License

MIT

---

<a name="chinese"></a>

# Antalpha AI Setup（中文）

Antalpha Skills MCP 服务器安装指南 —— 60+ Web3 工具，覆盖 DEX 兑换、聪明钱追踪、Polymarket 预测市场、Hyperliquid 永续合约和 DeFi 分析。

## 这是什么？

一个 [OpenClaw](https://github.com/openclaw/openclaw) Skill，帮助你的 AI Agent 接入 Antalpha Skills MCP 服务器，解锁 60+ 个 Web3 工具。

## 快速安装

### 方式一：mcporter（推荐）

```bash
npx mcporter list https://mcp-skills.ai.antalpha.com/mcp --name antalpha
```

输出示例：

```
✓ MCP server "antalpha" connected

→ Registering agent...
 ✓ agent_id: "a3f1c8e7-4d2b-4a9f-b6e5-7c8d9e0f1a2b"
 ✓ api_key: "sk_4f7a2e...b2c3d4e5f6a7b8c9d"

 62 tools ready.
```

> 将返回的 `agent_id` 和 `api_key` 配置到你的 MCP 客户端即可。

### 方式二：OpenClaw Skill 安装

```bash
openclaw skill install https://github.com/AntalphaAI/antalpha-ai-setup
```

## MCP 服务器地址

```
https://mcp-skills.ai.antalpha.com/mcp
```

## 支持的客户端

- Claude.ai（网页版）
- Claude Code（终端）
- Codex（终端）
- Claude Desktop / Cursor / Windsurf
- Gemini CLI
- OpenCode
- OpenClaw

## 工具分类（60+）

- **DEX 兑换** — swap-quote、swap-full、smart-swap-* — *"查询 1 ETH 兑换 USDC 的报价"*
- **聪明钱追踪** — smart-money-signal、smart-money-watch — *"查看鲸鱼交易信号"*
- **Polymarket 预测市场** — poly-trending、poly-buy、poly-master-* — *"当前 Polymarket 热门市场有哪些？"*
- **Hyperliquid 永续合约** — hl-positions、hl-limit-order、hl-market-order — *"查看我的永续仓位"*
- **DeFi 投资** — investor_discover、investor_analyze — *"发现年化 5% 以上的稳定币机会"*
- **链上结算** — settlement-gas-prediction、settlement-track-tx — *"查询 Arbitrum 当前 gas 费"*

## 相关链接

- [Antalpha MCP 文档](https://github.com/antalpha-com/antalpha-skills)
- [Antalpha 官网](https://www.antalpha.com/)

## 许可证

MIT
