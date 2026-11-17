## Description:

Scan a third-party agent skill with ClawVet and act on its grade before installing, enabling, or running it. Use when the user asks to scan, vet, or check a skill they did not write, or whether a skill from ClawHub or another untrusted source is safe to install.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohibshaikh](https://clawhub.ai/user/mohibshaikh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this agent skill to scan third-party agent skills and review scan coverage, findings, and recommendations before deciding whether to install, enable, or run them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scan evidence is incomplete; the unpinned package reference and unresolved local references leave uncertainty.

Mitigation: Resolve the local references and use an installed ClawVet for a complete local scan before relying on the grade for an installation decision.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations depend on the scan status, coverage, findings, and grade.]

## Skill Version(s):

1.0.6 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
