## Description:

CloakClaw redacts sensitive entities from documents or pasted text before cloud LLM use, then restores originals in the model response.

This skill is ready for commercial/non-commercial use.

## Publisher:

[canonflip-git](https://clawhub.ai/user/canonflip-git)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI users use this skill to cloak sensitive documents or pasted text before sending content to cloud LLMs and to decloak model responses afterward.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags broad automatic handling of sensitive documents by a globally installed external executable.

Mitigation: Use explicit opt-in, verify and pin the installed cloakclaw version, and consider disabling network access while processing sensitive files.

Risk: Reversible local mappings may retain original sensitive values beyond the immediate model interaction.

Mitigation: Review the external tool's storage behavior, enable password protection where appropriate, and purge sessions after use.

Risk: The artifact states that CloakClaw is not HIPAA, GDPR, SOC 2, PCI-DSS, or CCPA compliant.

Mitigation: Do not rely on this skill for regulated or highly confidential data without independent compliance and security review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/canonflip-git/skills/cloakclaw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces reversible cloaked and decloaked text through a locally invoked CLI; session mappings are retained by the external tool until expiry.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
