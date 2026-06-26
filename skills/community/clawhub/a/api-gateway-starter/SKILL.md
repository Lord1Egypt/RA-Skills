# API Gateway Starter

Production-ready API Gateway with everything you need.

## Features

- **Authentication** - JWT, OAuth2, API keys
- **Rate Limiting** - Per-user, per-endpoint
- **Caching** - Redis integration
- **Monitoring** - Request logs, metrics
- **Load Balancing** - Multiple upstream support
- **SSL/TLS** - Automatic cert management

## Quick Start

```bash
# Start gateway
./gateway.sh start

# Add upstream
./gateway.sh add http://localhost:3000

# Configure auth
./gateway.sh auth jwt --secret your-secret
```

## Configuration

Edit `config.yaml` to customize:
- Ports
- Upstreams
- Auth methods
- Rate limits

## Requirements

- Node.js 18+
- Redis (optional)

## Author

Sunshine-del-ux
