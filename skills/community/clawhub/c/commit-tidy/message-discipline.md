# Commit Message Discipline

Conventional Commit conventions, PUBLIC repo English enforcement, Git operation-type continuity, `--amend` message refresh, source-code `.md` behavior verbs. Covers EVERY commit-message write path: `git commit -m`, heredoc, `-F`, `--amend`, `gh pr create --title`, and similar.

## When to use

- Before every `git commit` (including `--amend`, `rebase --interactive edit`)
- Before composing PR title / body when the body is derived from commit messages
- When choosing a Conventional Commit tag for a change
- When the diff includes `skills/**/*.md`, `rules/**/*.md`, or `.claude/rules/**/*.md` files

## Conventional Commit base (HARD STOP)

- Tags: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `ci`, `perf` — **no other tags allowed**. Forbid invented tags like `infra:`, `build:`, `wip:`
- Repo-visibility language: **PUBLIC = English enforced, PRIVATE = native-language default** (see opensource.md visibility table). Per-medium separation — commit / PR / issue / comment all follow the same visibility rule
- Open-source contributions: see `opensource.md`
- Wrong commits → fix with a new commit. `--amend` + force-push is allowed only when the user explicitly instructs it

## Default commit message structure (HARD STOP)

**Default commit message form is a `<subject>` line, a blank line, a `<body>`, optionally another blank line and a `<footer>`.** A body is recommended for every commit. A footer is optional.

```text
<type>(<scope>): <subject>

<body>

<footer>
```

### Body authoring

- **Recommended for every commit.** Do not stop at the subject line by default
- **Not restricted to per-file enumeration** — the body may be free-form prose, a bulleted list of changes, motivation, before/after, trade-offs, or any combination. Per-file enumeration is one option, not the required form
- The subject explains the *what* compactly. The body adds the *why* and the wider *what* that does not fit in the subject (rationale, scope details, behavioral consequences)

### Footer

- **Optional**
- Common uses: `Closes #<issue>`, `Fixes #<issue>`, `Refs #<issue>`, `BREAKING CHANGE: <description>`, `Co-Authored-By: <name> <email>`, `Reviewed-by: <name>`

### Subject-only acceptable cases

- Typo / single-character fix where a body would only repeat the subject
- Routine dependency bump where the body adds no information

### Don't / Do

| # | Don't | Do |
|---|-------|-----|
| 1 | `git commit -m "feat(scope): subject"` — stop at the subject line | `git commit -m "feat(scope): subject" -m "<body>"` or HEREDOC (`git commit -F -`) for multi-line body |
| 2 | Body restricted to a per-file enumeration | Body can be free-form (prose / bullets / sections / mixed). Per-file enumeration is one option, not the only one |
| 3 | "Diff is small, so subject is enough" autonomous skip | Author a body whenever a body would help future readers — most commits qualify. Subject-only is the exception, not the default |
| 4 | Use the footer for prose that belongs in the body (e.g., motivation, trade-offs) | Footer = machine-readable references (`Closes`, `BREAKING CHANGE:`, `Co-Authored-By:`). Prose goes in the body |
| 5 | Skip the blank line between subject ↔ body ↔ footer | Maintain blank-line separators — Git tooling (`git log --oneline`, GitHub squash) relies on them |

### Bash invocation forms

```bash
# Form 1 — repeated -m (each -m becomes a paragraph; Git inserts blank lines between them)
git commit -m "feat(scope): subject" -m "<body prose or bullets>" -m "Closes #<issue>"

# Form 2 — HEREDOC via -F - (preferred for richer body / footer)
git commit -F - <<'EOF'
feat(scope): subject

<body — prose or bullets, multi-paragraph if needed>

Closes #<issue>
EOF
```

### Self-check (every time before writing a commit message)

1. Did you author a body? — subject-only is the exception (typo / dep bump). Default = body present
2. Is the body restricted to per-file enumeration when free-form would explain more? — switch to free-form prose / bullets
3. Footer present? — only for `Closes` / `Fixes` / `Refs` / `BREAKING CHANGE:` / `Co-Authored-By:` / `Reviewed-by:` style references. Prose belongs in the body
4. Blank line between subject ↔ body ↔ footer? — Git tooling depends on the blank-line separators
5. PUBLIC repo? — body + footer are also subject to the English enforcement rule below

## PUBLIC repo English enforcement (HARD STOP)

**Before every commit, verify repo visibility + commit-message language as primary sources. If PUBLIC, English is mandatory.** Stops the pattern where native-language thinking leaks straight into the commit body.

### Why

- PUBLIC repo commit history is permanent (force-push amend still leaves it in forks / clones)
- "Conventional Commit tag (`ci:` / `feat:`) is English but the body parenthetical is the native language" — a frequent mix pattern where the author's native-language thinking transfers verbatim
- Native-language thinking leaks into commit bodies more often than into the code itself

### Don't / Do

| # | Don't | Do |
|---|-------|-----|
| 1 | PUBLIC repo with native-language words / sentences in the commit message (e.g., subject English + body mixed with a native-language parenthetical) | Subject + body + every parenthetical aside in English |
| 2 | "Conventional Commit tag in English, body in native language" mix pattern | Tag + subject + body all English. The note after a hyphen is also English |
| 3 | "User decided / instructed in their native language, so the commit message tracks it" | The user's decision language ≠ the commit-message language. Commit medium always follows the visibility rule first |
| 4 | Skip the visibility check right before commit ("I already know this is PUBLIC") | Run the visibility check at every commit — `gh repo view <repo> --json isPrivate -q '.isPrivate'`. If you confirmed earlier in the session, you may skip |
| 5 | Assume PoC / draft / temporary commits are exempt from English enforcement | PUBLIC repo PoC commits are still English. Discarding the branch does NOT erase fork/clone history |

### Self-check (every time before writing a commit message)

1. Is the target repo PUBLIC? — most recent visibility check + `isPrivate=false`. PRIVATE skips this rule (native-language default)
2. Does the drafted subject + body contain any non-English characters in the relevant native script? — mental grep right before the Edit / Bash call
3. 1+ matches → translate immediately. Parenthetical asides, post-hyphen notes, code-review summaries all included
4. Visual whole-message inspection right before `git commit -m` / `-F` / heredoc
5. Post-amend force-push: visually verify the final commit message is English. Mechanical check is a heuristic only: `git log -1 --format=%B | grep -P '[^[:ascii:]]'` rejects non-ASCII characters (catches CJK/accented native scripts) but does NOT cover ASCII-only non-English text (e.g., romanized Korean/Japanese) — pair with a language-aware validator when available, or scope the check to "non-ASCII characters" rather than treating it as definitive "non-English"

### Exceptions

- PRIVATE repo (`isPrivate=true`) — native-language default (opensource.md visibility table)
- User explicitly says "this commit in <native language>" (PUBLIC + explicit override only)

### Escalation

Cumulative violations → escalate to a PreToolUse:Bash hook (`git commit` command + PUBLIC repo visibility + native-language match → block).

## Git operation-type continuity (HARD STOP)

**When the user's immediately-prior ask / turn specified a Git operation type (amend / new commit / cherry-pick / rebase / squash / force-push), the same type is the default for the related next decision.** Switching to a different operation type requires an explicit user confirmation ask.

### Why

- The user's intent is expressed through a single operation type. amend = history-cleanliness intent. new commit = step-by-step intent. cherry-pick = selective-application intent. rebase = linear-history intent
- After the user has specified a type, using a different type for the next decision = ignoring their intent
- Especially when **history-cleanliness** has been declared (amend), switching to a separate commit for the follow-up directly violates that intent. An automation-tool-made wrong commit (e.g., release-please) being "fixed" with a separate downgrade commit accumulates dirty history

### Don't / Do

| # | Don't | Do |
|---|-------|-----|
| 1 | User said "amend" → next decision uses a separate commit instead | Keep the same amend type. Switching types requires an explicit ask |
| 2 | "Separate commit is safer (avoids force-push)" as the default heuristic | If the user specified amend, amend IS the default. Force-with-lease is safe enough |
| 3 | Automation-tool wrong commit (e.g., release-please 0.5.0 bump) → fix with a separate downgrade commit | Fix the automation's commit via amend directly. Keep PR head as a single clean commit. Remove the wrong trace from history |
| 4 | "User's stated operation is for that ONE turn only" | When the user specifies a type, it applies to the entire active work-flow. The next decisions inherit it automatically |
| 5 | "Force-push is risky" → avoid amend follow-up + add a separate commit | If the user said amend + force-push, force-with-lease is the right move. Verify CI is not in progress, then push |

### Self-check (every time before creating a commit)

1. Did the user's immediately-prior ask / turn specify a Git operation type?
2. If yes, is the current decision the same type?
3. About to use a different type? → halt → ask for explicit user confirmation
4. Fixing an automation-tool wrong commit? → history-cleanliness priority → amend
5. About to default to "avoid force-push"? → if the user already specified amend, amend + force-with-lease is the right answer

### Exceptions

- User did not specify a type → default = new commit (safe)
- Amend target is someone else's published commit, OR a protected branch (main/master) → force-push is forbidden by the higher rule

## `--amend` requires message refresh

**When `git commit --amend` adds or changes files, the commit message MUST be updated.**

- `--no-edit` is forbidden (the message ends up inconsistent with the actual change)
- **Exception**: typo fixes, formatting, etc. — change types that do NOT need a message update

## Semantic Versioning order

**Pre-release tags are always ORDERED BEFORE their corresponding release** (semver 2.0.0 spec):

```text
v0.4.7 < v0.4.8-beta.0 < v0.4.8-beta.1 < v0.4.8
```

- `v0.4.8-beta.0` is a **pre-release of `v0.4.8`** — it ships earlier than `v0.4.8`
- Apply this ordering when comparing tags, computing changelog ranges, or sorting

## Tag selection criteria

- `feat`: user-facing functional additions (UI, API endpoints, CLI commands)
- `test`: test code add / update (test files, fixture data, test config)
- `ci`: CI/CD workflows, test infrastructure setup (GitHub Actions, Playwright config, CI config)
- **Test infrastructure + test code mixed** → `ci`
- `feat` NOT allowed for: e2e test additions, test fixture additions, CI pipeline additions

## Working-tree-specific commit-type override (HARD STOP)

**Before applying the global tag-selection criteria above (or the "Verb selection" defaults below), check the working tree's local rules directory (`<repo>/.claude/rules/*.md`) for a commit-type / version-bump override. Local rules take precedence over the global defaults.**

### Why

- Release automation (release-please, semantic-release, changesets) reads commit types as version-bump signals. A workspace may bind `feat:` to "new topic / new skill" and a more restrictive type (`fix:` / `chore:`) to in-place edits of existing topics, precisely to keep `minor` bumps tied to publish-worthy surface changes.
- The global default "skill/rule `.md` behavior change ⇒ `feat:`" (Verb selection row 3) is too coarse for these workspaces — every HARD STOP added inside an existing topic would trigger a `minor` bump even when the topic's surface is unchanged.
- Local rules in `.claude/rules/` are loaded into the assistant's context but are not reached automatically during commit drafting. A procedural self-check is required.

### Self-check (every time before drafting a commit message)

1. `git rev-parse --show-toplevel` → `<repo>`
2. `find <repo>/.claude/rules/ -name '*.md' 2>/dev/null` — does the workspace ship any local rules?
3. If 1+ files exist, grep them for commit-type / version semantics: `grep -liE 'commit type|conventional commit|version bump|feat|fix|topic' <repo>/.claude/rules/*.md`
4. Read each match. If a local rule defines its own mapping (e.g., "new topic = feat, in-place edit of existing topic = fix"), **the local rule wins**. Re-classify the staged diff under the local rule before composing the subject
5. If no local rule applies, fall back to the global defaults below ("Verb selection" + "Tag selection criteria")

### Don't / Do

| # | Don't | Do |
|---|-------|-----|
| 1 | Apply the global "`.md` behavior-change addition ⇒ `feat:`" rule without checking the working tree's `.claude/rules/` | Run the self-check (`find <repo>/.claude/rules/ -name '*.md'`) first. If a local mapping exists, defer to it |
| 2 | Treat the local rule as "informational only" and stick with the global default | Local rule overrides the global default. The override is the source of truth for the commit type, not a suggestion |
| 3 | Add an HARD STOP / Don't-Do row to an existing topic and prefix `feat(skill-X):` autonomously | Inspect the diff for "new topic file / new SKILL.md Topics-table row." None? → look for the local rule's classification (`fix` / `chore` / etc.). Many → `feat:` only when a topic file actually appears |
| 4 | Self-check the local rule once per session and assume it still holds for later commits | The diff scope changes per commit. The classification is per-commit, not per-session |

### Example mapping (illustrative — actual mapping comes from the local rule file)

A workspace whose `.claude/rules/branch-policy.md` defines:

| Change | Tag | Bump |
|--------|-----|------|
| New topic file added (e.g., `skills/<slug>/<new-topic>.md`) | `feat:` | minor |
| In-place edit of an existing topic (new HARD STOP / Don't-Do row / Self-check) | `fix:` | patch |
| Body cleanup / wording only | `chore:` | none |

… would classify a commit that adds 3 HARD STOP sections inside `skills/X/existing-topic.md` (no new topic file, no new Topics-table row) as `fix(X): …`, **not** `feat(X): …` — even though the diff adds new agent behavior.

## Verb selection — skill/rule `.md` is source code (HARD STOP)

**For commits that change `skills/**/*.md`, `rules/**/*.md`, or `.claude/rules/**/*.md`, the verb MUST state the behavior change. Documentation verbs (`document`, `describe`, `note`) are forbidden in this case.**

Why: these files are **runtime instructions consumed by AI agents**. Adding / editing markdown text means adding / editing agent behavior — not recording existing behavior. Being fooled by the `.md` medium into framing the commit as "documenting" causes new HARD STOP / Don't-Do / self-check additions to be mis-prefixed as `docs:`.

### Allowed verbs vs forbidden verbs

| Kind | Verbs |
|------|-------|
| **Behavior-change verbs** (use in skill/rule `.md`) | `add`, `introduce`, `require`, `mandate`, `enforce`, `prohibit`, `forbid`, `allow`, `replace`, `restructure`, `remove`, `tighten`, `relax`, `extend` |
| **Documentation verbs** (forbidden in skill/rule `.md`) | `document`, `describe`, `note`, `clarify wording`, `fix typo` (typo / wording-only — strictly behavior-unchanged cases) |

### Don't / Do

| # | Don't | Do |
|---|-------|-----|
| 1 | `feat(wip): document Copilot rate-limit cache write` | `feat(wip): require Copilot rate-limit reset timestamp shared-cache write` |
| 2 | `docs(skill-X): describe new behavior` (when actually adding new behavior) | `feat(skill-X): add / introduce / enforce new behavior` — `docs:` is for **behavior-unchanged** changes only |
| 3 | "`.md` text addition = `docs:`" reasoning | skill/rule `.md` is AI source. New rule / HARD STOP / Don't-Do row addition = `feat:` **by global default**, but the "Working-tree-specific commit-type override" above wins when the workspace's `.claude/rules/` defines a stricter mapping (e.g., in-place edit of an existing topic = `fix:`). Rule removal = `feat:` (behavior change) by default, also subject to the local override. Meaning-preserving refactor = `refactor:` |
| 4 | Use a behavior verb but body says "documents that X must Y" — prose-frames it as documentation | Body too: "this commit changes how the agent behaves: X must now Y". Avoid "documents …" phrasing |

### Self-check (every time before drafting a commit message)

1. Do the changed files include any of `skills/**/*.md`, `rules/**/*.md`, `.claude/rules/**/*.md`? — 1+ match
2. If yes, does the commit-message verb match the "documentation verbs" row?
3. If a match → re-verify the diff: is it actually new behavior / HARD STOP / Don't-Do / self-check addition?
4. Behavior change → pick a verb from the "behavior-change verbs" row. If the type prefix was `docs:`, change it to `feat:`

### Exceptions

- skill/rule `.md` file but the change is purely typo / formatting / link fix — behavior unchanged → `docs:` + documentation verb OK
- skill/rule `.md` external references / example text only (no rule / procedure change) → `docs:` OK

## Related topics

- `staging-discipline` — runs BEFORE this (the staged set must be intentional before drafting a message)
- `security-scan` — runs BEFORE this (PUBLIC repo body scan must pass before drafting English-language message)
- `interactive-amend` / `soft-reset-amend` — when messages on prior commits must be rewritten
