# Bailian Search v1.1.0

Real-time web search powered by Alibaba Cloud Bailian (DashScope).
*Fixed MCP protocol implementation - 2026-03-23*

## Quick Start

```bash
# Install
openclaw skill install bailian-search

# Configure
export DASHSCOPE_API_KEY="your-api-key"

# Use
./search.sh "latest technology news"
```

## Documentation

See [SKILL.md](./SKILL.md) for full documentation.

## Requirements

- OpenClaw >= 2026.2.0
- Bash shell
- Python 3 (for URL encoding and JSON parsing)
- curl
- Alibaba Cloud DashScope API Key

## License

MIT