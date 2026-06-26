# openclaw-skill-atlassian-jira

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Node.js](https://img.shields.io/badge/Node.js-%3E%3D18-green.svg)](https://nodejs.org/)
[![Jira Cloud](https://img.shields.io/badge/Jira-Cloud-blue.svg?logo=jira)](https://www.atlassian.com/software/jira)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-orange.svg)](https://clawhub.ai)
[![ClawHub](https://img.shields.io/badge/ClawHub-atlassian--jira--by--altf1be-orange)](https://clawhub.ai/skills/atlassian-jira-by-altf1be)
[![GitHub last commit](https://img.shields.io/github/last-commit/ALT-F1-OpenClaw/openclaw-skill-atlassian-jira)](https://github.com/ALT-F1-OpenClaw/openclaw-skill-atlassian-jira/commits/main)
[![GitHub issues](https://img.shields.io/github/issues/ALT-F1-OpenClaw/openclaw-skill-atlassian-jira)](https://github.com/ALT-F1-OpenClaw/openclaw-skill-atlassian-jira/issues)
[![GitHub stars](https://img.shields.io/github/stars/ALT-F1-OpenClaw/openclaw-skill-atlassian-jira)](https://github.com/ALT-F1-OpenClaw/openclaw-skill-atlassian-jira/stargazers)

OpenClaw skill for Atlassian Jira Cloud — CRUD issues, comments, attachments, workflow transitions, and JQL search via Jira REST API v3.

By [Abdelkrim BOUJRAF](https://www.alt-f1.be) / ALT-F1 SRL, Brussels 🇧🇪 🇲🇦

## Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Setup](#setup)
- [Commands](#commands)
- [Security](#security)
- [ClawHub](#clawhub)
- [License](#license)
- [Author](#author)
- [Contributing](#contributing)

## Features

- **Issues** — Create, read, update, delete, list, and search (JQL)
- **Comments** — Add, update, delete, and list
- **Attachments** — Upload, list, and delete
- **Workflow Transitions** — List available transitions and move issues through workflow states
- **Security** — `--confirm` required for deletes, no secrets to stdout, rate-limit retry with backoff
- **Auth** — Email + API token (Basic auth)

## Quick Start

```bash
# 1. Clone
git clone https://github.com/ALT-F1-OpenClaw/openclaw-skill-atlassian-jira.git
cd openclaw-skill-atlassian-jira

# 2. Install
npm install

# 3. Configure
cp .env.example .env
# Edit .env with your Jira Cloud credentials

# 4. Use
node scripts/jira.mjs list --project PROJ
node scripts/jira.mjs create --project PROJ --summary "My first issue"
node scripts/jira.mjs read --key PROJ-1
```

## Setup

1. Go to https://id.atlassian.com/manage-profile/security/api-tokens
2. Create an API token
3. Copy `.env.example` to `.env` and fill in:
   - `JIRA_HOST` — your Jira Cloud instance (e.g. `yourcompany.atlassian.net`)
   - `JIRA_EMAIL` — your Atlassian account email
   - `JIRA_API_TOKEN` — the API token you just created
   - `JIRA_DEFAULT_PROJECT` — (optional) default project key

## Commands

See [SKILL.md](./SKILL.md) for full command reference.

## Security

- Email + API token auth (Basic auth via base64 encoding)
- No secrets or tokens printed to stdout
- All delete operations require explicit `--confirm` flag
- Built-in rate limiting with exponential backoff retry
- Lazy config validation (only checked when a command runs)

## ClawHub

Published as: `atlassian-jira-by-altf1be`

```bash
clawhub install atlassian-jira-by-altf1be
```

## License

MIT — see [LICENSE](./LICENSE)

## Author

Abdelkrim BOUJRAF — [ALT-F1 SRL](https://www.alt-f1.be), Brussels 🇧🇪 🇲🇦
- GitHub: [@abdelkrim](https://github.com/abdelkrim)
- X: [@altf1be](https://x.com/altf1be)

## Contributing

Contributions welcome! Please open an issue or PR.
