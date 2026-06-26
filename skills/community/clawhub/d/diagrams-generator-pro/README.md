# 📊 Diagrams Generator (Pro)

Professional diagram generation skill for AI agents. Generate cloud architecture diagrams, data charts, academic figures, and more.

**💰 Pricing: 0.001 USDT per generation** (via [SkillPay](https://skillpay.me))

## Features

- ☁️ **Cloud Architecture Diagrams** - AWS, GCP, Azure, Kubernetes
- 📈 **Data Visualization** - Bar charts, line charts, pie charts, scatter plots
- 🔬 **Academic Figures** - Neural networks, model architectures (TikZ/LaTeX)
- 🔄 **Flow Diagrams** - State machines, decision trees, process flows
- 🌐 **Network Topology** - Relationship graphs, knowledge graphs

## Installation

### Via ClawHub CLI

```bash
# Install the skill
clawhub install diagrams-generator

# Or search and install
clawhub search diagrams
```

### Manual Installation

Copy the skill folder to your OpenClaw skills directory:
- macOS: `~/Library/Application Support/OpenClaw/skills/`
- Linux: `~/.config/openclaw/skills/`
- Windows: `%APPDATA%\OpenClaw\skills\`

## Prerequisites

```bash
# Required: Graphviz
brew install graphviz  # macOS
apt-get install graphviz  # Linux

# Required: Python libraries
pip install diagrams matplotlib seaborn plotly networkx requests

# Optional: LaTeX (for academic-grade figures)
brew install --cask mactex  # macOS, full version
```

## Usage

Simply ask your AI agent to generate diagrams:

```
"画一个 AWS 微服务架构图"
"Create a GCP data pipeline diagram"
"画一个神经网络架构图"
"Generate a flowchart for user registration"
```

## Payment

This skill uses [SkillPay](https://skillpay.me) for monetization.

- **Price**: 0.001 USDT per diagram
- **Settlement**: Instant (BNB Chain)
- **No KYC required** for users

Payment is automatically verified before each diagram generation.

## Files

- `SKILL.md` - Main skill definition and workflow
- `payment.py` - SkillPay payment module
- `references/diagrams-api.md` - Node import reference
- `references/styling-guide.md` - Styling best practices

## Supported Diagram Types

| Type | Tool | Quality |
|------|------|---------|
| Cloud Architecture | `diagrams` | ★★★★ |
| Data Charts | `matplotlib` | ★★★ |
| Statistical Charts | `seaborn` | ★★★★ |
| Interactive Charts | `plotly` | ★★★★ |
| Flow Diagrams | `graphviz` | ★★★ |
| Network Topology | `networkx` | ★★★ |
| Academic Figures | `TikZ/LaTeX` | ★★★★★ |

## License

MIT License

## Support

For issues or feature requests, please contact the skill author.

---

*Powered by [SkillPay](https://skillpay.me) - AI Skill Monetization Infrastructure*
