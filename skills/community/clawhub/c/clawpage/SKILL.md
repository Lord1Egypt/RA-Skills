---
name: clawpage
description: "Share AI agent conversations as public web pages. Use when the user wants to share a conversation externally, export conversation history for documentation, or publish a chat session to a public URL."
license: Apache-2.0
metadata: {"openclaw":{"emoji":"💬","homepage":"https://github.com/imyelo/clawpage"}}
---

# clawpage

Share AI agent conversations as public web pages.

## Supported Agents

| Agent | Profile |
|-------|---------|
| OpenClaw | [references/platforms/openclaw.md](references/platforms/openclaw.md) |
| _(unknown)_ | [references/platforms/unknown.md](references/platforms/unknown.md) — generic skill-based fallback |
| _(new platform)_ | Add a file following [references/platforms/TEMPLATE.md](references/platforms/TEMPLATE.md) |

## Core Workflow

### 1. Setup Check

- Detect agent type; load project dir + site URL using the agent profile
- If project not configured locally, ask the user:
  - **"Do you have an existing clawpage repo?"**
  - Yes → [Existing Repo, New Environment](references/setup.md#existing-repo-new-environment)
  - No (Default) → [First-Time Setup](references/setup.md#first-time-setup)

### 2. Locate Session

- List sessions using agent profile discovery
- Show candidates → user confirms selection

### 3. Extract & Convert

Follow the **Conversion** section in the platform profile detected in Step 1.
Save the result to `{projectDir}/chats/.tmp/{timestamp}.yaml`.

### 4. Populate Metadata

The CLI auto-fills structural fields. The Skill's job is to fill in the human-facing metadata:

| Field | CLI default | Action |
|-------|-------------|--------|
| `date`, `sessionId`, `model`, `totalMessages`, `totalTokens`, `defaultShowProcess` | Auto-filled | Review only |
| `visibility` | `private` | Update to `public` |
| `participants` | Generic role names (`user`, `assistant`) | Ask user for display names → rename keys; if no name is provided, use `Human` / `Agent` for single-speaker or `Human 1` / `Human 2` … for multi-speaker |
| `title` | `'Session Export'` (generic) | Skim generated YAML → suggest → confirm |
| `description` | _(absent)_ | Write one-sentence summary → confirm |
| `channel` | _(absent)_ | Ask user — set to platform name (e.g. `discord`) if applicable; omit otherwise |
| `cover` | _(absent)_ | Skip (user adds custom OG image URL manually later) |
| `tags` | _(absent)_ | Skip (user adds manually later) |

### 5. Redact

Review the generated YAML and replace sensitive information with `[REDACTED]`:
- API keys, tokens, passwords → `[REDACTED]`
- File paths with usernames (`/Users/xxx` → `~`)
- Email addresses, phone numbers → `[REDACTED]`
- Internal URLs and private IPs → `[REDACTED]`

Do **not** silently remove content — always substitute `[REDACTED]` so the reader can see that content was present but withheld.

### 6. Confirm & Save

- Suggest filename: `{YYYYMMDD}-{topic}.yaml`
- Show preview → user confirms or modifies topic/filename
- **Before moving the file, create a dedicated branch** (see below — required even if the user does not publish yet):
  ```bash
  cd {projectDir}
  git checkout main
  git pull origin main
  git checkout -b chat/{YYYYMMDD}-{topic}
  ```
- Move: `{projectDir}/chats/.tmp/{timestamp}.yaml` → `{projectDir}/chats/{YYYYMMDD}-{topic}.yaml`
- Stage and commit immediately so the file is isolated on its own branch:
  ```bash
  git add chats/{YYYYMMDD}-{topic}.yaml
  git commit -m "docs: add {topic}"
  ```

> **Why create a branch here?** Saving on the default branch risks mixing unrelated changes into a future PR. Always commit each chat file on its own dedicated branch.

---

## Optional: Publish

Push the branch created in step 6 and open a PR.
See [references/publish.md](references/publish.md). Only proceed after explicit user request.

---

## Edge Cases

- **First-time project setup** → [references/setup.md](references/setup.md)
- **Large or complex sessions (unknown platforms)** → [references/large-file.md](references/large-file.md)
