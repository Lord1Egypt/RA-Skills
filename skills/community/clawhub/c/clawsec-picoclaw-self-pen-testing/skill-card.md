## Description: <br>
Picoclaw-only local posture-review skill focused on read-only findings and safe operator remediation guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davida-ps](https://clawhub.ai/user/davida-ps) <br>

### License/Terms of Use: <br>
AGPL-3.0-or-later <br>


## Use Case: <br>
Developers and operators use this skill to review a generated Picoclaw posture profile for local security findings such as public UI exposure, disabled authentication, unrestricted tooling, unsigned mode, MCP trust boundaries, scheduler persistence, plaintext secret markers, and multi-channel auth review needs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Picoclaw posture profile and the generated findings may reveal sensitive local security posture. <br>
Mitigation: Store and share profiles and findings as security-sensitive data, and redact them before broader distribution. <br>
Risk: The release is published by a third party. <br>
Mitigation: Install only when the publisher is trusted and the user intends to analyze a Picoclaw posture profile. <br>


## Reference(s): <br>
- [ClawSec homepage](https://clawsec.prompt.security) <br>
- [ClawHub skill page](https://clawhub.ai/davida-ps/skills/clawsec-picoclaw-self-pen-testing) <br>


## Skill Output: <br>
**Output Type(s):** [json, guidance] <br>
**Output Format:** [JSON with severity-ranked findings, summary counts, evidence strings, and remediation recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally against an explicit Picoclaw profile path and prints deterministic JSON.] <br>

## Skill Version(s): <br>
0.0.5 (source: frontmatter, skill.json, changelog, release evidence; released 2026-06-23) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
