## Description:

Clawhub Gate provides a ClawHub release helper that runs local shell and Python static analysis, invokes ClawHub sync, and polls ClawScan results for a skill release.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freepengyang](https://clawhub.ai/user/freepengyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill publishers use this skill to run local shell/Python static checks and ClawScan polling during ClawHub release workflows. Manual review is needed before relying on it as a release gate because server security evidence reports release-order and polling risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script can publish or update a skill before the promised security gate completes.

Mitigation: Review and fix the sync order and rollback behavior before using it as a pre-publish blocker.

Risk: The polling path has a code-injection flaw.

Mitigation: Patch slug handling so untrusted values are passed as data rather than embedded in inline code, then re-scan before use.

Risk: `--local-only` should not be relied on to avoid network access or publication.

Mitigation: Use an isolated test skill or a reviewed local-only path until the control flow is corrected.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/freepengyang/skills/clawhub-gate)
- [clawhub_gate.sh](artifact/references/clawhub_gate.sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash commands and terminal status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires shellcheck, bandit, jq, python3, the clawhub CLI, and a local ClawHub config token.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
