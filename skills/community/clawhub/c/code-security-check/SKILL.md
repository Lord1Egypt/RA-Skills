---
name: code-security-check
description: |
  Audit the current project for sensitive information leaks before pushing to public repositories.
  This skill should be used when the user asks to check for security issues, scan for secrets,
  review .gitignore coverage, audit a project before open-sourcing, or when they mention
  keywords like "安全检查", "敏感信息", "泄露", "gitignore", "密钥", "API key leak",
  "before pushing to GitHub", "开源检查". It scans the working tree for exposed credentials,
  API keys, tokens, private keys, and misconfigured .gitignore files.
agent_created: true
---

# Code Security Check - AI-Driven Code Repository Security Audit

## Purpose

Scan the current project for sensitive information leaks that could be exposed when pushing to a
public repository. This skill uses AI directly to read and analyze files — no scripts, no regex
database to maintain. The AI understands context, recognizes novel key formats, and avoids the
brittleness of pattern matching.

## When to Use

Trigger this skill when the user says things like:

- "安全检查" / "帮我检查敏感信息" / "开源前检查" / "我的代码能公开吗"
- "check for secrets" / "scan for API keys" / "audit before pushing"
- "检查 .gitignore" / "我的项目有泄露风险吗"
- Any concern about pushing code to GitHub or open-sourcing

## Workflow

The audit proceeds in six phases. Complete each phase before moving to the next.

**CRITICAL — Phase 0 MUST run first.** It determines whether a full audit is even necessary.
Do not skip it. Do not lead with "let me scan your code" — first check if there's any real risk.

### Phase 0: Exposure Risk Assessment (Gate Check)

Goal: Determine whether the project has any public exposure risk. If not, exit early
with a friendly reminder — do NOT bother the user with a full detailed scan.
Only non-public / local projects have no leak risk.

**Step 1 — Check if this is a git repo:**

Run `git status` in the project root. If the command fails (not a git repo):

> 🟢 **这是一个本地项目，未使用 Git 管理。本地文件不存在公开泄露风险，无需担心。**

→ **EXIT. Do not proceed to further phases.** Do not ask to fix anything.

**Step 2 — Check for remote (for git repos only):**

Run `git remote -v`. If no remote is configured:

> 🟢 **这是一个本地 Git 仓库，尚未关联远程仓库（没有 remote），代码不会被推送到任何公开位置，不存在泄露风险。**
> 💡 友情提醒：如果未来要推送到公开仓库，建议提前配置 `.gitignore` 防止构建产物和依赖被提交。

→ **EXIT. Do not proceed to further phases.** Do not ask to fix anything — a quick reminder is enough.

**Step 3 — Check remote visibility (for repos with a remote):**

If the remote appears to be on GitHub, try to check its visibility:

```bash
gh repo view --json visibility 2>/dev/null || echo "CANNOT_DETERMINE"
```

- If `visibility` is `PRIVATE`:

> 🟢 **远程仓库是私有仓库（private），非公开项目不存在泄露风险。**
> 💡 友情提醒：确保 `.gitignore` 配置正确，以防将来改为公开仓库时出现意外。

→ **EXIT. Do not proceed to further phases.** A friendly reminder is sufficient.

- If `visibility` is `PUBLIC` → proceed to full audit (Phase 1–5).
- If `CANNOT_DETERMINE` (not GitHub, or gh CLI not available) → proceed to full audit with a caveat:
  > ⚠️ 无法确定远程仓库的可见性，按公开仓库标准进行完整检查。

### Phase 1: Project Discovery

Goal: Understand what kind of project this is and what files exist.

1. Determine the project root (current workspace, or path specified by user).
2. Detect the technology stack by looking for indicator files:
   - `package.json` → Node.js / TypeScript
   - `requirements.txt`, `pyproject.toml`, `Pipfile` → Python
   - `go.mod` → Go
   - `pom.xml`, `build.gradle`, `build.gradle.kts` → Java / Kotlin
   - `Gemfile` → Ruby
   - `Cargo.toml` → Rust
   - `composer.json` → PHP
   - `Dockerfile`, `docker-compose.yml` → Docker
   - `*.tf` → Terraform
   - `.firebaserc` → Firebase
3. Use `git ls-files --others --exclude-standard` to list untracked files. These are
   high-risk because they slip past `.gitignore` and could be accidentally committed.

### Phase 2: .gitignore Audit

Goal: Check if .gitignore exists and whether it covers the basics.

1. Read `.gitignore` if it exists. If not, this is a critical finding — note it.
2. For the detected tech stack, check whether essential patterns are covered.
   Key patterns by stack:

   | Stack | Must-have in .gitignore |
   |-------|------------------------|
   | Node.js | `.env`, `.env.*`, `node_modules/` |
   | Python | `.env`, `.env.*`, `__pycache__/`, `venv/`, `*.pyc` |
   | Go | `.env`, `.env.*`, `*.exe`, `*.test` |
   | Java | `.env`, `.env.*`, `*.class`, `target/` |
   | Ruby | `.env`, `.env.*`, `*.gem`, `vendor/bundle/` |
   | Rust | `.env`, `.env.*`, `target/` |
   | Docker | `.env`, `.env.*` |
   | Terraform | `*.tfstate`, `*.tfstate.*`, `.terraform/`, `terraform.tfvars` |
   | Firebase | `google-services.json`, `GoogleService-Info.plist`, `.env` |
   | Any | `*.pem`, `*.key`, `*.p12`, `*.pfx`, `credentials.json`, `*.log` |

3. Note any missing patterns as findings.

### Phase 3: Identify and Analyze Suspicious Files

Goal: Find files that might contain secrets, then use AI to analyze them.

**Step 1 — Structural scan (fast, no content reading yet):**

Use Glob to find files that commonly hold secrets:

```
**/.env
**/.env.*
**/.npmrc
**/credentials.json
**/credentials.*.json
**/service-account.json
**/service-account-*.json
**/google-services.json
**/GoogleService-Info.plist
**/secrets.yaml
**/secrets.yml
**/secret*
**/terraform.tfvars
**/*.tfstate
**/*.tfstate.backup
**/config/database.yml
**/config/secrets.yml
**/config/master.key
**/.aws/credentials
**/aws-credentials.json
```

Also look for private key files: `id_rsa`, `id_ed25519`, `id_ecdsa`, `*.pem`, `*.key`, `*.p12`, `*.pfx`.

**Step 2 — Quick content pre-filter (optional, use Grep):**

For efficiency on larger projects, run a few broad Grep queries to narrow down which text
files are worth reading:

```
# Files that look like they contain API keys or tokens
(sk-|ghp_|github_pat_|AKIA|AIza|xox[baprs]-|sk_live_|eyJ|-----BEGIN)
```

**Step 3 — AI Analysis of suspicious files:**

Read each identified file. For each file, analyze its content and determine:

- Does it contain real credentials, keys, or tokens?
- Are these live/production keys or test/placeholder values?
- Is the file already in `.gitignore`?
- Is it already tracked by git? (use `git ls-files` to check)

Be thorough but smart — skip obvious false positives like:
- Files that only contain placeholder/example values (`YOUR_API_KEY`, `changeme`, `xxxx`)
- Obvious documentation or README snippets showing example usage
- Files already listed in `.gitignore`

### Phase 4: Risk Report

Present findings to the user in a clear, organized format.

**Report structure:**

1. **Project summary**: Tech stack detected, total files scanned.
2. **.gitignore status**: Exists? Coverage gaps?
3. **Findings table** with columns:

   | Severity | File | Line | What was found |
   |----------|------|------|----------------|
   | 🔴 Critical | `config.js` | 12 | GitHub personal access token |
   | 🟡 High | `.env` | 3 | OpenAI API key |
   | 🟢 Medium | `app.config` | 5 | Database password |

4. **Overall verdict**: SAFE / CAUTION / DANGER with explanation.

**Severity definitions:**

| Level | Criteria |
|-------|----------|
| 🔴 Critical | Production API keys, private keys, GitHub tokens, database credentials that would grant real access |
| 🟡 High | Service tokens, internal API keys, any credential in a file not in .gitignore |
| 🟢 Medium | Suspicious assignments, configuration with credentials, files missing from .gitignore that should be ignored |

**Important — never display full secrets.** Redact them: show first 4 and last 4 characters
with `****` between. E.g., `ghp_****abcd`.

### Phase 5: Remediation

After presenting the report, ask the user whether to proceed with fixes. Do NOT modify
any files until the user explicitly confirms.

**If user confirms, proceed with:**

1. **.gitignore**: Generate or update it.
   - If missing: create a complete `.gitignore` with patterns for the detected tech stack.
   - If incomplete: add the missing patterns. Show what will be added, then append.

2. **Untrack files already committed**: For sensitive files tracked by git, suggest:
   ```bash
   git rm --cached <file>   # stop tracking, keep local copy
   ```
   Then add the pattern to `.gitignore`.

3. **Best practices reminders**:
   - Rotate any keys that may have been exposed — they are compromised!
   - Use `.env.example` with placeholder values instead of committing real `.env`
   - Consider pre-commit hooks: `detect-secrets`, `gitleaks`, or `git-secrets`
   - For production projects, use a secret manager (AWS Secrets Manager, Vault, etc.)

## Important Rules

- **Phase 0 gate is mandatory** — always check exposure risk first. Exit early with a brief,
  friendly message for non-git / local-only / private repos. Do NOT proceed to scanning.
- **Phase 0 exits are final** — do not offer to fix .gitignore, do not ask "是否需要...？",
  do not suggest next steps beyond the one-liner reminder. The user called this skill to
  check for leaks; if there's no leak vector, the answer is simply "没有风险".
- **Only scan the working tree** — do NOT scan git history. History is out of scope.
- **Do NOT modify any files without explicit user confirmation.** Always present findings first.
- **Never display full secrets.** Always redact in the report.
- **Skip binary files** — images, archives, compiled binaries, office documents.
- **Skip common dependency directories** — `node_modules/`, `vendor/`, `.venv/`, `target/`, etc.
- **Respect `.gitignore`** — files already ignored are not a risk (but an untracked `.env` that
  is NOT in `.gitignore` IS a risk).
