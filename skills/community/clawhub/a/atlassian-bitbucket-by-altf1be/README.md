# :bucket: openclaw-skill-atlassian-bitbucket-by-altf1be

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Node.js](https://img.shields.io/badge/Node.js-%3E%3D18-green.svg)](https://nodejs.org/)
[![Bitbucket Cloud](https://img.shields.io/badge/Bitbucket_Cloud-API_2.0-blue.svg)](https://developer.atlassian.com/cloud/bitbucket/rest/intro/)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-orange.svg)](https://clawhub.ai)
[![GitHub last commit](https://img.shields.io/github/last-commit/ALT-F1-OpenClaw/openclaw-skill-atlassian-bitbucket-by-altf1be)](https://github.com/ALT-F1-OpenClaw/openclaw-skill-atlassian-bitbucket-by-altf1be/commits/main)
[![GitHub issues](https://img.shields.io/github/issues/ALT-F1-OpenClaw/openclaw-skill-atlassian-bitbucket-by-altf1be)](https://github.com/ALT-F1-OpenClaw/openclaw-skill-atlassian-bitbucket-by-altf1be/issues)
[![GitHub stars](https://img.shields.io/github/stars/ALT-F1-OpenClaw/openclaw-skill-atlassian-bitbucket-by-altf1be)](https://github.com/ALT-F1-OpenClaw/openclaw-skill-atlassian-bitbucket-by-altf1be/stargazers)

OpenClaw skill for Atlassian Bitbucket Cloud — full CRUD via REST API 2.0

By [Abdelkrim BOUJRAF](https://www.alt-f1.be) / ALT-F1 SRL, Brussels

## Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [API Groups](#api-groups)
- [Authentication](#authentication)
- [Common Options](#common-options)
- [Environment Variables](#environment-variables)
- [Security](#security)
- [License](#license)
- [Author](#author)
- [Links](#links)

## Features

- **335 API endpoints** covering the entire Bitbucket Cloud REST API 2.0
- **23 API groups** — repositories, pull requests, pipelines, issues, and more
- **App Password authentication** — simple, secure, no OAuth flow required
- **Rate-limit retry** with exponential backoff (up to 3 attempts)
- **Pagination support** for all list operations
- **JSON output** for easy integration with other tools and scripts
- **Delete safety** — all destructive operations require explicit `--confirm`
- **Path traversal prevention** for file uploads
- **File size validation** before upload (50 MB default limit)

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/ALT-F1-OpenClaw/openclaw-skill-atlassian-bitbucket-by-altf1be.git
cd openclaw-skill-atlassian-bitbucket-by-altf1be

# 2. Install dependencies
npm install

# 3. Configure environment
cp .env.example .env
# Edit .env with your Bitbucket credentials:
#   BITBUCKET_EMAIL=you@example.com
#   BITBUCKET_API_TOKEN=your-api-token
#   BITBUCKET_WORKSPACE=your-workspace

# 4. Run commands
node scripts/bitbucket.mjs repo-list --workspace my-workspace
node scripts/bitbucket.mjs repo-read --workspace my-workspace --repo my-repo
node scripts/bitbucket.mjs pr-list --workspace my-workspace --repo my-repo
node scripts/bitbucket.mjs pipeline-list --workspace my-workspace --repo my-repo
```

## API Groups

All 335 endpoints organized across 23 API groups:

| # | API Group | Endpoints |
|---|-----------|-----------|
| 1 | Addon | 10 |
| 2 | Branch restrictions | 5 |
| 3 | Branching model | 7 |
| 4 | Commit statuses | 4 |
| 5 | Commits | 16 |
| 6 | Deployments | 16 |
| 7 | Downloads | 4 |
| 8 | GPG | 4 |
| 9 | Issue tracker | 33 |
| 10 | Pipelines | 68 |
| 11 | Projects | 16 |
| 12 | Properties | 12 |
| 13 | Pullrequests | 36 |
| 14 | Refs | 9 |
| 15 | Reports | 9 |
| 16 | Repositories | 26 |
| 17 | Search | 3 |
| 18 | Snippets | 25 |
| 19 | Source | 4 |
| 20 | SSH | 5 |
| 21 | Users | 4 |
| 22 | Webhooks | 2 |
| 23 | Workspaces | 17 |

See [docs/API-COVERAGE.md](./docs/API-COVERAGE.md) for a full breakdown of every endpoint.

## Authentication

This skill uses **Atlassian API Tokens** for authentication (App Passwords were deprecated in September 2025 and will be disabled on June 9, 2026).

### Creating an API Token

1. Log in to your Atlassian account
2. Go to **[API tokens](https://id.atlassian.com/manage-profile/security/api-tokens)**
3. Click **Create API token**
4. Give it a descriptive label (e.g., `openclaw-bitbucket`)
5. Select the scopes your workflows require
6. Click **Create** and copy the generated token

The skill authenticates using HTTP Basic Auth with your Atlassian email and the API token.

> **Legacy support:** Existing App Passwords (`BITBUCKET_USERNAME` + `BITBUCKET_APP_PASSWORD`) are still accepted as a fallback until June 9, 2026. Migrate to API tokens before then.

## Common Options

| Option | Description |
|--------|-------------|
| `--workspace <slug>` | Bitbucket workspace slug |
| `--repo <slug>` | Repository slug |
| `--id <id>` | Resource identifier |
| `--page <n>` | Page number for paginated results |
| `--pagelen <n>` | Number of results per page (default: 50) |
| `--confirm` | Required flag for delete operations |
| `--help` | Show help for any command |

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `BITBUCKET_EMAIL` | Yes | Your Atlassian account email |
| `BITBUCKET_API_TOKEN` | Yes | API token from [id.atlassian.com](https://id.atlassian.com/manage-profile/security/api-tokens) |
| `BITBUCKET_WORKSPACE` | No | Default workspace slug (avoids passing `--workspace` every time) |
| `BITBUCKET_MAX_RESULTS` | No | Maximum results per page (default: `50`) |
| `BITBUCKET_USERNAME` | Legacy | Bitbucket username (fallback, deprecated June 2026) |
| `BITBUCKET_APP_PASSWORD` | Legacy | App password (fallback, deprecated June 2026) |

Create a `.env` file in the project root or export variables in your shell:

```bash
BITBUCKET_EMAIL=you@example.com
BITBUCKET_API_TOKEN=your-api-token
BITBUCKET_WORKSPACE=your-workspace
```

## Security

- API Token authentication (Basic auth, no OAuth flow needed)
- No secrets or tokens printed to stdout
- All delete operations require explicit `--confirm` flag
- Path traversal prevention for file uploads (`safePath()`)
- Built-in rate limiting with exponential backoff retry (3 attempts)
- File size validation before upload (50 MB limit)
- Lazy config validation (credentials only checked when a command runs)

## License

MIT — see [LICENSE](./LICENSE)

## Author

Abdelkrim BOUJRAF — [ALT-F1 SRL](https://www.alt-f1.be), Brussels

- GitHub: [@abdelkrim](https://github.com/abdelkrim)
- X: [@altf1be](https://x.com/altf1be)

## Links

- **Homepage:** [https://www.alt-f1.be](https://www.alt-f1.be)
- **Repository:** [https://github.com/ALT-F1-OpenClaw/openclaw-skill-atlassian-bitbucket-by-altf1be](https://github.com/ALT-F1-OpenClaw/openclaw-skill-atlassian-bitbucket-by-altf1be)
- **Bitbucket REST API docs:** [https://developer.atlassian.com/cloud/bitbucket/rest/intro/](https://developer.atlassian.com/cloud/bitbucket/rest/intro/)
- **Issues:** [https://github.com/ALT-F1-OpenClaw/openclaw-skill-atlassian-bitbucket-by-altf1be/issues](https://github.com/ALT-F1-OpenClaw/openclaw-skill-atlassian-bitbucket-by-altf1be/issues)
