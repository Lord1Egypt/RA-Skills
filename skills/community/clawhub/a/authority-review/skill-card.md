## Description:

Reviews entity clarity, independent references, author credibility, and reputation signals to assess site authority without collapsing it into an unsupported score.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trustgrowth](https://clawhub.ai/user/trustgrowth)

### License/Terms of Use:

MIT-0

## Use Case:

External site owners, SEO practitioners, and content teams use this skill to understand whether a site has clear authority signals from independent references, credible authorship, first-party proof, and comparable peer evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to execute an unbundled groundcrew-doctor.py validator from an ambiguous skills root.

Mitigation: Install only in environments where the Groundcrew skills root is trusted, verify the validator path and hash before execution, and prefer a release that bundles or pins the validator.

Risk: SEO and analytics connectors may expose site or account data if configured with broad permissions.

Mitigation: Use read-only connector credentials where possible and only connect accounts already controlled by the user or organization.

## Reference(s):

- [Connectors and categories](references/connectors.md)
- [Reporting contract](references/reporting.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown guidance with evidence requirements and occasional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend at most one missing connector and should label unknowns rather than estimate missing authority metrics.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
