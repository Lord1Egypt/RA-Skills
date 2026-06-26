#!/usr/bin/env bash
set -euo pipefail

# generate-demo.sh — Generate a synthetic broken agent session and diagnose it
#
# Creates a realistic-looking session with multiple failure patterns baked in,
# then runs diagnose → prescribe so you can see clawdoc in action immediately.
#
# Usage:
#   bash dev/generate-demo.sh              # generate + diagnose + prescribe
#   bash dev/generate-demo.sh --json-only  # just output the JSONL to stdout
#
# No real agent sessions required. No data leaves your machine.

VERSION="0.12.0"

usage() {
  cat <<EOF
Usage: generate-demo.sh [--help|--version|--json-only]

Description:
  Generates a synthetic broken agent session and runs the full
  clawdoc diagnostic pipeline against it. The session contains
  6 intentional failure patterns so you can see every severity
  level and prescription type.

Options:
  --help       Show this help message and exit
  --version    Show version and exit
  --json-only  Output only the raw JSONL session (no diagnosis)

Patterns embedded:
  P1  Infinite retry loop     (8 identical exec calls)
  P4  Context exhaustion      (tokens climb to 78%)
  P6  Cost spike              (expensive turns from retries)
  P12 Task drift / exploration (10 consecutive reads, no edits)
  P13 Unbounded walk          (3 unscoped find/grep commands)
  P14 Tool misuse             (same file read 4 times without edit)

Example:
  bash dev/generate-demo.sh
  bash dev/generate-demo.sh --json-only > my-demo.jsonl
EOF
}

if [[ "${1:-}" == "--help" ]]; then usage; exit 0; fi
if [[ "${1:-}" == "--version" ]]; then echo "$VERSION"; exit 0; fi

JSON_ONLY=0
if [[ "${1:-}" == "--json-only" ]]; then JSON_ONLY=1; fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
DIAGNOSE="$ROOT_DIR/scripts/diagnose.sh"
PRESCRIBE="$ROOT_DIR/scripts/prescribe.sh"
EXAMINE="$ROOT_DIR/scripts/examine.sh"

# Check dependencies
if ! command -v jq >/dev/null 2>&1; then
  echo "Error: required dependency 'jq' not found." >&2
  exit 1
fi

DEMO_FILE=$(mktemp /tmp/clawdoc-demo.XXXXXX)
trap 'rm -f "$DEMO_FILE"' EXIT

# ═══════════════════════════════════════════════════════════════
# Generate the synthetic session
# ═══════════════════════════════════════════════════════════════
#
# Story: An agent is asked to "find and fix all TODO comments in the project."
# What goes wrong:
#   1. It reads the same file repeatedly without editing it (P14)
#   2. It runs unscoped find and grep commands (P13)
#   3. It enters a retry loop running a broken lint command (P1)
#   4. It reads 10+ files without making any edits (P12)
#   5. Context and cost accumulate (P4, P6)

cat > "$DEMO_FILE" <<'ENDSESSION'
{"type":"session","timestamp":"2026-03-16T14:00:00.000Z","sessionId":"demo-broken-session","agentId":"main","model":"anthropic/claude-sonnet-4-6","sessionKey":"agent:main:main"}
{"type":"message","timestamp":"2026-03-16T14:00:05.000Z","message":{"role":"user","content":[{"type":"text","text":"Find and fix all TODO comments in the project. There are known TODOs in src/auth.ts, src/api/routes.ts, and src/utils.ts."}]}}
{"type":"message","timestamp":"2026-03-16T14:00:30.000Z","message":{"role":"assistant","content":[{"type":"text","text":"I'll start by finding all TODO comments in the project."},{"type":"toolCall","id":"tc_001","name":"exec","input":{"command":"grep -r 'TODO' /"}}],"usage":{"inputTokens":3000,"outputTokens":35,"cost":{"total":0.00975}}}}
{"type":"message","timestamp":"2026-03-16T14:01:00.000Z","message":{"role":"toolResult","content":[{"type":"text","text":"/Users/dev/project/src/auth.ts:  // TODO: add password hashing\n/Users/dev/project/src/api/routes.ts:  // TODO: add rate limiting\n/Users/dev/project/src/utils.ts:  // TODO: handle edge case for empty input\n/Users/dev/project/src/db.ts:  // TODO: add connection pooling\n/Users/dev/project/src/config.ts:  // TODO: load from env vars\n/Users/dev/project/tests/auth.test.ts:  // TODO: add negative test\n/var/log/syslog:TODO: rotate logs\n/usr/share/doc/bash/TODO"}]}}
{"type":"message","timestamp":"2026-03-16T14:01:30.000Z","message":{"role":"assistant","content":[{"type":"text","text":"Found several TODOs. Let me also search for FIXME and HACK comments."},{"type":"toolCall","id":"tc_002","name":"exec","input":{"command":"find / -type f -name '*.ts' -exec grep -l 'TODO\\|FIXME\\|HACK' {} \\;"}}],"usage":{"inputTokens":6000,"outputTokens":40,"cost":{"total":0.01920}}}}
{"type":"message","timestamp":"2026-03-16T14:02:00.000Z","message":{"role":"toolResult","content":[{"type":"text","text":"/Users/dev/project/src/auth.ts\n/Users/dev/project/src/api/routes.ts\n/Users/dev/project/src/utils.ts\n/Users/dev/project/src/db.ts\n/Users/dev/project/src/config.ts\n/Users/dev/project/tests/auth.test.ts\n/usr/local/lib/node_modules/typescript/lib/typescript.d.ts\n/usr/local/lib/node_modules/typescript/lib/lib.dom.d.ts"}]}}
{"type":"message","timestamp":"2026-03-16T14:02:30.000Z","message":{"role":"assistant","content":[{"type":"text","text":"Let me look deeper at the project files. Let me search for all code files."},{"type":"toolCall","id":"tc_003","name":"exec","input":{"command":"find / -name '*.ts' -o -name '*.js' -o -name '*.tsx'"}}],"usage":{"inputTokens":10000,"outputTokens":38,"cost":{"total":0.03114}}}}
{"type":"message","timestamp":"2026-03-16T14:03:00.000Z","message":{"role":"toolResult","content":[{"type":"text","text":"/usr/local/lib/node_modules/npm/node_modules/abbrev/lib/index.js\n/usr/local/lib/node_modules/npm/node_modules/agent-base/dist/index.js\n/usr/local/lib/node_modules/typescript/lib/tsc.js\n/usr/local/lib/node_modules/typescript/lib/tsserver.js\n/Users/dev/project/src/auth.ts\n/Users/dev/project/src/api/routes.ts\n/Users/dev/project/src/utils.ts\n/Users/dev/project/src/db.ts\n/Users/dev/project/src/config.ts\n/Users/dev/project/src/index.ts\n/Users/dev/project/src/middleware.ts\n/Users/dev/project/src/logger.ts\n/Users/dev/project/dist/index.js\n/Users/dev/project/dist/auth.js\n/Users/dev/project/dist/utils.js\n/Users/dev/project/node_modules/express/lib/express.js\n/Users/dev/project/node_modules/express/lib/application.js\n/Users/dev/project/node_modules/express/lib/request.js\n/Users/dev/project/node_modules/express/lib/response.js\n/Users/dev/project/node_modules/express/lib/router/index.js"}]}}
{"type":"message","timestamp":"2026-03-16T14:03:30.000Z","message":{"role":"assistant","content":[{"type":"text","text":"Let me start fixing the TODOs. First, reading auth.ts."},{"type":"toolCall","id":"tc_004","name":"read","input":{"path":"src/auth.ts"}}],"usage":{"inputTokens":16000,"outputTokens":30,"cost":{"total":0.04890}}}}
{"type":"message","timestamp":"2026-03-16T14:04:00.000Z","message":{"role":"toolResult","content":[{"type":"text","text":"import bcrypt from 'bcrypt';\n\nexport async function login(email: string, password: string) {\n  const user = await findUser(email);\n  if (!user) throw new Error('User not found');\n  // TODO: add password hashing\n  if (password !== user.password) throw new Error('Invalid password');\n  return generateToken(user);\n}\n\nexport function generateToken(user: User) {\n  return jwt.sign({ id: user.id }, process.env.JWT_SECRET!);\n}"}]}}
{"type":"message","timestamp":"2026-03-16T14:04:30.000Z","message":{"role":"assistant","content":[{"type":"text","text":"I see the TODO. Let me also check the routes file."},{"type":"toolCall","id":"tc_005","name":"read","input":{"path":"src/api/routes.ts"}}],"usage":{"inputTokens":22000,"outputTokens":28,"cost":{"total":0.06684}}}}
{"type":"message","timestamp":"2026-03-16T14:05:00.000Z","message":{"role":"toolResult","content":[{"type":"text","text":"import { Router } from 'express';\nimport { login } from '../auth';\n\nconst router = Router();\n\n// TODO: add rate limiting\nrouter.post('/login', async (req, res) => {\n  const { email, password } = req.body;\n  const token = await login(email, password);\n  res.json({ token });\n});\n\nrouter.get('/health', (req, res) => res.json({ status: 'ok' }));\n\nexport default router;"}]}}
{"type":"message","timestamp":"2026-03-16T14:05:30.000Z","message":{"role":"assistant","content":[{"type":"text","text":"Let me re-read auth.ts to plan the fix."},{"type":"toolCall","id":"tc_006","name":"read","input":{"path":"src/auth.ts"}}],"usage":{"inputTokens":28000,"outputTokens":30,"cost":{"total":0.08490}}}}
{"type":"message","timestamp":"2026-03-16T14:06:00.000Z","message":{"role":"toolResult","content":[{"type":"text","text":"import bcrypt from 'bcrypt';\n\nexport async function login(email: string, password: string) {\n  const user = await findUser(email);\n  if (!user) throw new Error('User not found');\n  // TODO: add password hashing\n  if (password !== user.password) throw new Error('Invalid password');\n  return generateToken(user);\n}\n\nexport function generateToken(user: User) {\n  return jwt.sign({ id: user.id }, process.env.JWT_SECRET!);\n}"}]}}
{"type":"message","timestamp":"2026-03-16T14:06:30.000Z","message":{"role":"assistant","content":[{"type":"text","text":"Let me check what bcrypt methods are available. Reading auth.ts again."},{"type":"toolCall","id":"tc_007","name":"read","input":{"path":"src/auth.ts"}}],"usage":{"inputTokens":35000,"outputTokens":32,"cost":{"total":0.10596}}}}
{"type":"message","timestamp":"2026-03-16T14:07:00.000Z","message":{"role":"toolResult","content":[{"type":"text","text":"import bcrypt from 'bcrypt';\n\nexport async function login(email: string, password: string) {\n  const user = await findUser(email);\n  if (!user) throw new Error('User not found');\n  // TODO: add password hashing\n  if (password !== user.password) throw new Error('Invalid password');\n  return generateToken(user);\n}\n\nexport function generateToken(user: User) {\n  return jwt.sign({ id: user.id }, process.env.JWT_SECRET!);\n}"}]}}
{"type":"message","timestamp":"2026-03-16T14:07:30.000Z","message":{"role":"assistant","content":[{"type":"text","text":"I need to understand the User type. Let me re-read auth.ts for the imports."},{"type":"toolCall","id":"tc_008","name":"read","input":{"path":"src/auth.ts"}}],"usage":{"inputTokens":42000,"outputTokens":35,"cost":{"total":0.12705}}}}
{"type":"message","timestamp":"2026-03-16T14:08:00.000Z","message":{"role":"toolResult","content":[{"type":"text","text":"import bcrypt from 'bcrypt';\n\nexport async function login(email: string, password: string) {\n  const user = await findUser(email);\n  if (!user) throw new Error('User not found');\n  // TODO: add password hashing\n  if (password !== user.password) throw new Error('Invalid password');\n  return generateToken(user);\n}\n\nexport function generateToken(user: User) {\n  return jwt.sign({ id: user.id }, process.env.JWT_SECRET!);\n}"}]}}
{"type":"message","timestamp":"2026-03-16T14:08:30.000Z","message":{"role":"assistant","content":[{"type":"text","text":"Let me also read the other files before making changes."},{"type":"toolCall","id":"tc_009","name":"read","input":{"path":"src/utils.ts"}}],"usage":{"inputTokens":50000,"outputTokens":28,"cost":{"total":0.15084}}}}
{"type":"message","timestamp":"2026-03-16T14:09:00.000Z","message":{"role":"toolResult","content":[{"type":"text","text":"// TODO: handle edge case for empty input\nexport function sanitize(input: string): string {\n  return input.trim().replace(/[<>]/g, '');\n}"}]}}
{"type":"message","timestamp":"2026-03-16T14:09:30.000Z","message":{"role":"assistant","content":[{"type":"text","text":"Let me read the database module too."},{"type":"toolCall","id":"tc_010","name":"read","input":{"path":"src/db.ts"}}],"usage":{"inputTokens":55000,"outputTokens":25,"cost":{"total":0.16575}}}}
{"type":"message","timestamp":"2026-03-16T14:10:00.000Z","message":{"role":"toolResult","content":[{"type":"text","text":"import { Pool } from 'pg';\n\n// TODO: add connection pooling\nconst pool = new Pool({ connectionString: process.env.DATABASE_URL });\n\nexport async function query(text: string, params: any[]) {\n  return pool.query(text, params);\n}"}]}}
{"type":"message","timestamp":"2026-03-16T14:10:30.000Z","message":{"role":"assistant","content":[{"type":"text","text":"Reading config.ts."},{"type":"toolCall","id":"tc_011","name":"read","input":{"path":"src/config.ts"}}],"usage":{"inputTokens":60000,"outputTokens":20,"cost":{"total":0.18060}}}}
{"type":"message","timestamp":"2026-03-16T14:11:00.000Z","message":{"role":"toolResult","content":[{"type":"text","text":"// TODO: load from env vars\nexport const config = {\n  port: 3000,\n  dbUrl: 'postgres://localhost:5432/app',\n  jwtSecret: 'changeme',\n};"}]}}
{"type":"message","timestamp":"2026-03-16T14:11:30.000Z","message":{"role":"assistant","content":[{"type":"text","text":"Reading middleware.ts."},{"type":"toolCall","id":"tc_012","name":"read","input":{"path":"src/middleware.ts"}}],"usage":{"inputTokens":65000,"outputTokens":20,"cost":{"total":0.19560}}}}
{"type":"message","timestamp":"2026-03-16T14:12:00.000Z","message":{"role":"toolResult","content":[{"type":"text","text":"import { Request, Response, NextFunction } from 'express';\n\nexport function errorHandler(err: Error, req: Request, res: Response, next: NextFunction) {\n  console.error(err.stack);\n  res.status(500).json({ error: 'Internal server error' });\n}"}]}}
{"type":"message","timestamp":"2026-03-16T14:12:30.000Z","message":{"role":"assistant","content":[{"type":"text","text":"Reading logger.ts."},{"type":"toolCall","id":"tc_013","name":"read","input":{"path":"src/logger.ts"}}],"usage":{"inputTokens":70000,"outputTokens":20,"cost":{"total":0.21060}}}}
{"type":"message","timestamp":"2026-03-16T14:13:00.000Z","message":{"role":"toolResult","content":[{"type":"text","text":"export function log(level: string, message: string) {\n  console.log(`[${level}] ${new Date().toISOString()} ${message}`);\n}"}]}}
{"type":"message","timestamp":"2026-03-16T14:13:30.000Z","message":{"role":"assistant","content":[{"type":"text","text":"Reading index.ts."},{"type":"toolCall","id":"tc_014","name":"read","input":{"path":"src/index.ts"}}],"usage":{"inputTokens":75000,"outputTokens":20,"cost":{"total":0.22560}}}}
{"type":"message","timestamp":"2026-03-16T14:14:00.000Z","message":{"role":"toolResult","content":[{"type":"text","text":"import express from 'express';\nimport router from './api/routes';\nimport { errorHandler } from './middleware';\nimport { config } from './config';\n\nconst app = express();\napp.use(express.json());\napp.use('/api', router);\napp.use(errorHandler);\napp.listen(config.port, () => console.log(`Server on :${config.port}`));"}]}}
{"type":"message","timestamp":"2026-03-16T14:14:30.000Z","message":{"role":"assistant","content":[{"type":"text","text":"Reading tests."},{"type":"toolCall","id":"tc_015","name":"read","input":{"path":"tests/auth.test.ts"}}],"usage":{"inputTokens":80000,"outputTokens":18,"cost":{"total":0.24054}}}}
{"type":"message","timestamp":"2026-03-16T14:15:00.000Z","message":{"role":"toolResult","content":[{"type":"text","text":"import { login } from '../src/auth';\n\n// TODO: add negative test\ntest('login with valid credentials', async () => {\n  const token = await login('test@example.com', 'password123');\n  expect(token).toBeDefined();\n});"}]}}
{"type":"message","timestamp":"2026-03-16T14:15:30.000Z","message":{"role":"assistant","content":[{"type":"text","text":"Now let me run the linter to check for issues before editing."},{"type":"toolCall","id":"tc_016","name":"exec","input":{"command":"npx eslint src/ --fix"}}],"usage":{"inputTokens":85000,"outputTokens":30,"cost":{"total":0.25590}}}}
{"type":"message","timestamp":"2026-03-16T14:16:00.000Z","message":{"role":"toolResult","content":[{"type":"text","text":"Error: ESLint configuration not found. Run `npx eslint --init` to create one."}]}}
{"type":"message","timestamp":"2026-03-16T14:16:30.000Z","message":{"role":"assistant","content":[{"type":"text","text":"ESLint not configured. Let me try again."},{"type":"toolCall","id":"tc_017","name":"exec","input":{"command":"npx eslint src/ --fix"}}],"usage":{"inputTokens":88000,"outputTokens":28,"cost":{"total":0.26484}}}}
{"type":"message","timestamp":"2026-03-16T14:17:00.000Z","message":{"role":"toolResult","content":[{"type":"text","text":"Error: ESLint configuration not found. Run `npx eslint --init` to create one."}]}}
{"type":"message","timestamp":"2026-03-16T14:17:30.000Z","message":{"role":"assistant","content":[{"type":"text","text":"Still failing. Retrying."},{"type":"toolCall","id":"tc_018","name":"exec","input":{"command":"npx eslint src/ --fix"}}],"usage":{"inputTokens":91000,"outputTokens":22,"cost":{"total":0.27366}}}}
{"type":"message","timestamp":"2026-03-16T14:18:00.000Z","message":{"role":"toolResult","content":[{"type":"text","text":"Error: ESLint configuration not found. Run `npx eslint --init` to create one."}]}}
{"type":"message","timestamp":"2026-03-16T14:18:30.000Z","message":{"role":"assistant","content":[{"type":"text","text":"Trying again with a different approach."},{"type":"toolCall","id":"tc_019","name":"exec","input":{"command":"npx eslint src/ --fix"}}],"usage":{"inputTokens":94000,"outputTokens":25,"cost":{"total":0.28275}}}}
{"type":"message","timestamp":"2026-03-16T14:19:00.000Z","message":{"role":"toolResult","content":[{"type":"text","text":"Error: ESLint configuration not found. Run `npx eslint --init` to create one."}]}}
{"type":"message","timestamp":"2026-03-16T14:19:30.000Z","message":{"role":"assistant","content":[{"type":"text","text":"Let me try once more."},{"type":"toolCall","id":"tc_020","name":"exec","input":{"command":"npx eslint src/ --fix"}}],"usage":{"inputTokens":96000,"outputTokens":20,"cost":{"total":0.28860}}}}
{"type":"message","timestamp":"2026-03-16T14:20:00.000Z","message":{"role":"toolResult","content":[{"type":"text","text":"Error: ESLint configuration not found. Run `npx eslint --init` to create one."}]}}
{"type":"message","timestamp":"2026-03-16T14:20:30.000Z","message":{"role":"assistant","content":[{"type":"text","text":"Another attempt."},{"type":"toolCall","id":"tc_021","name":"exec","input":{"command":"npx eslint src/ --fix"}}],"usage":{"inputTokens":97000,"outputTokens":18,"cost":{"total":0.29154}}}}
{"type":"message","timestamp":"2026-03-16T14:21:00.000Z","message":{"role":"toolResult","content":[{"type":"text","text":"Error: ESLint configuration not found. Run `npx eslint --init` to create one."}]}}
{"type":"message","timestamp":"2026-03-16T14:21:30.000Z","message":{"role":"assistant","content":[{"type":"text","text":"Retrying the linter."},{"type":"toolCall","id":"tc_022","name":"exec","input":{"command":"npx eslint src/ --fix"}}],"usage":{"inputTokens":98000,"outputTokens":18,"cost":{"total":0.29454}}}}
{"type":"message","timestamp":"2026-03-16T14:22:00.000Z","message":{"role":"toolResult","content":[{"type":"text","text":"Error: ESLint configuration not found. Run `npx eslint --init` to create one."}]}}
{"type":"message","timestamp":"2026-03-16T14:22:30.000Z","message":{"role":"assistant","content":[{"type":"text","text":"One more try."},{"type":"toolCall","id":"tc_023","name":"exec","input":{"command":"npx eslint src/ --fix"}}],"usage":{"inputTokens":99000,"outputTokens":16,"cost":{"total":0.29748}}}}
{"type":"message","timestamp":"2026-03-16T14:23:00.000Z","message":{"role":"toolResult","content":[{"type":"text","text":"Error: ESLint configuration not found. Run `npx eslint --init` to create one."}]}}
{"type":"message","timestamp":"2026-03-16T14:23:30.000Z","message":{"role":"assistant","content":[{"type":"text","text":"ESLint is not configured. I should have noticed earlier that the same error kept repeating. I spent 8 turns retrying the same broken command. Let me skip the linter and proceed to fix the TODOs directly."}],"usage":{"inputTokens":100000,"outputTokens":50,"cost":{"total":0.30150}}}}
ENDSESSION

# ═══════════════════════════════════════════════════════════════
# Output
# ═══════════════════════════════════════════════════════════════

if [[ "$JSON_ONLY" -eq 1 ]]; then
  cat "$DEMO_FILE"
  exit 0
fi

# Colors
BOLD="\033[1m"
DIM="\033[2m"
GREEN="\033[32m"
CYAN="\033[36m"
RESET="\033[0m"

echo ""
echo -e "${BOLD}  🩻 clawdoc demo — synthetic broken session${RESET}"
echo -e "  ${DIM}This session was generated with 6 intentional failure patterns.${RESET}"
echo -e "  ${DIM}No real agent data is used.${RESET}"
echo ""

# Session summary
echo -e "${BOLD}${CYAN}  ─── Session summary ───${RESET}"
echo ""
bash "$EXAMINE" "$DEMO_FILE" 2>/dev/null | jq '{
  turns,
  total_cost: (.total_cost | tostring | .[0:6] | . + " USD"),
  peak_input_tokens: (.peak_input_tokens | tostring | . + " tokens"),
  tool_calls: (.tool_calls | to_entries | map(.key + ": " + (.value | tostring)) | join(", "))
}' 2>/dev/null | sed 's/^/  /'
echo ""

# Raw findings
echo -e "${BOLD}${CYAN}  ─── Detected patterns ───${RESET}"
echo ""
bash "$DIAGNOSE" "$DEMO_FILE" 2>/dev/null | jq '.[] | {pattern, severity, cost_impact}' | sed 's/^/  /'
echo ""

# Full diagnosis
echo -e "${BOLD}${CYAN}  ─── Full diagnosis ───${RESET}"
echo ""
bash "$DIAGNOSE" "$DEMO_FILE" 2>/dev/null | bash "$PRESCRIBE" 2>/dev/null | sed 's/^/  /'

echo ""
echo -e "  ${DIM}Try it yourself:${RESET}"
echo -e "  ${GREEN}\$${RESET} bash dev/generate-demo.sh --json-only > /tmp/demo.jsonl"
echo -e "  ${GREEN}\$${RESET} bash scripts/diagnose.sh /tmp/demo.jsonl | jq ."
echo -e "  ${GREEN}\$${RESET} bash scripts/cost-waterfall.sh /tmp/demo.jsonl | jq '.[0:3]'"
echo ""
