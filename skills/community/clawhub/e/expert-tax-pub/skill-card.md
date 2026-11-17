## Description:

税务申报与筹划专家 routes pasted tax or document tables to one of 32 local checking engines and returns line-referenced, reproducible conclusions or missing-column feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, tax, and operations users working with China-focused tax and business-document tables use this skill to route a pasted table to the relevant local checker, receive row-level findings, and see which required columns or parameters are missing.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Users may treat deterministic tax and document consistency checks as professional tax advice.

Mitigation: Present results as review aids and require qualified tax or finance review before filing, payment, or compliance decisions.

Risk: The skill processes business or tax tables locally, which may contain sensitive information.

Mitigation: Run it only on trusted local systems and avoid providing sensitive tables unless local processing is acceptable for the organization.

Risk: A local trial-use counter is recorded in the user's home directory.

Mitigation: Disclose the local counter behavior to users and manage it according to local privacy and retention expectations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/expert-tax-pub)
- [Publisher profile](https://clawhub.ai/user/chenqg618)
- [Artifact skill definition](artifact/SKILL.md)
- [Expert manifest](artifact/scripts/engine/expert-manifest.json)
- [Local runner](artifact/scripts/run.mjs)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Plain text or JSON with routed sub-skill results, row-level findings, missing-input notices, and unexecuted-check notices]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally through Node.js; results are deterministic consistency checks and not professional tax advice.]

## Skill Version(s):

1.0.10 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
