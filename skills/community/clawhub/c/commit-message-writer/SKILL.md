# commit-message-writer

## Description
Write Conventional Commit messages from a git diff, code snippet, or plain description. Also generates PR titles and 3-bullet PR summaries. Works with any language and any project — no setup, no config.

## Use when
- "write a commit message"
- "what should I commit this as"
- "conventional commit for this diff"
- "write a PR title and description"
- Any git diff or code change needing a message

## Supported conventions
- Conventional Commits 1.0 (default)
- Angular commit format
- GitHub squash-merge style
- Plain descriptive (no convention)

Request a specific one or it defaults to Conventional Commits.

## Input
Paste one of:
- A git diff (`git diff --staged`)
- A description of what changed ("I added rate limiting to the API")
- Code before/after

Optionally specify:
- Convention (defaults to Conventional Commits)
- Scope (component, module, or area affected)
- Whether this is a breaking change

## Output format

```
## Commit Message

[type]([scope]): [subject]

[body — explains WHY, not just WHAT. Omitted if obvious from subject]

[BREAKING CHANGE: description — only if applicable]
[Closes #123 — only if issue number is known]

---

## PR Title
[short, imperative, under 70 chars]

## PR Summary
- [What changed]
- [Why it changed / what problem it solves]
- [Any notable side effects, caveats, or follow-up needed]
```

## Conventional Commits type guide

| Type | When to use |
|---|---|
| `feat` | New feature (triggers minor version bump) |
| `fix` | Bug fix (triggers patch version bump) |
| `docs` | Documentation only |
| `style` | Formatting, whitespace — no logic change |
| `refactor` | Restructure without changing behavior |
| `perf` | Performance improvement |
| `test` | Adding or fixing tests |
| `chore` | Build system, CI, dependency updates |
| `revert` | Reverts a prior commit |
| `ci` | CI pipeline changes |

## Writing rules
- Subject: imperative mood ("add", "fix", "remove" — not "added", "fixed", "removes")
- Subject: no period at end
- Subject: under 72 characters
- Body: explain WHY the change was made, not just what the diff shows
- Breaking change: always include `BREAKING CHANGE:` footer with migration notes
- Scope: use the module, file, or feature name (e.g., `auth`, `api`, `db`, `ui`)
- If the diff touches multiple concerns: suggest splitting into multiple commits

## Examples

### Simple fix
```
fix(auth): reject expired JWT tokens before checking claims

Previously, token expiry was checked after claim validation,
which allowed attackers to replay expired tokens with valid claims.
```

### New feature with breaking change
```
feat(api)!: require API key on all public endpoints

BREAKING CHANGE: All requests now require `X-API-Key` header.
Clients using anonymous access will receive 401. See migration guide.
```

### Dependency update
```
chore(deps): bump openssl from 1.1.1 to 3.0.8

Addresses CVE-2023-0286 (X.400 address type confusion).
No API changes.
```

## Self-improvement instructions
After each commit message written, note whether the input was a diff, description, or code snippet. After 20 uses, surface the most common missing context that leads to weaker messages.
