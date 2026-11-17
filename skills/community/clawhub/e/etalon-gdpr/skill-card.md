## Description:

Full GDPR compliance audit for any website or codebase using the ETALON CLI; it scans for trackers, tests consent violations, checks privacy policy alignment, maps PII data flows, and returns structured reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rednix](https://clawhub.ai/user/rednix)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, privacy engineers, and compliance teams use this skill to run ETALON CLI website or codebase audits, review GDPR consent and tracker findings, and generate concise remediation guidance or privacy policy output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installation command does not pin a reviewed etalon-cli version.

Mitigation: Verify the ETALON package and publisher before installation, and prefer a pinned reviewed version when available.

Risk: Codebase audits may read local configuration files and surface secrets, API keys, or connection strings in audit output.

Mitigation: Run audits in a clean workspace without unnecessary secrets and do not forward raw findings or config contents to external tools without explicit user approval.

Risk: The skill can propose automatic fixes through ETALON CLI behavior.

Mitigation: Review any generated or fixed changes in version control before keeping them.

## Reference(s):

- [ETALON homepage](https://etalon.nma.vc)
- [ClawHub skill page](https://clawhub.ai/rednix/skills/etalon-gdpr)

## Skill Output:

**Output Type(s):** [analysis, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with JSON-derived findings, inline shell commands, and optional generated Markdown policy content.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the local etalon CLI; codebase audits may expose sensitive local configuration or secret-like values in outputs.]

## Skill Version(s):

0.9.6 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
