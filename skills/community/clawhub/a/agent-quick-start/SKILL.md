---
name: agent-quick-start
description: Quick start templates for OpenClaw agents. Boilerplate code for research bots, content generators, task automation, and more. Jumpstart your development with ready-to-use templates. Use when starting new OpenClaw projects.
---

# Agent Quick Start

Ready-to-use templates for common OpenClaw agent patterns. Start your project faster.

## Installation

```bash
npx clawhub@latest install agent-quick-start
```

## Usage

```bash
# List available templates
node ~/.openclaw/skills/agent-quick-start/start.js list

# Create a project from a template
node ~/.openclaw/skills/agent-quick-start/start.js create <template_name> <project_path>

# Example: Create a research bot
node ~/.openclaw/skills/agent-quick-start/start.js create research-bot my-research-agent
```

## Available Templates

### 1. Research Bot
- 🤖 Research agent with web search
- 📊 Summarize findings
- 📝 Generate reports
- Use for: Research, data gathering, analysis

### 2. Content Generator
- ✍️ Generate blog posts
- 📱 Social media content
- 📧 Email drafts
- Use for: Content creation, marketing, copywriting

### 3. Task Automator
- ⚡ Automate repetitive tasks
- 🔄 Workflows and pipelines
- 🎯 Scheduled jobs
- Use for: Automation, scripts, workflows

### 4. Customer Support Bot
- 💬 Answer common questions
- 📚 Knowledge base integration
- 🎫 Ticket management
- Use for: Customer service, FAQs, support

### 5. Data Processor
- 📊 Process data files
- 📈 Analysis and reports
- 💾 ETL operations
- Use for: Data processing, analytics, ETL

## Features

- ✅ Ready-to-use templates
- ✅ Copy to any directory
- ✅ Clear documentation
- ✅ Best practices included
- ✅ Easy to customize

## Example Workflow

```bash
# 1. List templates
node ~/.openclaw/skills/agent-quick-start/start.js list

# 2. Choose a template
node ~/.openclaw/skills/agent-quick-start/start.js create research-bot ./my-bot

# 3. Customize the project
cd ./my-bot
# Edit files, add your logic

# 4. Run your agent
openclaw run
```

## Need Help?

If you need help with OpenClaw:
- 📧 **Installation Service**: ¥99-299
- 🔗 **Landing Page**: https://yang1002378395-cmyk.github.io/openclaw-install-service/

## License

MIT
