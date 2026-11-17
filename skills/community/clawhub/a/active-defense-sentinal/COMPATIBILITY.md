# OpenClaw compatibility review

Reviewed OpenClaw main at `31157a19b41dae0ec28a4010d08656d11f55c067`
(September 17, 2026 in America/New_York).

## Source contracts

- `docs/cli/health.md`: `health --json --timeout <ms>`; top-level `ok` indicates
  RPC success, not overall channel or host health.
- `src/config/state-dir.ts` and `src/cli/profile-utils.ts`: home/state overrides,
  isolated named profiles, validated profile names, legacy state fallback.
- `src/agents/workspace-default-path.ts`: workspace override and profile/state
  workspace defaults.
- `docs/tools/skills.md` and `src/cli/skills-cli.format.ts`: managed skills are
  only one source; `skills list --json` lacks file paths, while `skills info`
  exposes file-backed skill details. No claim of whole-catalog coverage is made.

Upstream source: https://github.com/openclaw/openclaw/tree/31157a19b41dae0ec28a4010d08656d11f55c067

The Cisco MarkdownReporter contract was reviewed at blob
`50255ff4fc6eeee13b29d46f4a7e1fbd619a4954`
(`skill_scanner/core/reporters/markdown_reporter.py`). Single and bulk summaries
include explicit counts for Critical, High, Medium, Low, and Info. Duplicate or
incomplete summaries are unknown, never automatically clean.

## Validation and limits

Offline Python regression tests exercise state paths, report verdicts, blocked
installs, staging layouts, report freshness, destination boundaries, and the
Gateway/browser CLI split. Mocks do not establish live runtime compatibility.
No real OpenClaw, Cisco scanner, ClawHub, or Hermes deployment was executed.
No user clone was inspected or presumed clean. Native OpenClaw lifecycle calls
are not intercepted, scan/copy concurrency is not secured by immutable snapshots,
and a successful health RPC is not an integrity attestation.

`--force` remains replacement-only in Sentinal and never bypasses scan failures.
The separate Bash scanner repository has a different explicit findings override;
it also refuses scanner-error or unknown-report overrides.

Before pushing, main was rechecked at
`57034eb5e70b33bcf1e11ba782693d0d0889bb83`. The intervening seven commits
were compared; none changes the reviewed path, skills CLI, or health contracts.
