## Description:

Picoclaw-only local posture-review skill focused on read-only findings and safe operator remediation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davida-ps](https://clawhub.ai/user/davida-ps)

### License/Terms of Use:

AGPL-3.0-or-later

## Use Case:

Developers and security operators use this skill to review an existing Picoclaw posture profile for local exposure, authentication, workspace, MCP, scheduler, secrets, and multi-channel access findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A floating npx installation command can retrieve an unexpected installer or release state.

Mitigation: Prefer the signed release verification instructions or a pinned, reviewed installer version before installation.

Risk: The tool reads a user-provided Picoclaw posture profile and prints security findings that may describe local exposure or configuration weaknesses.

Mitigation: Run it locally on intended profile files only and handle generated findings as sensitive operational information.

Risk: Findings and recommendations are review guidance, not automatic remediation.

Mitigation: Require operator review before applying configuration changes or security remediations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/davida-ps/skills/clawsec-picoclaw-self-pen-testing)
- [ClawSec homepage](https://clawsec.prompt.security)

## Skill Output:

**Output Type(s):** [analysis, json, guidance]

**Output Format:** [JSON containing severity-ranked findings, evidence strings, recommendations, and summary counts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on a user-provided Picoclaw posture profile and performs read-only analysis.]

## Skill Version(s):

0.0.5 (source: frontmatter, skill.json, CHANGELOG, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
