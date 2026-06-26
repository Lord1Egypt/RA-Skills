# Setup - Dual-Brain Memory Guardian Agent

## First-Time Setup

### 1. Create Local Memory Structure

PowerShell (Windows):

```powershell
New-Item -ItemType Directory -Force -Path "$HOME/dual-brain-memory-guardian/projects","$HOME/dual-brain-memory-guardian/domains","$HOME/dual-brain-memory-guardian/archive" | Out-Null
```

POSIX shell (macOS/Linux):

```bash
mkdir -p ~/dual-brain-memory-guardian/{projects,domains,archive}
```

### 2. Initialize Core Markdown Files

Create:

- `~/dual-brain-memory-guardian/memory.md` from `memory-template.md`
- `~/dual-brain-memory-guardian/corrections.md`
- `~/dual-brain-memory-guardian/reflections.md` from `reflections.md`
- `~/dual-brain-memory-guardian/index.md`
- `~/dual-brain-memory-guardian/heartbeat-state.md`

### 3. Enable npm Runtime

In this project root:

```bash
npm install
```

This installs all runtime dependencies from `package.json`, including `@pinecone-database/pinecone` and `dotenv`.

If you see `Cannot find package 'dotenv'` or `Cannot find package '@pinecone-database/pinecone'`, run `npm install` in this directory and retry.

### 4. Configure Environment

Create `.env` manually in the project root and set at least:

For npm commands in this repo, `.env` is auto-loaded by the CLI.

Example:

```dotenv
PINECONE_API_KEY=your_api_key_here
PINECONE_INDEX_NAME=dual-brain-memory-guardian-memory
PINECONE_CLOUD=aws
PINECONE_REGION=us-east-1
PINECONE_MODEL=multilingual-e5-large
PINECONE_FIELD_MAP_TEXT=content
PINECONE_NAMESPACE_PREFIX=dualbrain
MEMORY_TENANT=default
```

- `PINECONE_API_KEY`
- `PINECONE_INDEX_NAME` (default: `dual-brain-memory-guardian-memory`)
- `PINECONE_CLOUD` (default: `aws`)
- `PINECONE_REGION` (default: `us-east-1`)
- `PINECONE_MODEL` (must stay `multilingual-e5-large` unless intentionally changed)
- `PINECONE_FIELD_MAP_TEXT` (default: `content`)
- `PINECONE_NAMESPACE_PREFIX` (default: `dualbrain`)
- `MEMORY_TENANT` (default: `default`)

Optional:

- `PINECONE_IMPORT_INTEGRATION_ID` for private object storage import
- `DUAL_BRAIN_MEMORY_HOME` to override local markdown memory root

### 4.1 Configure OpenClaw Skill Entry (Recommended)

If you run through OpenClaw, keep the skill key aligned with SKILL frontmatter and inject env via `skills.entries`:

```json5
{
	skills: {
		entries: {
			"dual-brain-memory-guardian": {
				enabled: true,
				apiKey: { source: "env", provider: "default", id: "PINECONE_API_KEY" },
				env: {
					PINECONE_API_KEY: "<set-in-your-secret-store>",
					PINECONE_INDEX_NAME: "dual-brain-memory-guardian-memory",
					PINECONE_CLOUD: "aws",
					PINECONE_REGION: "us-east-1",
					PINECONE_MODEL: "multilingual-e5-large",
					PINECONE_FIELD_MAP_TEXT: "content",
					PINECONE_NAMESPACE_PREFIX: "dualbrain",
					MEMORY_TENANT: "default"
				}
			}
		}
	}
}
```

Sandbox note:

- `skills.entries.*.env` and `apiKey` apply to host runs.
- For sandboxed runs, set environment variables in the sandbox docker env map (default or per-agent).

### 4.2 Security Review + Isolated Run (Required for Third-Party Use)

Before first use with real secrets:

1. Review `SKILL.md`, `operations.md`, `boundaries.md`, and `scripts/memory-cli.js`.
2. Run verification in a disposable environment: `npm run verify`.
3. Test with a limited-scope Pinecone key and non-production namespace/tenant.
4. Keep production secrets out of prompts and logs.

### 5. Initialize Pinecone Index

```bash
npm run memory:init
```

This command bootstraps or validates an integrated embedding index with:

- model: `multilingual-e5-large`
- field map: `text -> content`

### 6. Add SOUL.md Steering (Dual-Brain)

Add this section to `SOUL.md`:

```markdown
**Dual-Brain Memory Guardian**
Runtime flow source of truth: follow `operations.md`.

Before non-trivial tasks, run:
- `npm run memory:auto-session-start -- --task "..." --top-k 3`

After corrections, run:
- `npm run memory:on-correction -- --content "..."`

When execution or reasoning errors happen, run immediately:
- `npm run memory:on-correction -- --type pitfall --content "what failed" --resolution "root cause and fix"`

After non-trivial task completion, run:
- `npm run memory:auto-task-complete -- --summary "..." --outcome success|partial|failed`

Fallback manual hooks when auto wrappers are unavailable:
- `npm run memory:session-start -- --task "..." --top-k 3`
- `npm run memory:on-task-complete -- --summary "..." --outcome success|partial|failed`
```

### 7. Refine AGENTS.md Memory Behavior (Non-Destructive)

Update the `## Memory` section by adding:

- Dual-brain continuity source (`~/dual-brain-memory-guardian/`)
- Pre-task recall ritual with enforced command (`memory:auto-session-start`)
- Conflict policy (Markdown > Pinecone)
- Correction routing (`memory:on-correction`) and post-task routing (`memory:auto-task-complete`)
- Error capture routing: store failed experience and root cause via `memory:on-correction --type pitfall`
- Deletion safety: before `memory:forget`/`memory:forget-all`, warn user about irreversible deletion and confirm intent
- Runtime sequencing authority: `operations.md`

### 8. Add HEARTBEAT.md Steering

Ensure `HEARTBEAT.md` includes:

```markdown
## Dual-Brain Memory Guardian Check

- Read `./heartbeat-rules.md`
- Read `./operations.md` for trigger contract and command names
- Use `~/dual-brain-memory-guardian/heartbeat-state.md` for run markers
- Review heartbeat-related memory files:
	- `~/dual-brain-memory-guardian/memory.md`
	- `~/dual-brain-memory-guardian/corrections.md`
	- `~/dual-brain-memory-guardian/reflections.md`
	- `~/dual-brain-memory-guardian/index.md`
- If no local changes and no promotable DEEP digest signal, return `HEARTBEAT_OK`
```

If you use OpenClaw Gateway heartbeat, keep heartbeat enabled and use a prompt that tells the agent to read `HEARTBEAT.md` and follow it strictly. This ensures the files above are actually included in each heartbeat run.

### 9. Optional Proactivity Companion

If user agrees:

1. `clawhub install proactivity`
2. Read installed proactivity skill
3. Continue its setup flow immediately

If user declines, continue with dual-brain-memory-guardian only.

## Verification

Run these checks:

```bash
npm run verify
npm run memory:init
npm run memory:freshness
```

Optional end-to-end smoke test:

```bash
npm run memory:auto-session-start -- --task "api refactor" --project sample --domain code
npm run memory:save -- --type correction --content "sample correction" --domain code
npm run memory:search -- --query "sample correction" --top-k 3
npm run memory:on-correction -- --content "always use explicit return types" --domain code
npm run memory:mark-promoted -- --id <event-id> --promoted true
npm run memory:auto-task-complete -- --summary "refactored auth retries" --outcome success
```

For LLM/CLI reliability, prefer file-backed flags when text contains nested quotes or braces:

```bash
npm run memory:on-correction -- --content-file ./temp-correction.txt --domain code
```

Expected outcome:

- Index reachable
- Save command returns id/namespace
- Search command returns at least one related hit
