---
name: cli-skill-release (English manual)
slug: cli-skill-release
displayName: CLI Skill Release Engineering (releaser.py multi-capability CLI + scaffold + CI + LICENSE + publish + market intelligence)
version: 1.9.6
author: 何巍 (He Wei)
license: MIT-0
description: >
  Release engineering for zero-dependency Python CLI agent skills: releaser.py validates publish-readiness
  (a 0-100 score with real functional checks that actually boot your CLI), inventory/gap market intelligence,
  scaffold, CI, LICENSE(MIT-0), marketplace publish, readiness badge, and back-link badge tooling.
  Pre-publish checklist, skill publish checklist, "is my skill ready to publish?", "what am I missing before
  I push this skill to GitHub?", audit skill against Agent Skills spec, fix LICENSE shows Other, pytest exit
  code 2, CI keeps failing, ClawHub/SkillHub/agentskills.io publish guide, skill discoverability, quality gate.
description_en: "Release engineering for zero-dependency Python CLI skills: validate(score)/diagnose/preflight/badge/publish. Pre-publish checklist, is my skill ready to publish, ClawHub publish guide, skill discoverability."
tags: [publish, skill-publishing, pre-publish-checklist, clawhub, agent-skills, quality-gate, ci, license, mit-0, zero-dependency, python, release]
keywords: cli, python, zero-dependency, skill, release, publish-skill, release-skill, publish, skill-release, skill-publishing, validate, skill-validation, readiness, quality-gate, ci-gate, badge, skill-badge, github-actions, ci, license, mit-0, pytest, scaffold, inventory, gap, diagnose, preflight
---

# CLI Skill Release Engineering — English Manual

> **Philosophy (mirroring find-skills++): methodology becomes a runnable tool; prose degrades to background.**
> find-skills++ uses AST scanning / offline search / lifecycle governance to actively manage agent skills.
> This tool uses `validate` / `inventory` / `gap` / `selfcheck` to actively manage *whether a skill can be reliably published + what the market needs*.

---

## 0. When to use this skill (and the boundary with skill-creator)

**Use this skill when:**
- You want to **build from scratch / publish** a WorkBuddy skill delivered as a Python CLI (zero-dependency preferred).
- You want to **proactively check** whether a skill "can ship, what's missing, what score it gets": `python releaser.py validate --path <dir>`.
- You want to **know what skills the market lacks**: `python releaser.py gap`.
- You hit: `pytest exit code 2`, CI stuck red with no logs, LICENSE shows "Other", publish blocked by `skill-card.md` conflict or Topics over 48 chars.

**Do NOT use this skill when:**
- You only want to **write the SKILL.md content / design trigger descriptions** of a new skill — that's **skill-creator**'s job (it writes; this skill ships + understands the market).

| Dimension | skill-creator (built-in · writes) | cli-skill-release (this skill · ships + intelligence) |
|---|---|---|
| Core question | How to write a good skill | How to reliably publish a CLI tool to market + what to build |
| Executable | `init_skill.py` (generates docs) | **`releaser.py` (19 subcommands, actually runs)** |
| Active capability | none | validate trap-scan + readiness score / inventory governance / gap market intel / selfcheck dep-check |
| CI / LICENSE / publish | not involved | templates + rules + troubleshooting SOP + release manual import intel (see §3) |

> **🔒 Security & Privacy**
> This is a **local-only, zero-dependency** release-engineering assistant that **takes no remote action by default**:
> - Unless you explicitly pass `--push` (git push to remote) or `--publish` (publish via your logged-in `clawhub` CLI), `release` only does a local commit and prints manual-import steps — it never silently touches the remote.
> - **No credential handling**: there is no `--api-token` parameter; the tool stores no secrets and never sends tokens / passwords to any server.
> - **★Security red-line (hard credential-leak gate)**: `validate` / `gate` / `release` **mandatorily scan the whole skill for hardcoded passwords / auth-codes / API tokens** before publishing (the `secretscan` subcommand can be run standalone); on a hit it marks FAIL and **hard-blocks commit / push / publish**, so nothing that shouldn't go to GitHub ever gets committed. Environment-variable references (`os.environ.get(...)` / `${...}`) are treated as safe.
> - **No hidden network egress**: the code contains no `urllib` / `requests` / socket calls. The `api.github.com/.../license` URLs in the docs are public endpoints for *you* to verify LICENSE — the tool itself never calls them.
> - **Read-only scans**: `inventory` / `gap` / `curate` only **read** your locally installed skill directories; data never leaves your machine.
> - **Local ledger**: the `registry` ledger is written only to a local `ledger.json` under your home; it is never uploaded.
> - **No command-injection surface**: all `subprocess` calls use explicit argument lists (no `shell=True`, no string-concatenated commands).
> - **Redacted reporting**: every finding is **redacted** (only first 4 + last 2 chars shown) — **plaintext credentials are never echoed**.

---

## 1. Core tool: releaser.py subcommand overview

Run inside the cli-skill-release skill directory (zero dependency, stdlib only):

| Subcommand | Role | vs find-skills++ |
|---|---|---|
| `scaffold <name>` | one-shot generate a CI-ready publishable skeleton | — |
| `validate --path <dir>` | **★killer feature: active trap-scan + 0-100 readiness + ★functional verification + ★security-redline credential scan** | security scan + reference integrity + **functional verify (no competitor does this)** |
| `secretscan --path <dir>` | **★security red-line: dedicated scan for hardcoded passwords/auth-codes/API tokens (independent of readiness score)** | (unique: hard credential-leak gate) |
| `gate --path <dir> --min 90` | **★CI gate: non-zero exit if score below threshold (readiness-as-a-service)** | (unique: quality gate) |
| `inventory [--roots ...]` | **govern: which installed skills can ship** | install / list governance |
| `gap [--roots ...]` | **market intel: local coverage + combination gaps** (+ `--scan-json` consumes find-skills++ real market data) | (unique: market side) |
| `selfcheck [--path .]` | zero-dep check: scan imports vs `sys.stdlib_module_names` | — |
| `bump [--type patch]` | bump SKILL.md version + append CHANGELOG | — |
| `release --path .` | git push (needs `--push`) + **clawhub publish (needs `--publish`) (or build ClawHub manual import intel)** | — |
| `publish --github --clawhub` | **★multi-registry orchestrator: explicit per-site authorization to publish to GitHub/ClawHub (security gate first, no remote by default)** | (unique: multi-registry dispatch) |
| `badge --path <dir>` | **★back-link badge: readiness badge SVG + back-link snippet** | (unique: reference & attribution) |
| `promote [--path <dir>]` | **★promo toolkit: badge zone + elevator pitch + social copy + back-link playbook** | (unique: reach) |
| `diagnose --symptom "..."` | **★long-tail diagnosis: symptom→root-cause→fix** | (unique: covers long-tail searches) |
| `preflight [--market clawhub]` | **★market-specific pre-publish checklist** | (unique: checklist = content) |
| `registry [list\|show\|add]` | **★state layer: published-skill ledger (auto-registered on release)** | (unique: governance state) |
| `recheck [<slug>]` | **★lifecycle: re-verify published skills, report drift/deprecation** | (unique: continuous governance) |
| `selfdemo` | **★self-proof base: full self-demonstration (claims = demos, vs smoke.py)** | (unique: trust base) |
| `curate [--roots ...]` | **★supply-side curation: proactively tell the ecosystem what to build** | (unique: proactive curation) |
| `doctor [--path <dir>]` | self-check this tool; or run validate on a target dir | self-check gate |

---

## 2. Subcommand usage (with examples)

### 2.1 validate — ★killer feature: active scan + 0-100 readiness + ★functional verification
```bash
python releaser.py validate --path ./my-skill
python releaser.py validate --path ./my-cli --mode cli        # any zero-dep CLI project
python releaser.py validate --path ./my-pkg --mode package  # any zero-dep Python package
python releaser.py validate --path ./my-skill --bench       # benchmark vs top skills
python releaser.py validate --path ./my-skill --rubric      # transparent scoring
```
It **really runs** the following checks and gives PASS/WARN/FAIL, then a **0-100 publish-readiness score** (weighted to 100):

| Dimension | Weight | Check |
|---|---|---|
| frontmatter | 8 | has `name/version/license` |
| license field | 4 | `license` field is MIT/MIT-0 |
| LICENSE-SPDX | 8 | `LICENSE` exists and is recognized by licensee (SPDX) |
| ASCII copyright | 6 | copyright holder name is ASCII (else NOASSERTION) |
| no skill-card | 8 | no ClawHub reserved name `skill-card.md` anywhere |
| doctor gate | 10 | CLI entry `doctor --path .` really exits 0 |
| CI | 8 | CI has `doctor` step + `tee $GITHUB_STEP_SUMMARY` |
| reference integrity | 6 | files referenced by SKILL.md really exist |
| zero dependency | 6 | no third-party imports |
| **★compile** | 8 | **all `.py` compile (no syntax errors)** |
| **★import** | 6 | **entry module imports (no import-time crash)** |
| **★--help smoke** | 10 | **entry `--help` smoke test passes (CLI really boots)** |
| **★security red-line** | 12 | **no hardcoded passwords/auth-codes/API tokens (prevents the v1.9.x credential-leak incident)** |

> **★Functional verification is the differentiator**: skill-lint / agent-skill-linter / @effectorhq/skill-lint / Skill Validator only check paperwork — none actually execute your CLI to prove it boots. That's releaser's unique engine-level verification.

`--mode cli` skips frontmatter / skill-card checks for any zero-dep CLI. `--mode package` generalizes to any zero-dep Python package (adds `pyproject.toml/setup.py/setup.cfg` detection). `--json` outputs machine-readable report; `--bench` adds a benchmark; `--rubric` adds transparent weights. Exit code: 1 if any FAIL, else 0.

### 2.1.1 gate — ★CI gate (readiness-as-a-service)
```bash
python releaser.py gate --path . --min 90     # non-zero exit if score < 90
python releaser.py gate --path . --min 90 --json
```
Turns the readiness score into an orchestratable pipeline gate: below threshold (default 90) → non-zero exit, blocking before publish. Upgrades the tool from "human-run checker" to "quality gate any pipeline can consume."

### 2.2 inventory — governance: which of your skills can ship
```bash
python releaser.py inventory
python releaser.py inventory --roots C:/Users/win/.workbuddy/skills
```
Prints per skill: `skill | lic field | LICENSE | CI | doctor`, with "ready N / needs-work M".

### 2.3 gap — ★market intel: what to build
```bash
python releaser.py gap
python releaser.py gap --roots C:/Users/win/.workbuddy/skills
```
Scans installed skills, buckets them into 8 categories, reports **empty categories (gaps)** and **thin categories (reinforceable)**, with `scaffold` suggestions. Add `--scan-json <file>` to **consume find-skills++ exported real market data** (JSON array of `{name, categories?, keywords?, description?}`) — upgrading "local heuristic" into "real on-sale gap" intel. This is the unique differentiator of the build flywheel: find-skills++ scans gaps → this tool `scaffold` → `validate` → `release` → re-found by find-skills++ → data flows back. Single tools are copyable; the closed loop is not.

### 2.4 selfcheck — zero-dependency check
```bash
python releaser.py selfcheck --path .
```
Scans all `.py` (skips `tests/` and generator `scaffold.py`), lists non-stdlib imports as WARN.

### 2.5 scaffold — one-shot project start
```bash
python scaffold.py my-cli-skill --author "He Wei" --email you@x.com --dest ./out
```
Generates a skeleton that avoids all §3 traps (SKILL.md / `<name>.py` with doctor --path / tests/conftest / CI / LICENSE MIT-0 / listing / README).

### 2.6 bump — version bump
```bash
python releaser.py bump --path . --type minor
```
Bumps `version` and appends a CHANGELOG entry (creates one if missing).

### 2.7 release — local commit + manual import steps (remote needs explicit flag)
```bash
python releaser.py release --path .                 # default: local commit + print manual import steps (no push, no publish)
python releaser.py release --path . --dry-run        # generate import steps only, no commit
python releaser.py release --path . --push           # explicit: git push to remote
python releaser.py release --path . --publish        # explicit: publish via your logged-in clawhub CLI
```
**Safe default**: `release` does **not** touch the remote by default — it only does a local `git add/commit` and prints ClawHub manual-import steps (auto-resolving repo URL, Display/Slug, top-3 categories, Topics ≤48). You must explicitly pass `--push` to `git push`, or `--publish` to call `clawhub publish` (requires `clawhub` CLI installed and `clawhub login` done). No remote write happens without your explicit flag.
> **Honest note**: ClawHub has no public REST/web publish endpoint (can't proxy OAuth), so the web "Publish" button still needs your login session to click once; `--publish` is the legal explicit path when the `clawhub` CLI is installed and logged in. Faster than competitors' "read the doc and click yourself" by an order of magnitude.

### 2.7.1 secretscan — ★security red-line: kill "things that shouldn't go to GitHub"

> **Why this gate is mandatory**: in v1.9.x, cli-skill-release got flagged `malicious.llm_malicious` and Blocked/Hidden on ClawHub because a **plaintext QQ SMTP auth-code had been `commit`+`push`ed to the public GitHub repo**. Passwords / auth-codes / API tokens must be eliminated in the **proofread / review / approve** loop — they must never reach the repo.

`secretscan` is the dedicated hard gate. It runs standalone, and is also auto-invoked by `validate` / `gate` / `release`:

```bash
python releaser.py secretscan --path .                 # scan whole skill for hardcoded creds, FAIL on hit
python releaser.py secretscan --path . --allow-file .my-allow   # custom allowlist regex file
python releaser.py validate --path .                   # validate includes the secret dimension (weight 12), FAIL on hit
python releaser.py release --path . --dry-run          # release hard-blocks at the "approve" stage: creds → no commit/push/publish
```

**Coverage (prefer false positives over missing a real secret)**:
- ① **`.env` files themselves are risky** (any extension, FAIL on hit, forbidden in repo);
- ② **known vendor token formats**: AWS Access Key, GitHub PAT, Slack/Google/Stripe/OpenAI/OpenRouter Key, JWT, PEM private key, `user:pass@host` BasicAuth, etc.;
- ③ **hardcoded credential assignments**: `PASSWORD = "..."` / `api_key="..."` / `client_secret='...'` — only flagged when the **assignment's left-hand identifier** contains a credential keyword, avoiding false positives from docs/strings mentioning password/token (and avoiding the scanner flagging its own definitions).

**Safety design**:
- Environment-variable references are treated as safe (creds injected at runtime, not in repo): `PASSWORD = os.environ.get(...)` / `os.getenv(...)` / `${VAR}` / `{{ secrets.X }}` are all allowed;
- reports are **redacted** (only first 4 + last 2 chars) — **plaintext never echoed**;
- **false positives**: add `.releaser-secret-allow` at repo root with allowlist regexes (use with care — this means you've confirmed no real creds there).

> **Leak response**: if a real credential is already in the repo, you must **① immediately rotate/revoke it at the service** (e.g. QQ mailbox SMTP auth-code) ② `git filter-repo --path <file> --invert-paths` to scrub history ③ force-push to overwrite the old remote history. Rotate the password before deleting code — plaintext in old history is irreversible once leaked.

### 2.7.2 publish — ★multi-registry orchestrator (one command to dispatch a corrected/new skill to multiple registries)

> **Design principle (answers the ClawHub false-positive + your "proofread/review/approve" requirement)**: security gate first, explicit per-site authorization, no remote by default. This carries forward the v1.9.3+ "never silently write remote" remediation — there is **no "push-everything-without-a-flag" path**, structurally preventing a repeat of the malicious flag.

`publish` is the unified entry point for "after a correct update or a new skill, automatically upload to multiple registries":

```bash
python releaser.py publish --path .                      # proofread + preview only, touches no remote (anti silent-send)
python releaser.py publish --github                      # explicit: push to GitHub (git add/commit/push)
python releaser.py publish --clawhub                     # explicit: publish to ClawHub via your logged-in clawhub CLI
python releaser.py publish --github --clawhub            # both (the in-scope set this round)
python releaser.py publish --github --clawhub --dry-run  # preview each site's action only
python releaser.py publish --github --force-history      # force-push when history was rewritten by git filter-repo (--force-with-lease)
```

**Order (each step can be blocked by the gate)**:
1. **Proofread (validate)**: run the publish-readiness scan (incl. ★security red-line credential scan), output 0-100;
2. **Approve (secretscan)**: on a hardcoded credential/auth-code hit → **hard-block publishing to any site**, never commit/send (confirm no false positive to force with `--allow-secret-risk`, dangerous);
3. **Dispatch**: each target needs its explicit flag (`--github` / `--clawhub` / `--xiaping` / `--workbuddy`), untouched otherwise; GitHub uses `git push` (normal fast-forward, `--force-history` when needed), ClawHub uses `clawhub publish` (needs CLI installed + logged in, else falls back to manual import intel).

> **Xiaping / WorkBuddy are reserved this round**: `--xiaping` (xiaping.coze.site, Coze ecosystem) and `--workbuddy` (open.workbuddy.cn SkillHub) only print manual-upload links this round (neither has a public API). Once their open endpoints/bots are wired in, the same explicit-authorization model makes them truly automatic with no usage change.

### 2.8 doctor — self-check
```bash
python releaser.py doctor            # self-check cli-skill-release (structure + zero-dep)
python releaser.py doctor --path .   # equivalent to validate
```

### 2.9 badge — ★back-link badge (users can add a back-link)
```bash
python releaser.py badge --path .                 # print readiness badge SVG + back-link snippet
python releaser.py badge --path . --output readiness-badge.svg   # write SVG to repo
```
Generates a shields-style badge from the validate score (green ≥90 / yellow 70-89 / red <70), plus a markdown snippet for your skill's README — the badge image self-hosts on your repo raw URL and links back to this skill page. This is the point of the back-link badge: every skill you publish hangs this badge; visitors to your repo click in, use it, publish their skill, hang it too — organic referencing grows.

### 2.10 promote — ★promo toolkit (share and reference)
```bash
python releaser.py promote --path .    # shows readiness score first if path given
```
Outputs at once: ① README badge zone ② pitch ("others lint docs, we execute the engine") ③ social/community-ready copy ④ one-line install ⑤ back-link playbook. Paste to introduce the tool to your audience.

### 2.11 diagnose — ★long-tail: symptom→root-cause→fix (covers long-tail searches)
```bash
python releaser.py diagnose --list
python releaser.py diagnose --symptom "LICENSE 显示 Other"
python releaser.py diagnose --symptom "pytest exit code 2"
python releaser.py diagnose --symptom "skill 搜不到"
```
Maps "long-tail problems users actually search" to root-cause + fix — the engine of "covers long-tail searches": someone searches "skill LICENSE shows Other" / "pytest exit code 2" / "CI keeps failing red" / "skill not found"; our README phrases get indexed by search engines/ClawHub → click in → run diagnose → answer. Competitors (jeremyknows/publish-skills etc.) only give static checklists; we give "executable + diagnosable". Known symptoms: LICENSE shows Other, pytest exit code 2, CI stuck red (doctor missing --path), skill-card.md conflict, Topics >48, entry import crash, skill not found, "can my skill ship" (natural-language long-tail).

### 2.12 preflight — ★long-tail: market-specific pre-publish checklist
```bash
python releaser.py preflight --market clawhub       # ClawHub/OpenClaw
python releaser.py preflight --market skillhub      # SkillHub mirror
python releaser.py preflight --market agentskills   # agentskills.io/GitHub open standard
python releaser.py preflight --market generic       # generic (default)
```
Outputs a market-specific pre-publish checklist (markdown checkboxes + required/suggested tags), each mapped to real rules (MIT-0, skill-card.md reserved name, Topics≤48, 3 categories, text-only files, GitHub topics, `gh skill publish --dry-run`). Directly answers long-tail searches: "skill publish checklist" / "pre-publish checklist for agent skills" / "what am I missing before I publish" — the checklist itself is indexable when pasted into README.

### 2.13 registry — ★state layer: published-skill ledger (governor base)
```bash
python releaser.py registry list
python releaser.py registry show cli-skill-release
python releaser.py registry add my-skill --name "My" --repo https://github.com/me/my-skill --version 1.2.0 --score 100 --market clawhub
```
`release` registers every publish (whether clawhub CLI explicit publish or manual import) into a local ledger (default `~/.workbuddy/cli-skill-release/ledger.json`, override with `RELEASER_LEDGER`). This lets the tool **hold a "published-skill ledger" across runs** — from one-shot checker to publish-side **governor** (vs find-skills++ state layer / full lifecycle governance).

### 2.14 recheck — ★lifecycle: re-verify / drift governance (continuous governance)
```bash
python releaser.py recheck
python releaser.py recheck my-skill
```
Re-runs `validate` on each published skill, compares to the registered score, reports **drift** (score dropped), **deprecation** (now FAIL / below gate), **missing** (local dir moved), **healthy**. Upgrades "ship-and-forget" to **continuous governance** — the "fate of governing skills", and the counterpart to find-skills++ lifecycle governance.

### 2.15 selfdemo — ★self-proof base: full self-demonstration (claims = demos, vs smoke.py)
```bash
python releaser.py selfdemo
```
Runs every capability on its own repo (validate / selfcheck / badge / preflight / diagnose / registry / gap / recheck) and prints demo summaries — **claims = demos**: proof that "others lint docs, we execute the engine" is not a slogan but a verified fact. Vs find-skills++'s `smoke.py` (full self-proof) — verifiable trust comes from running it in front of you, not narration.

### 2.16 curate — ★supply-side curation: proactively tell the ecosystem what to build (upgraded gap)
```bash
python releaser.py curate
python releaser.py curate --scan-json market.json   # overlay find-skills++ real market data
```
Upgrades `gap`'s market intel into an actionable curation list: combining local published (incl. ledger) with optional market data, outputs by priority "what to build" — ① combination opportunities (market has supply / you at 0, build most) ② local empty categories ③ thin categories. From passively waiting for searches to **proactively curating** (vs find-skills++ proactive curation), making the tool the ecosystem's "supply-side brain".

---

## 3. Background: publish-trap quick reference (prose, on demand)

### 3.1 sys.path injection (pytest exit code 2 classic root cause)
A CLI adds `scripts/` to `sys.path` at module level then imports — the CLI runs fine itself; but `tests/` importing directly depends on conftest injection.
**Correct**: inject root + `scripts/` in `tests/conftest.py` (scaffold writes this). Exit codes: `2`=collection crash (import/syntax), `1`=test fail, `0`=pass, non-zero reddens CI.

### 3.2 self-test gate doctor must define `--path`
In CI, `python main.py doctor --path .` — the `doctor` subcommand **must really define `--path`**, else `unrecognized arguments: --path .` fails on **all platforms**, reddening the whole job — and pytest's traceback won't show it (it's a separate step). This is the **real culprit** behind find-skills++'s early CI staying red.

### 3.3 LICENSE recognized by GitHub licensee
- Multiple copyright lines / **non-ASCII holder name** (e.g. Chinese "何巍") → easily judged `NOASSERTION` / **Other**.
- ClawHub forces **MIT-0** redistribution → writing LICENSE as **MIT-0** directly is safest.
- When deriving upstream: new self-built content uses MIT-0, and create a **`NOTICE`** fully preserving the upstream MIT copyright + license text (satisfies attribution).
- Verify (no login): `api.github.com/repos/{owner}/{repo}/license` → `license.spdx_id`.

### 3.4 ClawHub / SkillHub publish rules (2026 measured)
1. **MIT-0 forced** (not MIT).
2. **`skill-card.md` is a reserved name**: a same-named file at repo root (incl. subdirs/fixtures) errors `skill-card.md is generated by ClawHub and cannot be published directly` → rename repo-wide (e.g. `market-card.md`); `git ls-files | grep skill-card` to scan all.
3. **Topics ≤48 chars (whole string, commas included)** — not per-tag. Fill the shortest combo to pass (e.g. `skill-discovery, security`).
4. **GitHub account age ≥1 week**.
5. **Pick 3 categories** (Developer Tools / Security / AI & ML etc.).
6. **Post-publish verify loop**: contains `<main>.py`+`scripts/`, License shows MIT-0, SkillHub mirror searchable; new commits make the online listing show "Import is out of date" (published skills unaffected; click Re-run preview to sync new files).

#### 3.4.1 ClawHub CLI ops (local)
- Install: `npm i -g clawhub` (this machine: `node/workspace/node_modules/.bin/clawhub`).
- **Windows must call the `.cmd` wrapper** (`clawhub.cmd`); calling the node bin directly crashes on PATH errors.
- Check login: `clawhub whoami` (returns `Not logged in` if not).
- Check publish status: `clawhub search <slug>` (no login needed, returns `@owner DisplayName installs/60d`).
- After `clawhub login` (also supports device flow), run `clawhub publish`.
- Without login, `release` falls back to "manual import intel" (see §2.7) — you click Import once on ClawHub web.
- ClawHub **8 fixed categories, must pick 3**: Developer Tools / Security / AI & ML / Data / Productivity / Web / Finance / Content.

#### 3.4.2 Verify "published" (search index lags)
- `clawhub search <slug>` may **not immediately show** a freshly published skill (index lag, returns other skills with the same word) — **not found ≠ not published**.
- **Do NOT** verify via the OG image endpoint (`https://clawhub.ai/og/skill?...`): it returns HTTP 200 + a placeholder image for **any** slug (including non-existent ones), so it is NOT proof of publication. Verify via `clawhub inspect <owner>/<slug>` (public skills, no login) or `clawhub search <slug>` instead.
- Page `og:title` should be `<slug> — ClawHub`, `og:description` contains `Agent skill by @<owner>`; loads the `InstallCopyButton` module (published-only UI).

### 3.5 CI troubleshooting SOP (no logs: 403 / needs admin)
1. `git ls-remote origin HEAD` to confirm the actually-deployed commit (local `ahead N` = N unpushed).
2. Public API check LICENSE: `api.github.com/repos/{owner}/{repo}/license`.
3. Local venv pytest to reproduce: exit `2`=collection error, `1`=test fail.
4. Run each step command locally, focus on subcommands with undefined args.
5. In CI, `tee` pytest output to `$GITHUB_STEP_SUMMARY` (see §3.3 reference integrity / 3.4 publish).

### 3.6 Environment & tool gotchas (Windows sandbox measured)
- **bash shim occasionally loses PATH** → call scripts with Python **absolute paths**.
- **phantom cache** → verify key changes by reading disk directly with Python (`open(path, encoding='utf-8')`).
- **push may be silently blocked by sandbox** (empty output, remote unchanged) → disable sandbox and re-push, then `git ls-remote` to confirm remote HEAD advanced.
- **GitHub API password auth is disabled** (measured `POST /user/repos` returns `401 Requires authentication`): creating a repo only via ① authenticated SSH (can only push **existing** repos, can't create) ② **PAT (classic, repo scope)** ③ user creates empty repo on GitHub web. Password can't be used for API / repo creation.
- **clawhub CLI on Windows needs the `.cmd` wrapper** (see §3.4.1).
- **pytest bulk-delete guard**: teardown cleaning temp dirs may raise `SystemExit: 1` ("Exception ignored"), **doesn't affect result** (returncode 0, all passed); run tests in a separate subprocess writing results to a file to avoid the guard killing the result write.

---

## 4. Publish checklist (verify each before delivery)
- [ ] `python releaser.py validate --path .` → zero FAIL, score near 100
- [ ] `python releaser.py secretscan --path .` → no hardcoded credentials (security red-line passed)
- [ ] `python releaser.py selfcheck` → zero WARN (or only known false positives)
- [ ] `doctor` and `doctor --path .` exit 0
- [ ] LICENSE is MIT-0 + ASCII holder name; public API confirms `spdx_id=MIT-0`
- [ ] CI workflow exists and badge points to it; pytest output teed to Step Summary
- [ ] multi-registry: `publish --path .` (preview only) first, then `publish --github --clawhub` (explicit, gate-first)
- [ ] `git ls-remote` confirms all fix commits pushed (no `ahead N`)
- [ ] no `skill-card.md` residue repo-wide
- [ ] publish: License MIT-0, 3 categories picked, Topics whole-string ≤48 chars
- [ ] post-publish verify: contains `<main>.py`+`scripts/`, SkillHub mirror searchable
- [ ] (optional) `python releaser.py gap` to see local category coverage, decide next build

---

## 5. How this skill gets found + back-link badge (docs explain referencing)

This skill doesn't just "work well" — it's designed to be **actively found, continuously needed, and self-spreading**. The mechanism is built into the tool:

1. **Found by AI**: at publish, `keywords`/`description` hit high-frequency queries — "publish skill / 上架 skill / validate skill / 技能质量门禁 / skill CI gate / 技能徽章". AI discovery tools (find-skills++ etc.) match on these words and recommend.
2. **Found by humans**: ClawHub/SkillHub optimization (MIT-0, 3 categories, Topics≤48) + badges visible in every user's repo (word-of-mouth exposure).
3. **Continuously needed**: every publish and update re-runs `validate`/`gate`/`badge` — it's a **required step** in the publish pipeline, not a one-time download; badges refresh with version, forming habit dependency.
4. **Actually solves problems**: ★functional verification (compile+import+--help really boots CLI) blocks "perfect format, crashes on run" — hard value no competitor does.
5. **Back-link badge**: `badge` lets every user hang a back-link badge in their skill repo → the next skill author clicks in → may hang it too → one download, organic referencing. With the `promote` toolkit, users can introduce the tool to their audience.

### 5.1 How Chinese / English get found (measured retrieval mechanics)
**Chinese channel (AI discovery = keyword/text match)**: AI discovery tools do local `ls` → native market search by `keyword` → community source returns `score` (matches `name/description`, ignore <0.05) → merge sort. So `keywords`/`description` must hit Chinese high-frequency words — we already do (发布技能/上架/校验/门禁/徽章/长尾诊断/上架清单). Human channel: ClawHub/SkillHub search box, GitHub topics, WeChat official account, search engines — via **Chinese long-tail titles in README + GitHub topics (agent-skills, claude-skills, skill-md, ai-agents) + badge word-of-mouth**.

**English channel (evaluation: three levers)** — 2026 measured evidence:
- **Lever 1: `description` is the vector-search match surface** (ClawHub officially: "The SKILL.md description is what vector search matches on"). We wrote `description` as bilingual with English trigger phrases + added `description_en`.
- **Lever 2: `tags` decide adjacency** (tags put you next to elevenlabs-tts etc.). We added `tags: [publish, skill-publishing, pre-publish-checklist, clawhub, agent-skills, ...]`.
- **Lever 3: GitHub topics feed external indexers** (SkillsMP / skillsdirectory / claudeskills.info). At publish: `gh repo edit --add-topic agent-skills claude-skills codex-skills skill-md ai-agents`.
- **Natural-language long-tail triggers**: English users love "Is this skill ready to publish?" / "What am I missing before I push this skill to GitHub?" / "Audit this skill against the Agent Skills spec" — these phrases are already in our `description` and README FAQ titles.

### 5.2 Long-tail words & long-tail features (cover long-tail searches)
**Long-tail words (CN)**: 技能发布前检查清单、ClawHub 上架教程、skill LICENSE 显示 Other 怎么办、pytest exit code 2 修复、技能 CI 一直红、agent 技能发布流水线、技能质量门禁、发布就绪分、技能徽章、零依赖 Python 发布、技能搜不到怎么办.
**Long-tail words (EN)**: skill publish checklist、pre-publish checklist for agent skills、is my skill ready to publish、what am I missing before I push、audit skill against Agent Skills spec、skill LICENSE shows Other、pytest exit code 2、ClawHub publish guide、make my skill discoverable、agent skill CI validation.
**Long-tail features (shipped)**: `diagnose` (symptom→root-cause→fix, answers the above searches directly; competitors give static checklists, we give executable diagnosis); `preflight` (market-specific publish checklist, answers "pre-publish checklist" searches; the checklist itself is indexable in README); `README.md` (long-tail questions as H2/H3 titles, bilingual, indexed by search engines/ClawHub/GitHub); `release` defaults to manual import, or `--publish` if the `clawhub` CLI is installed and logged in.

> Docs explain referencing: the skill's docs clearly explain how to reference and credit this tool.

### 5.3 System upgrade: from "publish tool" to "publish-side governance system" (vs find-skills++)
v1.9.0 upgraded cli-skill-release from a one-shot publish tool to a publish-side governance system, filling 4 pillars find-skills++'s governance model was missing:

| Pillar | Subcommand | Problem solved |
|---|---|---|
| **A state layer** | `registry` | holds "published-skill ledger" across runs, from blind to governor |
| **B lifecycle** | `recheck` | continuous governance after ship, drift/deprecation/missing visible |
| **E self-proof base** | `selfdemo` | claims = demos, trust not from narration (vs smoke.py) |
| **F supply-side curation** | `curate` | proactively tells ecosystem what to build, passive → active |

> **Moat essence**: find-skills++ holds the "discovery-side governance seat"; we added the "publish-side governance seat" via v1.9.0. Once the two seats connect (C/D bidirectional live channel: let find-skills++ read this tool's readiness signals + this tool consume its market data), it's a truly uncopyable closed loop — **single tools are copyable, bidirectional governance loop is not**. C/D needs find-skills++ interface + your authorization; this round reserved `releaser.py gap --scan-json` and ledger data structure as the dock base.
