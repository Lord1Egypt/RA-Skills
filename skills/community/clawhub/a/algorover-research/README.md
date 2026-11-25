# AlgoRover Research Skills

Discover strategies, preview and run historical backtests, inspect jobs, and download reports using the hosted AlgoRover Research MCP service.

## Install

```sh
npx clawhub@latest skill install algorover-research
```

Follow [connection.md](connection.md) to connect `https://research.algorover.ai/mcp` in your client. Skill installation adds instructions; MCP connection and browser authorization are separate steps.

Discovery and preparation are public. Personal runs and reports require Research OAuth with `research:read` and `research:run`. Use the client's browser authorization flow for credentials.

Ask your agent to find a strategy, inspect its presets, and preview a 90-day historical backtest. Confirm the preview before starting. Then inspect progress, cancel a selected job or download completed reports.

Research uses public historical market data. It does not connect exchange accounts or place orders. Historical results do not establish future returns.

## Validation

The hosted MCP endpoint and public queries were verified in other clients. OpenClaw-specific OAuth, interactive cards and complete backtest workflows have not yet been validated.

Published by Rivendell Holdings Investment Limited. Based on Research 0.1.5.

- [Research](https://research.algorover.ai/)
- [Support](https://www.algorover.ai/en/help/)
- [Privacy](https://www.algorover.ai/privacy/)
- [Terms](https://www.algorover.ai/terms/)
