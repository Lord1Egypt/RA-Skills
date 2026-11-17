## Description:

Multi-agent deep review for code PRs in any repo, orchestrating Copilot and parallel subagents for adversarial, operational, and reference-comparison review with scope-based escalation, stale-finding triage, and a hard iteration cap.

This skill is ready for commercial/non-commercial use.

## Publisher:

[conorbronsdon](https://clawhub.ai/user/conorbronsdon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to run a structured PR review workflow that sizes a change, combines GitHub Copilot with focused subagent review angles, triages findings, and limits repeated review rounds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read PR diffs and repository context while coordinating GitHub Copilot and subagent reviews.

Mitigation: Invoke it deliberately for PR review tasks and review prompts before approving pushes or issue creation.

Risk: The workflow can push fixes or create GitHub issues as part of triage.

Mitigation: Require user confirmation before the first push of the session or before creating an issue.

Risk: Copilot may repeat stale findings against code that has already been fixed.

Mitigation: Read the file at HEAD before re-fixing and stop after the documented two Copilot review rounds.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/conorbronsdon/skills/cot-code-review)
- [README](artifact/README.md)
- [Skill workflow](artifact/SKILL.md)
- [Subagent prompt templates](artifact/patterns/subagent-prompts.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and review findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke GitHub CLI, GitHub Copilot review, and subagent review lanes when available; prompt templates cap each subagent report at about 500 words.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
