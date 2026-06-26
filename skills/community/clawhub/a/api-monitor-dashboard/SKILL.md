# API Monitor Dashboard

Real-time API monitoring and alerting system.

## Features

- Real-time uptime monitoring
- Response time tracking
- Error rate alerts
- Custom health checks
- Email/Slack notifications
- Historical data
- Auto-recovery detection

## Usage

```bash
# Start monitoring
./monitor.sh start

# Add endpoint
./monitor.sh add https://api.example.com/health

# Check status
./monitor.sh status
```

## Dashboard

Open browser to view dashboard:
```
http://localhost:3000
```

## Configuration

Edit `config.json` to customize:
- Check intervals
- Timeout settings
- Alert thresholds
- Notification channels

## Requirements

- Node.js 18+
- Docker (optional)

## Author

Sunshine-del-ux
