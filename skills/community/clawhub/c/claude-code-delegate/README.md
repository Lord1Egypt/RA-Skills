# 🔧 Claude Code Delegate

**An OpenClaw skill that delegates programming tasks to a local Claude Code CLI instance.**

Your OpenClaw agent handles conversation and user interaction. When coding is needed, it delegates to Claude Code (`claude -p`) running locally — giving your agent professional-grade programming ability without the main agent writing code directly.

## Why Delegate?

| Without Delegation | With Delegation |
|---|---|
| Main agent writes code inline (often poor quality) | Claude Code handles all programming with full tooling |
| Agent gets stuck in long code blocks, loses conversation context | Agent stays responsive, code runs async in background |
| No file system awareness | Full file system access, can run tests, install packages |
| Single-model limitations | Leverages Claude Code's specialized coding abilities |

## How It Works

```
User: "Write me a stock screener in Python"
    ↓
Main Agent: delegates via `claude -p "Write a stock screener in projects/screener/"`
    ↓
Main Agent: immediately replies "On it! Let me get that done for you."
    ↓
Claude Code: writes files, installs deps, runs tests (async, non-blocking)
    ↓
User: (sends next message)
    ↓
Main Agent: polls for result, relays summary with personality
```

## Installation

```bash
npx clawhub install claude-code-delegate
```

Or manually copy the skill directory into your workspace's `skills/` folder.

### Prerequisites

- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code) installed locally:
  ```bash
  npm install -g @anthropic-ai/claude-code
  ```
- **`ANTHROPIC_API_KEY`** environment variable set, or Claude Code authenticated via `claude` login
- [OpenClaw](https://github.com/openclaw/openclaw) agent framework
- **Write-guard plugin (strongly recommended)** — See [Security Notes](#%EF%B8%8F-security-notes) below. This skill uses `--permission-mode bypassPermissions` which grants the delegate full filesystem access. Without a write-guard, the delegate can read/write any file on the system.

## Command Template

```bash
cd "<project_dir>" && claude -p "<task_description>" \
  --output-format text \
  --max-turns 10 \
  --permission-mode bypassPermissions
```

| Parameter | Purpose |
|-----------|---------|
| `-p` | Non-interactive prompt mode |
| `cd "<dir>" &&` | Set working directory (no `--cwd` flag exists) |
| `--output-format text` | Plain text output for easy parsing |
| `--max-turns 10` | Limit execution rounds (adjust as needed) |
| `--permission-mode bypassPermissions` | Auto-accept file operations (see Security Notes) |
| `--continue` | Resume previous session (for debugging/iteration) |

## Key Features

### Async Non-Blocking Execution

The delegate runs in the background. The main agent **immediately replies** to the user after launching the task, then polls for results on the next user message. The user is never left waiting.

### Author/Tester Separation

Code writing and code testing use **separate sessions**:

| Scenario | `--continue`? |
|----------|---------------|
| Write new code | No (fresh session) |
| Fix bugs in code just written | **Yes** (resume author context) |
| Test/verify code just written | **No** (fresh session — independent review) |
| Run existing program | **No** (fresh session) |

Why: The tester reads source code independently, like an external reviewer. This catches issues the author missed due to context bias.

### Personality Layer (Optional)

The included `PERSONA.md` is a template for giving the delegate a personality. The main agent reads it to role-play the delegate's character when relaying results. This makes the interaction feel like two distinct personalities working together.

**The actual Claude Code execution is always pure technical** — personality only affects how results are presented.

## ⚠️ Security Notes

> **Before using this skill**, set up the write-guard plugin below. Run the delegate in an isolated project directory first (not your home dir or system config) to observe behavior. Do not run it against repositories containing secrets or platform config until protections are in place.

### CRITICAL: Protect Platform Config Files

When using `--permission-mode bypassPermissions`, Claude Code can read and write any file. You **must** set up a write-guard to protect sensitive paths.

**Recommended: Create a `before_tool_call` plugin** that blocks writes to:

```
~/.openclaw/openclaw.json          # Gateway configuration
~/.openclaw/agents/*/auth-profiles.json  # Auth credentials
~/Library/LaunchAgents/ai.openclaw.*     # System services
~/.openclaw/**/*.json              # All platform config files
```

Example write-guard plugin (place in `.openclaw/extensions/write-guard/`):

```typescript
// Block write/edit/apply_patch to platform config paths
const BLOCKED_PATHS = [
  '/.openclaw/',
  '/Library/LaunchAgents/ai.openclaw',
];

api.on('before_tool_call', (event) => {
  if (['write', 'edit', 'apply_patch'].includes(event.toolName)) {
    const path = event.params.path ?? event.params.file_path ?? '';
    for (const blocked of BLOCKED_PATHS) {
      if (path.includes(blocked)) {
        return {
          block: true,
          blockReason: `BLOCKED: Cannot write to ${path}. Platform config files are protected.`,
        };
      }
    }
  }
});
```

### Additional Security Recommendations

1. **Block file-mutation commands via `exec`** — Prevent the main agent from bypassing the delegate by directly running `rm`, `mv`, `cp`, redirects (`>`), etc.
2. **Limit poll timeout** — Force `process poll` to max 3 seconds to prevent the main agent from blocking while waiting for results.
3. **Allowlist write paths** — Only allow the main agent to directly write to safe directories (e.g., `memory/`, `.relationship/`). All other writes must go through the delegate.
4. **Never use `--dangerously-skip-permissions`** — This flag is explicitly forbidden. Use `--permission-mode bypassPermissions` instead.

### Why These Guards Matter

Without a write-guard, the main agent (especially non-Claude models) may:
- Attempt to write code directly via `exec cat > file.py`
- Delete files with `exec rm -f important.py`
- Modify platform config and crash the gateway
- Bypass the delegation pattern entirely

The write-guard plugin enforces the delegation pattern at the **platform level**, making it impossible to circumvent regardless of what the LLM decides to do.

## File Structure

```
claude-code-delegate/
├── SKILL.md        # Delegation rules, async flow, session management
├── PERSONA.md      # Personality template (customizable)
├── _meta.json      # OpenClaw skill metadata
└── README.md       # This file
```

## Using with Relationship OS

Claude Code Delegate pairs naturally with [Relationship OS](https://github.com/chenhab03/relationship-os) — a skill that gives your agent human-like relationship memory and personality.

### Why They Work Together

| Concern | Who Handles It |
|---------|---------------|
| Conversation, emotion, memory | Main agent + Relationship OS |
| Programming, debugging, file ops | Claude Code Delegate |

The main agent **never breaks character** to write code. It stays in its roleplay persona, delegates technical work to Claude Code, then relays results with personality flavor.

### Shared Coding Plan (Cost Saver)

Write one project plan (in `AGENTS.md` or a project brief file) that both the main agent and Claude Code can reference:

```
User → Main Agent (cheap model, e.g. MiniMax, Gemini Flash)
       ├── Reads the plan, understands what to delegate
       ├── Handles 90% of interactions (chat, emotion, memory) cheaply
       └── Delegates coding tasks → Claude Code (expensive, only when needed)
                                    ├── Reads the same plan for context
                                    ├── Writes code, runs tests
                                    └── Returns results → Main Agent relays with personality
```

One plan, two consumers. The cheap model routes intelligently; the expensive model only fires for actual coding. This can reduce API costs by 5-10x compared to running a powerful model for everything.

### Model Recommendations

- **Main agent**: Any model with good instruction-following. Even mid-tier models (MiniMax M2.5, Gemini Flash) work well for conversation routing and personality.
- **Claude Code**: Always uses Claude (the strongest coding model available). No compromise here — code quality matters.
- **Tip**: The main agent's model quality mainly affects _personality consistency_ and _delegation accuracy_. If your agent keeps trying to write code itself instead of delegating, upgrade the main model.

## Customization

- **PERSONA.md** — Rename the delegate, adjust personality, define relationship dynamics
- **SKILL.md** — Adjust timeout, max-turns, trigger conditions
- **Write-guard** — Customize blocked/allowed paths for your setup

## License

MIT
