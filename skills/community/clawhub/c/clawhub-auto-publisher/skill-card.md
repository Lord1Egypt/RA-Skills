## Description:

Automatically package and publish local skills to ClawHub marketplace with pricing optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sasamittrrr](https://clawhub.ai/user/sasamittrrr)

### License/Terms of Use:


## Use Case:

Developers and skill publishers use this skill to scan local skill directories, preview readiness, suggest pricing, and prepare ClawHub marketplace publishing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is intended for marketplace publishing and may expose local skill content if a future version enables upload behavior.

Mitigation: Run dry-run mode first and set CLAWHUB_API_KEY only when intentionally publishing.

Risk: Pricing and marketplace metadata suggestions are heuristic and may be unsuitable for a release.

Mitigation: Review suggested prices, descriptions, keywords, version changes, and changelog text before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sasamittrrr/skills/clawhub-auto-publisher)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and Python code references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference CLAWHUB_API_KEY and dry-run or publish CLI options.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
