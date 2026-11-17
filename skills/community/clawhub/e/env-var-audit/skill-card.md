## Description:

Audits source code for environment variables missing from example files and potential hardcoded secrets, with text or JSON findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill during local development or CI checks to find undocumented environment variables and possible hardcoded credentials before merging or deploying code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Downloading a mutable script directly into a persistent agent skills directory could introduce unreviewed changes.

Mitigation: Install the reviewed release artifact when possible; otherwise pin the download to a commit and verify the file before use.

Risk: Scanning unintended directories or sharing scan reports may expose sensitive project details.

Mitigation: Scan only intended project directories and limit access to terminal and JSON output.

Risk: Heuristic scanning may misidentify examples or miss credentials.

Mitigation: Review findings and important security decisions manually rather than treating a clean scan as a guarantee.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zhaoxinghua09-cell/skills/env-var-audit)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Plain text or JSON audit findings with suggested fixes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports source locations, undocumented variables and potential secrets; scan results require human review.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; bundled documentation says 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
