# ClawVet

[![CI](https://github.com/MohibShaikh/clawvet/actions/workflows/ci.yml/badge.svg)](https://github.com/MohibShaikh/clawvet/actions/workflows/ci.yml)
[![npm](https://img.shields.io/npm/v/clawvet)](https://www.npmjs.com/package/clawvet)
[![npm downloads](https://img.shields.io/npm/dw/clawvet)](https://www.npmjs.com/package/clawvet)

Skill vetting & supply chain security for the OpenClaw ecosystem. Scans SKILL.md files for prompt injection, credential theft, remote code execution, typosquatting, and social engineering — catching threats that VirusTotal misses.

## Why

In Feb 2026 researchers found 824+ malicious skills (~20% of ClawHub). The "ClawHavoc" campaign distributed infostealers via fake skills. ClawVet runs 6 independent analysis passes on every skill to catch what single-pass scanners miss.

## Quick Start

```bash
# Scan a local skill
npx clawvet scan ./my-skill/

# JSON output for CI/CD
npx clawvet scan ./my-skill/ --format json --fail-on high

# Audit all installed skills
npx clawvet audit
```

## Architecture

```
clawvet/
├── apps/
│   ├── api/          # Fastify backend (scanner engine, REST API, BullMQ worker)
│   └── web/          # Next.js 14 dashboard
├── packages/
│   ├── cli/          # `clawvet` CLI tool
│   └── shared/       # Types + scanner engine + 54 threat detection patterns
├── docker-compose.yml
└── turbo.json
```

## 6-Pass Scanner Engine

| Pass | Module | What it catches |
|------|--------|-----------------|
| 1 | `skill-parser` | Parses YAML frontmatter, extracts code blocks, URLs, IPs, domains |
| 2 | `static-analysis` | 54 regex patterns: RCE, reverse shells, credential theft, obfuscation, exfiltration |
| 3 | `metadata-validator` | Undeclared binaries/env vars, missing/vague descriptions, bad semver |
| 4 | `semantic-analysis` | Claude AI analyzes instructions for social engineering & prompt injection |
| 5 | `dependency-checker` | npx -y auto-install, global npm installs, risky packages |
| 6 | `typosquat-detector` | Levenshtein distance against top ClawHub skills |

## Risk Scoring

- Each **critical** finding: +30 points
- Each **high** finding: +15 points
- Each **medium** finding: +7 points
- Each **low** finding: +3 points
- Score capped at 100. Grades: A (0-10), B (11-25), C (26-50), D (51-75), F (76-100)

## API

```
POST   /api/v1/scans          # Submit skill content for scanning
GET    /api/v1/scans/:id      # Get scan result
GET    /api/v1/scans           # List scans (paginated)
GET    /api/v1/stats           # Public stats
POST   /api/v1/webhooks        # Register webhook
DELETE /api/v1/webhooks/:id    # Remove webhook
GET    /api/v1/auth/github     # GitHub OAuth flow
```

## Development

```bash
# Install deps
npm install

# Run tests (61 tests across 6 suites)
cd apps/api && npx vitest run

# Start API server
cd apps/api && npm run dev

# Start web dashboard
cd apps/web && npm run dev

# Start Postgres + Redis
docker-compose up -d

# Push DB schema
cd apps/api && npm run db:push
```

## Environment Variables

Copy `.env.example` to `.env`:

```
DATABASE_URL=postgres://clawvet:clawvet@localhost:5432/clawvet
REDIS_URL=redis://localhost:6379
ANTHROPIC_API_KEY=sk-ant-...    # For AI semantic analysis
GITHUB_CLIENT_ID=               # For OAuth
GITHUB_CLIENT_SECRET=
```

## Tests

61 tests covering:
- All 6 fixture skills (benign → malicious)
- Edge cases (empty files, malformed YAML, unicode, 100KB adversarial input)
- Regex catastrophic backtracking safety
- 54 threat patterns across 12 categories
- API route validation (auth, webhooks, scans)
- CLI end-to-end integration (--format json, --fail-on, exit codes)

## License

MIT
