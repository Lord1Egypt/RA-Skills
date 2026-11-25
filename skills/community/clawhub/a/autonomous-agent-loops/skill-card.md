## Description:

Autonomous Loops provides agent loop patterns for sequential pipelines, persistent REPL sessions, parallel spec-driven generation, PR automation, cleanup passes, and RFC-driven DAG orchestration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[djc00p](https://clawhub.ai/user/djc00p)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to choose and operate autonomous coding-agent loop patterns for repository automation, with consent, dry-run, isolation, budget, and human-review controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended repository automation can create branches, open pull requests, retry CI failures, or merge code on the wrong target.

Mitigation: Use only on repositories you own or administer, obtain explicit consent, start in dry-run or no-commit mode, avoid production branches, and require human review for merges.

Risk: Specs, diffs, logs, session files, and directory listings can expose secrets, customer data, internal paths, or proprietary code structure.

Mitigation: Redact sensitive inputs before passing them to an agent, keep session and notes files out of git, use least-privileged credentials, and rotate credentials after a run.

Risk: Long-running loops can waste budget or repeat failing actions without useful progress.

Mitigation: Set hard run, cost, duration, and CI retry limits; emit loop heartbeats; stop and alert a human when retry limits are reached.

## Reference(s):

- [Security Checklist](references/security-checklist.md)
- [Sequential Pipeline](references/sequential-pipeline.md)
- [Persistent REPL](references/persistent-repl.md)
- [Parallel Agents](references/parallel-agents.md)
- [PR Automation Loop](references/pr-automation.md)
- [De-Sloppify Pattern](references/de-sloppify.md)
- [DAG Orchestration](references/dag-orchestration.md)
- [ClawHub Skill Page](https://clawhub.ai/djc00p/skills/autonomous-loops)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with shell command examples, checklists, and decision matrices]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires gh, git, and node for applicable workflows; may use CLAW_SESSION and CLAW_SKILLS environment variables.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
