## Description:

Helps identify dangerous capability combinations that emerge when agent skills are composed, including cases where individually benign skills combine into exfiltration or compromise paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andyxinweiminicloud](https://clawhub.ai/user/andyxinweiminicloud)

### License/Terms of Use:


## Use Case:

Developers, security reviewers, and agent operators use this skill to analyze composed skill sets for dangerous capability pairs, emergent effective capabilities, permission declaration gaps, and inheritance amplification risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The analysis may produce conservative risk assessments for skill combinations that are isolated by external controls.

Mitigation: Review findings against the agent's actual runtime isolation, permission boundaries, and network policy before making deployment decisions.

Risk: The current Markdown-only artifact declares curl and python3 binary requirements that are not clearly needed.

Mitigation: Confirm whether those binaries are necessary before granting runtime access to them.

## Reference(s):

- [Capability Composition Analyzer on ClawHub](https://clawhub.ai/andyxinweiminicloud/skills/capability-composition-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown risk report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports dangerous pair inventory, emergent capability surface, inheritance amplification, permission declaration gaps, and a composition risk level.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
