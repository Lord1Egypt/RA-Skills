---
name: checkly-cli-skills
description: Comprehensive Checkly CLI command reference and Monitoring as Code workflows. Use when user mentions Checkly CLI, monitoring as code, synthetic monitoring, API checks, browser checks, Playwright testing, check deployment, or npx checkly commands. Routes to specialized sub-skills for auth, config, checks, testing, deployment, imports, constructs, and advanced patterns. Triggers on checkly, monitoring as code, synthetic monitoring, checkly cli, npx checkly.
metadata:
  {
    "openclaw":
      {
        "emoji": "✓",
        "requires": { "bins": ["checkly", "npx"], "env": ["CHECKLY_API_KEY", "CHECKLY_ACCOUNT_ID"] },
        "primaryEnv": "CHECKLY_API_KEY",
        "install":
          [
            {
              "id": "npm-create",
              "kind": "node",
              "package": "checkly",
              "bins": ["checkly"],
              "label": "Create Checkly project (npm)",
              "command": "npm create checkly@latest",
            },
            {
              "id": "npm-global",
              "kind": "npm",
              "package": "checkly",
              "bins": ["checkly"],
              "label": "Install Checkly CLI globally (npm)",
            },
          ],
        "notes":
          [
            "Requires Checkly account and API key (signup at checklyhq.com/signup or via 'npx checkly login').",
            "Credentials can be set via environment variables (CHECKLY_API_KEY, CHECKLY_ACCOUNT_ID) or stored in ~/.config/@checkly/cli/config.json via 'npx checkly login'.",
            "Config stored in checkly.config.ts and auth credentials in system config.",
            "Browser checks optionally require playwright binary and @playwright/test dependency.",
          ],
      },
  }
---

# Checkly CLI Skills

Comprehensive Checkly CLI command reference and Monitoring as Code (MaC) workflows.

## Quick start

```bash
# Create new Checkly project
npm create checkly@latest

# Test checks locally
npx checkly test

# Deploy to Checkly cloud
npx checkly deploy
```

## What is Monitoring as Code?

The Checkly CLI provides a TypeScript/JavaScript-native workflow for coding, testing, and deploying synthetic monitoring at scale. Define your monitoring checks as code, test them locally, version control them with Git, and deploy through CI/CD pipelines.

**Key benefits:**
- **Codeable** - Define checks in TypeScript/JavaScript
- **Testable** - Run checks locally before deployment
- **Reviewable** - Code review your monitoring in PRs
- **Native Playwright** - Use standard @playwright/test specs
- **CI/CD Native** - Integrate with your deployment pipeline

## Skill organization

This skill routes to specialized sub-skills by Checkly domain:

**Getting Started:**
- `checkly-auth` - Authentication setup and login
- `checkly-config` - Configuration files (checkly.config.ts) and project structure
- `checkly-members` - Account member and pending-invite listing, role updates, and removals

**Core Workflows:**
- `checkly-test` - Local testing workflow with npx checkly test
- `checkly-deploy` - Deployment to Checkly cloud
- `checkly-import` - Import existing checks from Checkly to code

**Check Types:**
- `checkly-checks` - API checks, browser checks, multi-step checks
- `checkly-monitors` - Heartbeat, TCP, DNS, URL monitors
- `checkly-groups` - Check groups for organization and shared config

**Advanced:**
- `checkly-constructs` - Constructs system and resource management
- `checkly-playwright` - Playwright test suites and configuration
- `checkly-advanced` - Retry strategies, reporters, environment variables, bundling

**Operations:**
- `checkly-members` - Audit and manage Checkly account access with `npx checkly members`
- `checkly-test` - Also covers `npx checkly test-sessions` for recorded test-session drilldown and RCA context
- `checkly-checks` - Inspect and delete deployed checks with `npx checkly checks`; use `checks delete --dry-run` before destructive deletes
- `checkly-assets` - List/download result assets such as logs, traces, videos, screenshots, pcap, reports, and files for failure investigation

## When to use Checkly CLI vs Web UI

**Use Checkly CLI when:**
- Defining monitoring as part of your codebase
- Automating check creation/updates in CI/CD
- Testing checks locally during development
- Version controlling monitoring configuration
- Managing multiple checks efficiently
- Integrating monitoring with application deployments

**Use Web UI when:**
- Exploring Checkly for the first time
- Viewing dashboards and historical results
- Analyzing check failures and incidents
- Managing account-level settings
- Configuring alert channels (email, Slack App, PagerDuty)
- Setting up private locations

## Common workflows

### New project setup

```bash
# Initialize project
npm create checkly@latest
cd my-checkly-project

# Authenticate
npx checkly login

# Test locally
npx checkly test

# Deploy to cloud
npx checkly deploy
```

### Daily development

```bash
# Create new API check
cat > __checks__/api-status.check.ts <<'EOF'
import { ApiCheck, AssertionBuilder } from 'checkly/constructs'

new ApiCheck('api-status-check', {
  name: 'API Status Check',
  request: {
    url: 'https://api.example.com/status',
    method: 'GET',
    assertions: [
      AssertionBuilder.statusCode().equals(200),
      AssertionBuilder.responseTime().lessThan(500),
    ],
  },
})
EOF

# Test locally
npx checkly test

# Deploy when ready
npx checkly deploy
```

### Browser check with Playwright

```bash
# Create browser check
cat > __checks__/homepage.spec.ts <<'EOF'
import { test, expect } from '@playwright/test'

test('homepage loads', async ({ page }) => {
  const response = await page.goto('https://example.com')
  expect(response?.status()).toBeLessThan(400)
  await expect(page).toHaveTitle(/Example/)
  await page.screenshot({ path: 'homepage.jpg' })
})
EOF

# Test with Playwright locally (faster)
npx playwright test __checks__/homepage.spec.ts

# Test via Checkly runtime
npx checkly test __checks__/homepage.spec.ts

# Deploy
npx checkly deploy
```

### Import existing checks

```bash
# Import all checks from Checkly account
npx checkly import plan

# Review generated code
git diff

# Commit imported checks
git add .
git commit -m "Import existing monitoring checks"
```

### Inspect deployed check failures

```bash
# List failing checks
npx checkly checks list --status failing

# Inspect a deployed check and recent runs
npx checkly checks get <check-id>
npx checkly checks get <check-id> --output json

# Drill into an error group or specific result
npx checkly checks get <check-id> --error-group <error-group-id>
npx checkly checks get <check-id> --result <result-id>
```

When investigating a deployed failure, look for `errorGroups`, `rootCause`, or `RCA` fields in the output. If Checkly already surfaced Rocky AI root-cause analysis, reuse that context before suggesting additional debugging steps.

For alerting questions, use read-only JSON/API evidence before table output:

```bash
npx checkly checks get <check-id> --output json
npx checkly api /v1/checks/<check-id>
npx checkly alert-channels list --output json --limit 100
```

Only fetch alert-channel details for channel IDs referenced by the selected check or matching group. If the check has a `groupId`, inspect groups once with `npx checkly api /v1/check-groups` and locate the matching group. Do not probe guessed account/global alerting endpoints; if output only shows `useGlobalAlertSettings: true`, say global alert settings are selected but their policy details were not available in the inspected CLI/API output.

## Decision Trees

### "What type of check should I create?"

```
What are you monitoring?
├─ REST API / HTTP endpoint
│  ├─ Simple availability → API Check (request + status assertion)
│  ├─ Complex validation → API Check (request + multiple assertions + scripts)
│  └─ Just uptime/ping → URL Monitor (simpler, faster)
│
├─ Web application / User flow
│  ├─ Single page → Browser Check (one .spec.ts file)
│  ├─ Multiple steps → Browser Check or Multi-Step Check
│  └─ Full test suite → Playwright Check Suite (playwright.config.ts)
│
└─ Service health / Infrastructure
   ├─ Periodic heartbeat → Heartbeat Monitor
   ├─ TCP port → TCP Monitor
   ├─ DNS record → DNS Monitor
   └─ Simple HTTP → URL Monitor
```

**Quick reference:**
- **API Check**: HTTP requests with assertions (status, headers, body, response time)
- **Browser Check**: Single Playwright spec file for web testing
- **Multi-Step Check**: Complex browser workflows (legacy, use Browser Check instead)
- **Playwright Check Suite**: Multiple Playwright tests with projects/parallelization
- **Monitors**: Simple health checks without code execution

### "Test locally or deploy?"

```
What stage are you at?
├─ Developing new check
│  ├─ Browser check → npx playwright test (fastest iteration)
│  └─ API check → npx checkly test (includes assertions)
│
├─ Ready to validate
│  └─ npx checkly test (runs in Checkly runtime, catches issues)
│
└─ Ready for production
   └─ npx checkly deploy (schedule checks to run continuously)
```

**Testing hierarchy:**
1. `npx playwright test` - Fastest, local Playwright execution (browser checks only)
2. `npx checkly test` - Validates in Checkly runtime, catches compatibility issues
3. `npx checkly deploy` - Deploys for continuous scheduled monitoring

### "File-based or construct-based checks?"

```
How do you want to define checks?
├─ Auto-discovery (convention over configuration)
│  ├─ Browser checks → *.spec.ts files matching testMatch pattern
│  ├─ Multi-step → *.check.ts files with MultiStepCheck construct
│  └─ API checks → *.check.ts files with ApiCheck construct
│
└─ Explicit definition
   ├─ Programmatic → Construct instances in .check.ts files
   └─ Full control → Playwright Check Suite with playwright.config.ts
```

**Patterns:**
- **Auto-discovery**: Configure `checks.browserChecks.testMatch` in checkly.config.ts
- **Explicit constructs**: Import from `checkly/constructs` and instantiate
- **Playwright projects**: Define multiple test suites with different configs

### "Where should configuration go?"

```
What are you configuring?
├─ Project-level (all checks)
│  └─ checkly.config.ts → defaults, locations, frequency, runtime
│
├─ Group-level (related checks)
│  └─ CheckGroup construct → shared settings for subset of checks
│
└─ Check-level (individual)
   └─ Check constructor → override defaults for specific check
```

**Configuration hierarchy** (specific overrides general):
1. Check-level properties (highest priority)
2. CheckGroup properties
3. checkly.config.ts defaults
4. Checkly account defaults (lowest priority)

## Project structure

Typical Checkly CLI project:

```
my-monitoring-project/
├── checkly.config.ts          # Project configuration
├── __checks__/                # Check definitions
│   ├── api.check.ts           # API check construct
│   ├── homepage.spec.ts       # Browser check (auto-discovered)
│   ├── login.spec.ts          # Another browser check
│   └── utils/
│       ├── alert-channels.ts  # Shared alert channel definitions
│       └── helpers.ts         # Shared helper functions
├── playwright.config.ts       # Playwright configuration (optional)
├── package.json
└── node_modules/
    └── checkly/               # CLI package with constructs
```

## Installation methods

### New project (recommended)

```bash
npm create checkly@latest
```

Creates scaffolded project with:
- `checkly.config.ts` with sensible defaults
- Example checks in `__checks__/` directory
- `package.json` with checkly dependency
- `.gitignore` configured

### Existing project

```bash
# Install as dev dependency
npm install --save-dev checkly

# Create configuration file
npx checkly init
```

### Global installation (not recommended)

```bash
npm install -g checkly
checkly test
```

**Note**: Use `npx checkly` instead for project-specific CLI version.

## Related Skills

**Getting started:**
- See `checkly-auth` for authentication setup
- See `checkly-config` for project configuration
- See `checkly-test` for local testing workflow

**Creating checks:**
- See `checkly-checks` for API and browser checks
- See `checkly-monitors` for simpler health checks
- See `checkly-playwright` for full test suite setup

**Advanced workflows:**
- See `checkly-deploy` for deployment strategies
- See `checkly-constructs` for understanding the object model
- See `checkly-advanced` for retry strategies and reporters

**Import existing:**
- See `checkly-import` to migrate from web UI to code
