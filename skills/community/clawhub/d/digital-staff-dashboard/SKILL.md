---
name: agent-dashboard-v2
description: A modern web-based dashboard for managing OpenClaw agents with real-time monitoring, token usage tracking, skill management, and multi-language support. Provides a visual interface for agent operations, subagent dispatch management, and comprehensive statistics.
metadata:
  openclaw:
    emoji: "📊"
---

# Agent Dashboard V2

A modern, feature-rich web dashboard for OpenClaw agent management with real-time monitoring, token usage tracking, and comprehensive agent operations.

## Features

- 📊 **Real-time Monitoring**: Monitor agent status, token usage, and session statistics
- 🎨 **Modern UI**: Dark theme with beautiful animations and responsive design
- 🛠️ **Skill Management**: Enable/disable skills for each agent with blacklist support
- 🔀 **Subagent Dispatch**: Visual management of agent delegation and permissions
- 🤖 **Agent Creation**: Create new agents with guided configuration
- 🌐 **Multi-language**: Automatic language detection (English/Chinese)
- 🌤️ **Weather Widget**: Real-time local weather and time display
- 📱 **Responsive Design**: Works on desktop and mobile devices

## Installation

### Quick Install

```bash
npx skills add mikezhuyan/agent-dashboard@agent-dashboard-v2
```

### Manual Installation

```bash
# Clone the repository
git clone https://github.com/mikezhuyan/agent-dashboard.git ~/.agents/skills/agent-dashboard-v2

# Navigate to the directory
cd ~/.agents/skills/agent-dashboard-v2

# Install (optional - creates systemd service)
./install.sh
```

## Usage

### Starting the Dashboard

```bash
# Run directly
python3 dashboard_server.py

# Or use the installed service
systemctl --user start agent-dashboard
```

### Access

Open your browser and navigate to:
```
http://localhost:5181
```

### Dashboard Features

#### 1. Agent Grid View
- View all agents with status indicators
- Drag to reorder agent cards
- Click cards to view details in sidebar
- Multiple view modes (grid, horizontal, list)

#### 2. Skill Management
- Click the 🛠️ icon on any agent card
- Enable/disable skills per agent
- Automatic blacklist/whitelist management
- View all available skills

#### 3. Subagent Dispatch
- Click "调度管理" (Manage Dispatch)
- Select a dispatcher agent
- Configure allowed subagents
- Set max concurrent tasks

#### 4. Create New Agent
- Click "新建 Agent" (Create Agent)
- Configure agent ID, name, emoji, color theme
- Select model provider and model
- Set system prompt

#### 5. Settings
- Click "设置" (Settings)
- Customize dashboard title and subtitle
- Configure auto-refresh interval
- Set token cost estimates
- Show/hide cost information

## Configuration

The dashboard reads configuration from:
- `~/.openclaw/openclaw.json` - OpenClaw global config
- `~/.config/agent-dashboard/config.json` - Dashboard settings (auto-created)

### Environment Variables

```bash
OPENCLAW_HOME=/home/user/.openclaw  # Path to OpenClaw installation
DASHBOARD_PORT=5181                  # Dashboard server port
```

## Architecture

- **Backend**: Flask (Python 3)
- **Frontend**: Vanilla JavaScript + CSS
- **Data Source**: OpenClaw JSON configuration
- **Authentication**: Inherits OpenClaw authentication

## API Endpoints

The dashboard provides REST API endpoints:

```
GET  /api/agents              # List all agents
POST /api/agents              # Create new agent
GET  /api/agents/<name>       # Get agent details
DELETE /api/agents/<name>     # Delete agent
GET  /api/skills              # List all skills
GET  /api/agents/<name>/skills # Get agent skills
POST /api/agents/<name>/skills/<id>/enable
POST /api/agents/<name>/skills/<id>/disable
GET  /api/stats               # Get statistics
```

## Requirements

- Python 3.8+
- OpenClaw installed and configured
- Modern web browser

## File Structure

```
agent-dashboard/
├── dashboard_server.py      # Flask backend
├── openclaw_config.py       # OpenClaw config manager
├── openclaw_skills.py       # Skills management
├── openclaw_finder.py       # OpenClaw path finder
├── openclaw_schema.py       # Config validation
├── static/
│   ├── css/style.css        # Styles
│   ├── js/app.js            # Frontend logic
│   └── js/i18n.js           # Internationalization
├── install.sh               # Installation script
└── SKILL.md                 # This file
```

## Troubleshooting

### Port Already in Use
```bash
# Find and kill process using port 5181
lsof -ti:5181 | xargs kill -9
# Or use a different port
DASHBOARD_PORT=8080 python3 dashboard_server.py
```

### Cannot Find OpenClaw
```bash
# Set environment variable
export OPENCLAW_HOME=/path/to/.openclaw
```

### Permission Denied
```bash
# Fix permissions
chmod +x install.sh
chmod 644 static/*
```

## Updating

```bash
cd ~/.agents/skills/agent-dashboard-v2
git pull origin main
# Restart service if using systemd
systemctl --user restart agent-dashboard
```

## Uninstallation

```bash
# Stop service
systemctl --user stop agent-dashboard
systemctl --user disable agent-dashboard

# Remove files
rm -rf ~/.agents/skills/agent-dashboard-v2
rm -f ~/.config/systemd/user/agent-dashboard.service
```

## License

MIT

## Author

@mikezhuyan

## Support

For issues and feature requests, visit:
https://github.com/mikezhuyan/agent-dashboard/issues
