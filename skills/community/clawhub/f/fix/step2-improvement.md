# Step 2: Prompt Improvement (Prevent Recurrence) — never skip

**Step 2 execution gate (HARD STOP)**:
If Step 1 produced even one Why, Step 2 is **mandatory**. The deliverable depends on recurrence count and the 4-filter gate below:

- **1st-2nd recurrence (default)**: record the lesson, **medium split by content type (HARD STOP — FA single-location rule)**:
  - **Case history** (violation-case quote, date, Nth-recurrence count, "how to apply" tied to a specific incident) → **`~/.claude/skills/cleanup/data/failed-attempts.md` (HOT)** via `/cleanup retrospect`. Violation cases live ONLY in failed-attempts.md — **never in `memory/feedback_*.md`**. Writing a violation-case + date entry to a `feedback_*.md` file violates the FA single-location rule (`rules/failed-attempts.md`).
  - **Pure user preference** (how-to-work guidance with NO violation-case quote, NO date, NO Nth-count) → a `feedback` memory entry is acceptable. The moment a date / violation-quote / recurrence-count appears, it is case history → route to failed-attempts.md instead.
  - Neither requires a rule-file Edit. failed-attempts.md (HOT) costs 0 always-on tokens and is searchable via the `/cleanup retrospect` recurrence pre-check.
- **3rd+ recurrence**: rule-file Edit is allowed **only if the 4-filter gate passes** (see below). If any filter fails → stay in memory + route to skill/hook/CLAUDE.md instead.
- **4th+ recurrence with deterministic pattern**: hook implementation (script + settings.json registration + parse verification). Rule body minimizes to a pointer to the hook.
- **AskUserQuestion mandatory before rule-file Edit (HARD STOP — every time)**: adding a new Don't/Do table OR a new self-check procedure section to a rule file requires explicit user ask first. Passing the 4-filter gate does NOT exempt the ask. The user must decide on the location (`~/.agents/rules/` vs `<repo>/.claude/rules/` vs inside a skill), the strength (HARD STOP vs note), the number of Don't/Do rows, and the length of the self-check procedure. Editing without ask = imposing always-on context cost without user consent. 1st-stage default = `feedback` memory OR a short skill cross-ref + failed-attempts entry (on-demand mediums). When rule strengthening is needed at 2nd+ stage, prefer hook → lazy-loaded skill invocation first to avoid the per-session always-on cost. See also: `rule-kit/add.md` same obligation.

**4-filter gate for rule-file Edit (ALL must pass — entered at 3rd+ recurrence)**:

| # | Filter | Meaning |
|---|--------|---------|
| 1 | **Destructive/irreversible/security impact** | Secret leak, destructive git, prod/infra damage, permission escalation. "Inconvenience" or "ugly" fails |
| 2 | **3+ verified recurrences** | 1st-2nd = feedback memory only. Recurrence cluster must share the same pattern |
| 3 | **Deterministic pattern** | Objectively judgeable via grep/regex/structure. "Depends on context" patterns can't be enforced — rule will be bypassed every time |
| 4 | **Always-on cost < violation cost** | Rule takes session tokens. Violation cost (time/money/data) per incident × remaining sessions must exceed rule load cost |

Failing any filter → route to other medium per the table below:

| Pattern | Routing target |
|---------|----------------|
| Domain knowledge / procedure | skill (on-demand) |
| 1st-2nd-time case note | `feedback` memory |
| Project-bounded policy | workspace CLAUDE.md / `.claude/rules/` |
| "Recommended" / "would be nice" | drop (rules enforce, not suggest) |
| Deterministic + automatable | hook (rule is fallback only) |

Zero Edit/Write **on the rule file** is allowed when memory + skill/hook is the chosen medium. Step 2 is complete when the chosen medium received its deliverable.

| # | Don't | Do |
|---|-------|-----|
| 1 | Write Why as inline text only (no medium produced) | Produce the Why's deliverable in the chosen medium per the Priority table (memory feedback is the 1st default for 1st-2nd recurrence) |
| 2 | Assume "current issue is resolved, so Step 2 is unnecessary" | Resolving current issue = Step 3, recurrence prevention = Step 2. Both are mandatory (medium may be memory, not rule) |
| 3 | Shorten Step 2 in later fixes within a chain | Every /fix call is the same quality. No shortening by call count |
| 4 | Edit a skill/rule file after partial Grep (e.g., only "Step 7", "Summary" keywords) | **Read the entire file** before any Edit. Skill files have section dependencies (templates, MANDATORY markers in other sections) — partial Grep can miss the existing canonical answer and lead to inventing redundant/conflicting rules |
| 5 | Invent a new title/template/keyword when the user reports a missing element | First Grep the target skill for existing templates/MANDATORY markers (e.g., `Grep "template\|MANDATORY"`). The user's report often refers to an existing template that wasn't followed, not a missing one |
| 6 | Build complex matching tables (skill lists, file presence checks) for rule criteria | **Prefer the simplest 1st-class signal first**. Before authoring a matching table, ask "is there a single field/line that decides this?" (e.g., SKILL.md frontmatter `description` language decides skill language — no publish-target table needed) |
| 7 | Author vendor-specific code (URL, skill name, MCP tool name, instance-bound command) into a generic skill body | Before authoring integration in a generic skill, **grep vendor skill docs for existing dispatch design**: `grep -rE "<generic-skill-name>" ~/.claude/skills/<vendor>/`. If found, follow that pattern. Generic skill declares abstract dispatch (`--<verb>=<skill>:<topic>`); vendor skill implements receiver. See the rule on forbidding vendor-specific references in generic skills |
| 8 | Add case-history meta OR ANY date stamp into a skill or rule body — case-history examples: "violation case", "verified YYYY-MM-DD", "Nth recurrence". Date stamp examples: `(HARD STOP -- added YYYY-MM-DD)`, `(HARD STOP -- newly added YYYY-MM-DD)`, `(recurrence-driven YYYY-MM-DD)`, "observed YYYY-MM-DD", "added in YYYY-MM-DD fix". Any literal `\d{4}-\d{2}-\d{2}` substring in new_string counts | Skill/rule body keeps Don't/Do + self-check + procedure only -- **no date stamps anywhere**, including section headers (`### X (HARD STOP -- added DATE)`), parenthetical annotations, code comments (`// observed DATE`), "added/newly added" footers, "since DATE" inline notes. Case history lives **only** in `~/.claude/skills/cleanup/data/failed-attempts.md` (HOT). If a case reference is essential, use a date-free pointer: `(see failed-attempts.md "<keyword>")`. **Self-check before every skill/rule Edit (MANDATORY, regex-strict)**: run `grep -E '[0-9]{4}-[0-9]{2}-[0-9]{2}' <<< "$new_string"` mentally -- 1+ match -> STRIP every match before calling Edit, then move case-history content (if any) into failed-attempts.md HOT as a separate write. Enforcement hook: `~/.claude/hooks/block-date-in-skill-rule.sh` (PreToolUse:Edit/Write on `skills/**/*.md` and `rules/**/*.md`) -- rejects calls whose new_string contains the date regex. Hook is the safety net; the self-check is the first line |

"Prompt" = any persistent text that influences Claude's behavior. Priority (check in order — **stop at the first match**):

| Priority | Target | Condition | Example |
|----------|--------|-----------|---------|
| **1st (default)** | **Memory** (`feedback` type) | All 1st-2nd-recurrence records, or context/reference info | new or updated `feedback_<topic>.md` |
| 2nd | **Skill** (`~/.claude/skills/`, `.claude/skills/`) | Skill procedure defect (missing/wrong step) | Fix procedure step missing |
| 3rd | **Rule** (`~/.agents/rules/`, `.claude/rules/`) | 3rd+ recurrence + 4-filter gate ALL pass | Add to existing rule section |
| 4th | **Sub-agent / CLAUDE.md** (`.claude/agents/*.md`, project root) | Policy bound to a specific context (agent/project) | Add to agent description / project CLAUDE.md |
| 5th | **Hook** (`settings.json` hooks) | 4th+ recurrence + deterministic pattern (grep/regex-judgeable) | Add PreToolUse/PostToolUse hook |

**Why Rule is not 1st**: a rule consumes always-on token cost continuously. Adding a rule for every mistake inflates the context until you can no longer follow the rules themselves — a paradox. memory (feedback) costs 0 tokens + is reachable via search — the natural medium for 1st-2nd-recurrence learning. Rules are reserved for permanent protection patterns that passed the 4-filter gate.

**Use Do & Don't table format (MANDATORY for 2+ recurrences)**:
When adding or strengthening rules, use the **Do & Don't table** instead of prose. Placing forbidden patterns (Don't) next to correct alternatives (Do) raises scan speed and compliance. For rules that have recurred 2+ times, switching to a table is required.

```markdown
| # | Don't | Do |
|---|-------|-----|
| 1 | {violation pattern} | {correct pattern} |
```

When fixing:
- **Skill is 1st priority** — if the problem is a skill's incomplete procedure, fix the skill. Don't skip to failed-attempts.md
- **If Why 3's conclusion is "missing procedure/rule"**: first look for an existing skill that owns that procedure. If a skill owns it, fix the skill → then the rule file
  - Example: "no move rule exists" → adding a move rule to the archive skill is the 1st priority; the rule-management rule is 2nd
- **If the fix skill's own procedural defect is the cause**: fix/SKILL.md is also a target — do not grant itself an exception
- Rule location must be confirmed via **AskUserQuestion**
- failed-attempts.md recording is **only for cases not covered by higher-priority targets** — no duplicate recording if root cause is already reflected in a skill or prompt
- **Profanity masking when recording to failed-attempts.md**: exclude or mask (`****`/`XX`) any user profanity/slurs in quoted text; preserve the anger context with a neutral term ("anger signal") instead of the raw word. Same rule as `cleanup/retrospect.md` Step 4-2 masking

**Escalation on recurrence** (4-stage progressive — minimize always-on context):

Minimize rule usage. **Default medium = memory (feedback)**. Edit a rule body only at the 3rd recurrence + after passing the 4-filter. Strengthening a rule on every fix causes always-on context inflation.

- **1st time**: **write a 1-3 line feedback memory** — new or update existing `~/.claude/projects/<project>/memory/feedback_<topic>.md`. No rule-file Edit. Record the case body separately in failed-attempts.md HOT.
- **2nd time**: **augment the feedback memory** — enrich the same memory entry with the case, trigger conditions, and How to apply. Add 2nd-time meta to failed-attempts.md HOT. Still no rule-file Edit.
- **3rd time**: **enter the 4-filter gate** — confirm all 4 filters pass:
  - pass → append 1-2 lines or a single Don't/Do row to an existing rule section (minimal). Grant the HARD STOP marker only for security/destructive/irreversible impact
  - any filter fails → re-route the medium (strengthen the skill procedure / CLAUDE.md / consider a hook design). No rule addition
- **4th time**: **if the pattern is deterministic, a hook is mandatory** (HARD STOP — implement it in this fix). script + chmod +x + install into `~/.claude/hooks/` + register in `settings.json` + `python3/jq` parse verification. Minimize the rule body to a hook pointer. For a non-deterministic pattern, redesign the skill procedure (no rule addition).
- **Recurrence after hook**: hook failed to block → strengthen the hook pattern + record in `failed-hooks.md` (not failed-attempts.md)

| Stage | Default medium | Rule-file action | Context impact | failed-attempts.md handling |
|-------|---------------|------------------|----------------|------------------------------|
| 1st | 1-3 line `feedback` memory | **forbidden** | 0 (memory is not always-on) | Register case body |
| 2nd | augment `feedback` memory | **forbidden** | 0 | Keep case body + 2nd-time meta |
| 3rd | 1-2 lines or a single row, only if the 4-filter passes | **conditionally allowed** | minimal or 0 | Keep case body + 3rd-time meta |
| 4th | hook implementation (deterministic patterns only) | hook pointer only | the hook enforces; minimize the rule body | HOT → archive |

**Forbidden patterns**:
- "At the 1st time, author a full Don't/Do table + HARD STOP + Scenarios" — context inflation
- "At the 3rd time, add a rule without the 4-filter check" — the 4-filter is the gate
- "At the 4th time, write only the hook spec and defer implementation" — hook spec + implementation are the same fix's Step 2 deliverable

## Don't / Do — no stage skipping

| # | Don't | Do |
|---|-------|-----|
| 1 | 1st time → author full Don't/Do table + Scenarios + HARD STOP as a new section (context inflation) | 1st time = 1-2 line prose or single row **inside an existing related section**. No new section. Defer the full table + section to the 2nd time |
| 2 | 2nd time → still only add 1-2 line prose to the same existing section (same as 1st time) | 2nd time = promote into a **standalone new section** + expand to Don't/Do table + self-check + Scenarios + HARD STOP |
| 3 | 4th time (hook registration) → write only spec and defer implementation | 4th time = actually author the script + install + register in settings.json + parse-verify (`python3 -c "import json"`). Mandatory |
| 4 | Ignore recurrence count → jump straight to hook design/implementation | Honor the stage sequence. 1st-3rd time = rule strengthening attempts; only at 4th time do you reach for a hook |
| 5 | 2nd time → just add another row to the 1st-time's appended line without restructuring | 2nd time = restructure: cut the 1st-time line from the existing section + paste as the kernel of the new standalone section, then expand |

## Stage decision procedure

1. In Step 1 recurrence pre-check (Stage 0 RAG + Stage 1 grep), identify the Nth recurrence count
2. Apply the stage matching N from the matrix above
3. 1st-3rd time = author rule file content (Don't/Do / Scenarios / hook design); 4th time = implement the hook

## Rule-file Edit gate (HARD STOP — AskUserQuestion mandatory)

**Before Edit/Write on any file under `~/.agents/rules/**`, `~/.claude/rules/**`, `<repo>/.claude/rules/**`, the fix flow MUST call AskUserQuestion to confirm: (a) which file to add to, (b) whether to add at all (memory/skill might be the better medium).** This applies even when fix Step 2 has decided rule strengthening is the chosen stage.

**Why**: `rule-management.md` (always_on) requires AskUserQuestion for any rule add/modify. fix's Step 2 routing decision (memory vs rule vs hook) selects the **medium category** but does not override the per-file `where to add` decision. Skipping the ask creates "/fix triggers rule rewrites without owner consent" — even sound rule additions accumulate without alignment.

**Skill files (`skills/**/*.md`) are NOT rule files** — direct Edit allowed (e.g., `step2-improvement.md` itself). The rule scope is strictly `rules/`, `.claude/rules/` directories.

### Don't / Do

| # | Don't | Do |
|---|-------|-----|
| 1 | "/fix Step 2 chose rule → directly Edit `branch-policy.md` (or other rule file)" | AskUserQuestion first: "Add to {existing file X} / {existing file Y} / {new file} / drop" → only after answer, Edit |
| 2 | Chain multiple rule additions in one fix run without ask | Each rule-file Edit is a separate ask. Even 2nd addition in the same fix needs its own ask |
| 3 | Treat rule-kit skill as optional convenience | `skill-usage.md` HARD STOP: rule file Edit goes through `rule-kit` skill. Call `Skill("rule-kit", "add")` (or `route`) **before** Edit |
| 4 | "Routing question was already implied by /fix scope" rationalization | /fix scope = "fix this behavior". Rule file location + content = separate decisions requiring explicit user input |
| 5 | Skip ask on minor rule additions ("only 1 line") | Line count is irrelevant. The rule's location and presence are user decisions |

### Self-check (every time before Edit/Write on rule file)

1. Is the target path `~/.agents/rules/*.md`, `~/.claude/rules/*.md`, or `<repo>/.claude/rules/*.md`?
2. If yes, did you call AskUserQuestion for (a) location and (b) presence?
3. Did you invoke `rule-kit` skill per `skill-usage.md` requirement?
4. Only after both → Edit. Otherwise STOP and ask first.

## Command / API / syntax primary-source verification (HARD STOP)

**When adding a CLI command / API call / config option / file path to a rule or skill body, verify each token against primary source (`--help`, `man`, official docs, source code) BEFORE Edit/Write.** Citing a flag/option/path from memory or analogy with sibling commands silently embeds wrong syntax — the rule body becomes a recurrence trap.

### Don't / Do

| # | Don't | Do |
|---|-------|-----|
| 1 | Cite `gh auth refresh -u <user>` by analogy with `gh auth switch -u` / `gh auth status -u` | Run `gh auth refresh --help` first; confirm each flag exists. Sibling-command flag presence ≠ this command's flag presence |
| 2 | Paste a `curl -X POST ...` example from training data without verifying the endpoint path / header shape against the provider's current API docs | Fetch the provider's API doc (or call the endpoint with `--head`) before pasting. APIs version-drift |
| 3 | "It worked in another project, so the syntax is fine" | Verify in **the destination project's CLI/API version**. flag/path drifts across versions and forks |
| 4 | Add a file path (`/etc/...`, `~/.config/...`) without confirming it exists on the target OS / version | `ls` / `command -v` / `find` to confirm. macOS/Linux/Windows paths differ |
| 5 | Quote a complex multi-line command (heredoc, pipeline) without dry-running once | Dry-run once (with `--dry-run` or `echo`) before placing it in a rule body. Syntax errors hidden in heredoc/quoting are silent |

### Self-check (every time before adding a command/API/syntax token to a rule/skill body)

1. List each CLI flag / option / API path / file path being added.
2. For each item, did I run `--help` / fetch docs / call the endpoint to verify it exists in the target version?
3. Where the rule cites a "sibling command" pattern (e.g., `gh auth switch -u` while documenting `gh auth refresh`), did I verify each command independently?
4. Did I dry-run multi-line commands or complex quoting?
5. If verification was skipped, the rule body is unverified — re-verify before Edit, or remove the token.

### Pointer

`(see failed-attempts.md "command syntax primary-source missing")` for case history.

### Pointer

See `~/.agents/rules/rule-management.md` (rule scope) + `~/.agents/rules/skill-usage.md` "Rule file Edit triggers rule-kit" + `(see failed-attempts.md "rule edit without ask in fix")` for details.
4. failed-attempts.md HOT entry only updates the Nth-time meta — do not re-author the case body redundantly

**Hook deferral forbidden (HARD STOP)**:

Writing only a hook **specification** ("hook X to be implemented on Nth recurrence") without the actual script + installation is a procedure violation at the 3rd recurrence. The spec must be **implemented in the same fix** (script file + chmod +x + settings.json registration). "Implement on next recurrence" defers indefinitely and the same mistake recurs.

| # | Don't | Do |
|---|-------|-----|
| 1 | "Hook spec to be implemented on Nth recurrence" deferral text in failed-attempts.md | 3rd recurrence = write hook script in this fix's Step 2 + install + register + verify with `jq` parsing settings.json |
| 2 | "Spec is done, implementation is the next fix's job" thinking at 3rd recurrence | Spec + implementation = same Step 2 deliverable. Splitting them = procedure violation |
| 3 | Skip the Checkpoint "Verify escalation artifacts" item | Step 2 Checkpoint #6 explicitly verifies "hook script file + settings.json registration" — missing = Step 2 incomplete |

(Case history: see failed-attempts.md "hook deferral".)

**`--plan` mode**:
- Emit only the list of target files + a preview of changes per file
- Do not perform Edit/Write (but **plan artifact .md saving is performed**)
- **Stop here after Step 2** — do not proceed to Step 3 or 4
- After reporting the plan, wait for user response. On "apply" approval, perform Edit/Write and proceed to Step 3

**Plan artifact .md saving (MANDATORY in `--plan` mode)** — applies the artifact-path rules:

| Environment detection | Save path | Filename |
|---------------------|-----------|----------|
| `{workspace}/.ralph/docs/generated/` exists | `.ralph/docs/generated/plan-fix-{slug}.md` | slug = key keyword (e.g., `consolidate-next-action`) |
| `{workspace}/.omc/plans/` exists (no Ralph) | `.omc/plans/plan-fix-{slug}.md` | same |
| Neither exists | Confirm path via AskUserQuestion | — |

**Chat output format** (after saving artifact):
```text
Plan saved: <absolute path>

Key summary:
- N target files
- Key changes ...

See the file above for details. Reply "apply" or with feedback.
```

Do not re-dump the entire plan body into chat — chat shows only path + 3-5 line summary.

| # | Don't | Do |
|---|-------|-----|
| 1 | Output --plan results only in chat and stop | Save .md to `.ralph/docs/generated/` or `.omc/plans/` and report the path |
| 2 | Save the artifact but also dump the full plan body in chat | Chat = path + 3-5 line summary only |
| 3 | Decide "it's just a draft, no need to save" | --plan = artifact. Always save |

**Checkpoint (MANDATORY before proceeding to Step 3; in `--plan` mode, only after approval):**
**Verify that the targets identified at every Why level (1~5) were actually modified before completing Step 2:**
0. **Was the Step 1.5 Action-plan table physically emitted in this fix's visible output?** If not, the planning step was skipped — emit it now (at "Target file : spot" granularity) before any further verification. Then confirm each Why row enumerates **all** spots, including multiple spots inside one file. A Why whose target file has N edit spots but only 1 table row = under-enumerated → re-list before proceeding. (Skipping 1.5 emission is the direct cause of "fixed the output template but missed the procedure/table/self-check" partial corrections.)
1. **Iterate over Why 1~5** and enumerate the target file paths each level identified (skills, rules, agents, etc.)
2. For each file, confirm that Edit/Write was performed in this Step 2
3. If any target was not modified, **do not advance to Step 3 — finish the modifications first**
4. **Do not pass on "existing rule not followed" alone without modifications** — if a rule existed but wasn't followed, strengthen its text to be more specific/explicit, or add examples / forbidden patterns. "Just naming the rule path" and moving on permits the same mistake to recur
5. **Do not check only Why 3 while omitting Why 1-2 targets** — if Why 2 says "X causes misunderstanding", X must be modified
6. **Verify escalation artifacts**: if this fix is the Nth recurrence, confirm the artifact for that count was actually produced in Step 2. 2nd time = hook design doc, **3rd time = hook script file + settings.json registration + parse-based verification**. Missing artifact = Step 2 incomplete.
   - **HARD STOP — "script file authored alone = done" is FALSE**: hook script + chmod +x + copy to `~/.claude/hooks/` + **`settings.json` PostToolUse/PreToolUse matcher registration + post-registration parse verification (`jq` or `python3 -c "import json"`) confirming actual registration** is the full Step 2 deliverable.
   - Mandatory verification command: `python3 -c "import json; d=json.load(open('~/.claude/settings.json')); ..."` to confirm the registered hook command is present in the matcher array. Skipping this = Step 2 incomplete.
   - **HARD STOP — authoring the script alone is not enough**: a hook is only "done" once it is registered AND the registration is parse-verified. Omitting settings.json registration silently disables the hook. (Case history: see failed-attempts.md "RAG store mandate".)
7. **Verify IaC constraints**: if the recovery or original work (Resume) touches infrastructure (Ansible, Terraform, docker compose) or server configuration, prove — before execution, by 1:1 comparison — that the design fully honors your infrastructure rules (e.g. no manual SSH operations on managed hosts, no direct operations on infra-tool-managed services).
