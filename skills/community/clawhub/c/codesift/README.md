# CodeSift

**Evidence-based code review for coding agents.**

CodeSift helps a coding agent uncover defects that survive a superficial review:
unreachable fast paths, broken contracts, redundant work, unused code, and checks
that appear to protect a system but do not affect its behavior.

It combines a reusable `SKILL.md` workflow, language-specific guidance, and small
evidence-collection helpers. The agent investigates the code, explains its
findings, proposes concrete changes, and waits for your approval before editing.

[Install](#install) · [Usage](#usage) · [FAQ](#faq) · [Measured results](#measured-results) ·
[Review contract](SKILL.md) · [License](#license) · [GitHub](https://github.com/zanw1/CodeSift)

## What CodeSift reviews

| Area | Questions it investigates |
|---|---|
| System behavior | Do callers, error handling, state transitions, and persistence agree across module boundaries? |
| Performance | Does the intended fast path run? Are storage reads, allocations, copies, locks, or recomputations repeated unnecessarily? |
| Dead and unused code | Can supported entry points reach this code? Is it an isolated cycle, test-only implementation, obsolete branch, or externally consumed API? |
| Ineffective gates | Can a check fail? Does failure reach a consumer that acts on it? Can empty tests, swallowed errors, or stale results appear successful? |
| Function design | Are responsibilities, return contracts, side effects, ownership, naming, and comments clear and consistent with the project? |
| Proportionality | Does each abstraction, dependency, fallback, and validation layer serve a concrete requirement? |
| Test and benchmark integrity | Do assertions come from independent contracts? Are workloads comparable, measurements real, and adverse results retained? |
| Concurrency and boundaries | Are races, lock order, retries and cancellation handled? Do both sides of an FFI, API, schema or configuration boundary agree? |
| Large and mixed repositories | Is every package reviewed as its own unit, ranked by risk, with a coverage ledger of what was and was not reviewed? |

CodeSift distinguishes **reproduced findings**, **statically established findings**,
and **hypotheses**. Impact severity is assessed separately from evidence strength.
An unused-symbol warning or a repeated code block is a candidate to investigate,
not automatic permission to delete or rewrite code.

## Review first, change after approval

1. **Investigate** the requested scope using source, contracts, call paths, and
   relevant checks.
2. **Explain** each actionable finding, its evidence, affected files, proposed
   correction, and validation plan.
3. **Wait for approval** of the presented plan or selected items.
4. **Implement** only the approved scope. Existing approval is not requested again;
   material additions are presented separately.
5. **Verify** the changes, report actual results and remaining limits, and clean
   temporary artifacts.

The workflow is defined in [SKILL.md](SKILL.md). Your agent remains responsible
for following it; execution permissions are controlled by the host environment.

## Measured results

Two anonymized case studies from private projects illustrate specific fixes found
through this review workflow. Their source, revision and evidence artifacts are not
public, so the numbers below cannot be independently reproduced. By the skill's own
case-study rule in [references/patterns.md](references/patterns.md), read them as
illustrations of the method, not as evidence about your code.

### Case A: redundant reads in a JSON-backed lookup

A conditional lookup loaded the same storage twice. Reusing the already loaded
snapshot removed duplicate deserialization while preserving the returned records.

| Metric, 10,000-document first-match workload | Before | After |
|---|---:|---:|
| Median latency per operation | 7.272 ms | **3.661 ms** |
| Storage reads per conditional operation | 2 | **1** |
| Peak traced Python allocation | 8,344,712 bytes | **4,685,686 bytes** |

That workload showed a **1.99x ratio of medians**, **49.66% lower latency**, and
**43.85% lower peak traced Python allocation**. The allocation measurement is a
separate `tracemalloc` probe, not process RSS.

Across 12 JSON-backed conditional-query cells, ratios of medians ranged from
**1.86x to 1.99x**. The functional suite passed **260 tests**, including 32 new
storage-boundary regression cases that failed before the fix.

### Case B: required persistence hidden inside assertions

Required metadata writes were evaluated inside assertions. Disabling assertions
removed the writes, so records that were readable before closing became
inaccessible after reopening. Moving the writes and their error checks into
unconditional execution restored the tested behavior.

| Correctness check | Before | After |
|---|---:|---:|
| Close/reopen cases with assertions disabled | 0/10 passed | **10/10 passed** |
| Close/reopen controls with assertions enabled | 10/10 passed | **10/10 passed** |
| Metadata I/O failure with assertions disabled | Returned normally | **Failure surfaced** |

The checks covered different record counts, block sizes, insertion orders, and
deletions. No speedup is claimed from comparing against a version that omitted
required persistence work.

### Measurement conditions and limits

- Five paired runs in fresh processes, alternating which version ran first.
- Two storage backends, three dataset sizes, five operations, three warmups, and
  seven measured batches per cell: **2,100 timed batches** in total.
- Before/after values are medians of five process-level medians. Each process
  median summarizes seven batches; batches are not independent machines.
- Setup, output validation, read-call tracing, and allocation tracing were
  excluded from latency measurement.
- Hardware: Apple M4, 32 GiB RAM; macOS 27.2; Python 3.11.9. Native checks used
  Apple Clang 21 with identical optimization settings apart from the assertion flag.
- JSON files were in a warm OS cache. No CPU pinning or cold-cache claim was made.

Unaffected ID lookups were approximately unchanged. In-memory results were mixed,
including small median regressions and timing outliers; these were retained in
the underlying experiment records. These selected, single-host cases demonstrate
particular fixes, not a universal speedup or superiority over other review methods.
They do not certify whole-project correctness or establish review-time savings.

## Install

CodeSift is distributed as a standalone skill folder. Clone it once, then expose it
to each agent through that agent's skill directory: Codex and Claude Code are shown
below; other compatible agents use their own documented directory.

### Requirements

- Codex or another agent that supports `SKILL.md` skills.
- Git for cloning this repository.
- Python 3.11+ on macOS, Linux, or Windows 10/11. Run the Python entry points
  directly from your terminal; Windows supports PowerShell 5.1 and 7 without
  WSL or Git Bash. Existing `.sh` wrappers remain available where Bash is installed.
  If the default interpreter is older, select a supported interpreter explicitly;
  the Bash wrappers also honor `CODESIFT_PYTHON=/path/to/python3.11`.
- The reviewed project's normal tools when needed: for example pytest, Cargo,
  npm, or CTest. Helpers do not install missing tools automatically.

### User-wide installation in Codex

```bash
mkdir -p "$HOME/.agents/skills"
git clone https://github.com/zanw1/CodeSift.git "$HOME/.agents/skills/codesift"
```

In Windows PowerShell:

```powershell
$CodeSiftPath = Join-Path $HOME '.agents\skills\codesift'
New-Item -ItemType Directory -Force (Split-Path $CodeSiftPath) | Out-Null
git clone https://github.com/zanw1/CodeSift.git $CodeSiftPath
```

The installed entry point should be:

```text
~/.agents/skills/codesift/SKILL.md
```

Codex discovers local skills in `~/.agents/skills` and repository
`.agents/skills` directories. It detects changes automatically; restart Codex if
the skill does not appear. See the [official skill documentation](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills).

### User-wide installation in Claude Code

Claude Code reads personal skills from `~/.claude/skills`. Link the clone above so
both agents share one copy:

```bash
mkdir -p "$HOME/.claude/skills"
ln -s "$HOME/.agents/skills/codesift" "$HOME/.claude/skills/codesift"
```

In Windows PowerShell, use a directory junction:

```powershell
$ClaudeSkillsPath = Join-Path $HOME '.claude\skills'
New-Item -ItemType Directory -Force $ClaudeSkillsPath | Out-Null
New-Item -ItemType Junction -Path (Join-Path $ClaudeSkillsPath 'codesift') -Target $CodeSiftPath
```

For a single repository, use `.claude/skills/codesift` inside that repository instead.

### Install for one repository

From a local CodeSift checkout, copy the skill package into the target project:

```bash
mkdir -p "/path/to/project/.agents/skills/codesift"
cp -R SKILL.md agents references scripts "/path/to/project/.agents/skills/codesift/"
```

In Windows PowerShell:

```powershell
$ProjectSkillPath = 'C:\path\to\project\.agents\skills\codesift'
New-Item -ItemType Directory -Force $ProjectSkillPath | Out-Null
Copy-Item -Path SKILL.md, agents, references, scripts -Destination $ProjectSkillPath -Recurse
```

Replace `/path/to/project` with your repository path. This copies the skill
resources without embedding a second Git repository. Use either a user-wide or
a project-local installation to avoid duplicate entries.

### Optional installation check

For the user-wide installation:

```bash
python3 -B "$HOME/.agents/skills/codesift/scripts/smoke_test.py"
```

In Windows PowerShell:

```powershell
py -3 -B (Join-Path $CodeSiftPath 'scripts\smoke_test.py')
```

The regression suite uses temporary fixtures and reports unavailable optional
integration tools as skipped. A skipped check is not a verified result. The
[cross-platform workflow](.github/workflows/cross-platform.yml) runs native
macOS/Linux/Windows tests and a separate PowerShell 5.1 check; inspect an actual
run before claiming those environments have passed for your revision.

## Usage

Open the project you want reviewed and mention the installed skill in Codex:

```text
$codesift Review this repository for systemic defects, redundant work,
unused code, and ineffective gates. List the evidence and proposed fixes
before changing any files.
```

For a smaller review:

```text
$codesift Review the changes on this branch. Trace affected callers and
contracts, and propose the smallest coherent fixes.
```

For a focused investigation:

```text
$codesift Investigate repeated storage reads on the lookup path.
Measure the relevant workload and explain a fix before implementing it.
```

After reviewing the findings, approve all or selected items:

```text
Approve R1 and R3. Implement those changes and run their validation plan.
```

For a large or mixed-language repository:

```text
$codesift Audit this monorepo. Split it into review units, rank them by risk,
and include a coverage ledger showing what was and was not reviewed.
```

You can also select a skill with `/skills` in Codex CLI or the IDE extension,
as described in the [official invocation guidance](https://learn.chatgpt.com/docs/build-skills#how-chatgpt-and-codex-use-skills).
In Claude Code, type `/codesift` followed by the same request, or describe the
task and let the agent load the skill from its description.

## FAQ

**Why does CodeSift stop before editing anything?**
Review and change are separate decisions. The agent presents findings with evidence
and a plan, and edits only after you approve the plan or selected items. A general
"review this" or "clean this up" does not approve a plan you have not seen.

**What do reproduced, confirmed_static and hypothesis mean?**
Reproduced: the behavior was observed with a recorded command and output.
Confirmed_static: the source establishes the trigger, path and consequence.
Hypothesis: a plausible candidate still waiting for that evidence. Hypotheses alone
never justify deleting code or blocking a merge. Severity is judged separately.

**The report found nothing. Is my code clean?**
Only within the reviewed scope. Check the coverage ledger: units and lenses marked
partial or skipped were not reviewed, and the limits section lists checks that did
not run.

**A helper exited 2 even though my tests pass. Why?**
Exit 2 means the evidence is incomplete, not that something failed: zero executed
tests, unrecognized output, a missing prerequisite or a timeout. Read status, reason
and failure_kind in the JSON report. An environment failure is not a defect.

**How do I run the helpers from PowerShell?**
Use their existing Python entry points; no `.ps1` launchers or execution-policy
changes are required. For example:

```powershell
py -3 -B (Join-Path $CodeSiftPath 'scripts\lib\source_checks.py') facts --root 'C:\my project' --output json
py -3 -B (Join-Path $CodeSiftPath 'scripts\lib\check_runner.py') correctness --root 'C:\my project' --lang python --json
```

For custom commands, prefer `--command-argv-file` (a UTF-8 JSON array) to preserve
empty arguments, quotes and backslashes across PowerShell versions. The original
`--command` remains a POSIX-token string on every OS. Explicit trusted shell mode
uses PowerShell on Windows and Bash on POSIX; arbitrary shell scripts must
propagate their own native-command failures. See [helper contracts](scripts/README.md).

**Registry checks are slow or fail from mainland China.**
Pass `--mirror cn` (TUNA for PyPI and crates, npmmirror for npm) or
`--registry-base URL`. A public mirror already configured for pip, npm or Cargo is
used automatically. A name missing only from a mirror is reported as
`mirror_not_found` and stays undetermined, because mirrors can lag. Use `--offline`
to skip network checks.

**How does it handle a large monorepo or several languages?**
`collect_facts.sh` lists every nested package as a review unit. The agent ranks units
by risk, picks a review depth from their size, reviews each through separate lenses,
and reports a coverage ledger instead of implying full coverage.

**Why are build, dist or vendor directories missing from the counts?**
They are excluded by default because they usually hold generated or third-party code.
The report lists every pruned directory; pass `--include-dir build` when one holds
code you want reviewed.

**My source files are GBK-encoded.**
Files that are not valid UTF-8 are decoded as GB18030 and listed under
`coverage.decoded_with_fallback`, so they are counted instead of skipped.

**Can CodeSift delete dead code for me?**
It reports unused-code candidates and confirmed unused code separately. Deletion
happens only as part of an approved plan, after reachability, external consumers and
build variants have been checked.

**Does any of my code leave the machine?**
Among the helpers, only verify_packages.py makes network requests, and it sends
package names, not code, unless you pass `--offline`. Test and benchmark helpers run
your project's own commands, which can do whatever the project does; the Cargo and
Go adapters start offline. The agent's model traffic is governed by the agent itself.

**Where can I see a complete report?**
[references/report-example.md](references/report-example.md) shows a full sample with
every evidence state, a gate table, a coverage ledger and an optional JSON form.

**How is the review itself tested?**
`scripts/smoke_test.py` tests the helpers. The cases in `evals/` (a seeded single
defect, a multi-defect recall set, a mixed-language boundary case and a clean
control) test whether a review finds the seeded problems without inventing new ones.
With Claude Code they run as `claude plugin eval . --allow-tools Write,Edit,Bash
--scaffold`; these are billed model runs.

## Package contents

| Path | Purpose |
|---|---|
| [SKILL.md](SKILL.md) | Review workflow, approval boundary, evidence rules, and finding format |
| [agents/openai.yaml](agents/openai.yaml) | CodeSift display metadata and default invocation prompt |
| [references/patterns.md](references/patterns.md) | Cross-language standards, dead-code analysis, redundancy, gate effectiveness, cross-boundary contracts, and candidate generators |
| [references/report-example.md](references/report-example.md) | Complete sample report, optional JSON findings, and SARIF export notes |
| [references/polyglot.md](references/polyglot.md) | Go, JVM, shell, SQL migration, infrastructure-as-code, and CI guidance |
| `references/` | Focused C, C++, Rust, Python, JavaScript/TypeScript, and storage-system guidance |
| [scripts/README.md](scripts/README.md) | Helper commands, prerequisites, result states, and evidence limits |
| `scripts/` | Project facts, duplicate-block candidates, dependency checks, test and benchmark runners |
| `evals/` | Behavior test cases for the review itself, in the `claude plugin eval` layout |

The review guidance is language-aware. Structural tools such as code-graph MCPs,
language servers and SCIP indexes can strengthen call-path analysis when available; direct source inspection remains necessary
for coverage gaps and dynamic behavior. Bundled helpers provide observations,
while the review connects them to the project's actual requirements.

## License

CodeSift is released under the [MIT License](LICENSE).

