# api-mock-server

## Overview

A lightweight API mock server for rapid prototyping, testing, and frontend-backend decoupling.

## Features

- **Zero-config startup**: One command to serve mock endpoints
- **JSON/Schema responses**: Static or dynamic response generation
- **Request validation**: Validate incoming requests against JSON Schema
- **Dynamic data**: Use Faker to generate realistic test data
- **Latency simulation**: Add artificial delays to simulate real networks
- **Webhook simulation**: Trigger callbacks after receiving requests
- **Config-driven**: Define all routes in a single JSON file

## Quick Start

```bash
# Install
pip install -r requirements.txt

# Start with a config file
python scripts/mock_server.py --config examples/routes.json

# Or start with inline routes
python scripts/mock_server.py --route GET /hello '{"message":"hello"}'
```

## Config Format

```json
{
  "routes": [
    {
      "method": "GET",
      "path": "/users",
      "response": {
        "users": [
          {"id": 1, "name": "Alice"},
          {"id": 2, "name": "Bob"}
        ]
      }
    },
    {
      "method": "POST",
      "path": "/users",
      "validate": {
        "required": ["name"],
        "properties": {
          "name": {"type": "string"}
        }
      },
      "response": {"id": 3, "created": true}
    }
  ],
  "latency": 100,
  "port": 3000
}
```

## CLI Commands

| Command | Description |
|---------|-------------|
| `--config <file>` | Load routes from JSON file |
| `--port <port>` | Server port (default: 3000) |
| `--latency <ms>` | Add artificial latency |
| `--route <method> <path> <response>` | Add inline route |

## Examples

See `examples/basic_usage.py` for programmatic usage.

## Testing

```bash
python -m pytest tests/ -v
```

## 中文说明

轻量级API Mock服务器，用于前后端分离开发、自动化测试和原型验证。

### 快速开始

```bash
python scripts/mock_server.py --config examples/routes.json --port 3000
```

## License

MIT License
