# ClawStatus

A real-time monitoring dashboard for [OpenClaw](https://github.com/anthropics/OpenClaw) ecosystem projects. Track devices, agents, sessions, cron jobs, models, and token usage across your entire OpenClaw deployment.

## Features

- **Device Monitoring** - Track online status and health of all connected devices
- **Agent Status** - Real-time visibility into running agents and subagents
- **Session Management** - View active sessions with detailed statistics
- **Cron Job Tracking** - Monitor scheduled tasks and their execution status
- **Model Overview** - Display available models and their configurations
- **Token Usage Analytics** - 15-day token consumption trends with daily breakdown
- **Multi-language Support** - English and Chinese interface
- **Single-file Deployment** - No complex dependencies, easy to deploy anywhere

## Installation

```bash
pip install --user -e .
```

## Usage

```bash
clawstatus --host 0.0.0.0 --port 8900 --no-debug
```

## Service Management (systemd --user)

```bash
systemctl --user restart clawstatus.service
systemctl --user status clawstatus.service
```

## License

MIT
