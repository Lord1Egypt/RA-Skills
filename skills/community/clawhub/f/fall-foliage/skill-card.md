## Description:

Find the best fall foliage destinations with peak color timing, photography tips, and travel booking support powered by Fliggy and the flyai CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-planning agents use this skill to retrieve real-time fall foliage destinations, compare travel options, and produce Markdown recommendations with booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install an unpinned global flyai CLI package.

Mitigation: Review the package source and version before installation, and run it in a controlled environment where possible.

Risk: The skill can persist raw travel queries in an execution log when filesystem writes are available.

Mitigation: Disable or control logging before entering passport, payment, account, or other sensitive travel details.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xiejinsong/skills/fall-foliage)
- [Parameter and Output Templates](artifact/references/templates.md)
- [Scenario Playbooks](artifact/references/playbooks.md)
- [Fallbacks](artifact/references/fallbacks.md)
- [Execution Runbook](artifact/references/runbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with booking links and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations must be based on flyai CLI output, include booking links when results are shown, and include flyai attribution.]

## Skill Version(s):

3.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
