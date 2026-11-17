## Description:

Search Cruit for AI-native developers and reach out to them with explicit confirmation before any credit-spending reveal or message.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nwang783](https://clawhub.ai/user/nwang783)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiters and hiring teams use this skill from a coding agent to connect Cruit, describe a hiring need, review search filters, inspect low-PII candidate cards, and approve candidate reveal or outreach actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote installer code and fetched skill instructions can change after review.

Mitigation: Prefer marketplace-native installation or a downloaded, reviewed, version-pinned package; trust only the documented cruit.dev instruction URL.

Risk: Local credentials stored at ~/.cruit/credentials.json can grant access to the recruiter's account if exposed.

Mitigation: Keep credentials in user-only files, never paste tokens into chat, and rotate or revoke credentials if exposure is suspected.

Risk: Candidate reveal and direct-message actions can spend contact credits and expose personal contact information.

Mitigation: Require explicit recruiter approval before each reveal or send action, show the exact message text before sending, and avoid batch reveal or batch messaging.

## Reference(s):

- [Cruit Recruiter canonical instructions](https://cruit.dev/skills/recruiter/INSTRUCTIONS.md)
- [Cruit website](https://cruit.dev)
- [ClawHub skill page](https://clawhub.ai/nwang783/skills/cruit-recruiter)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with concise recruiter workflow prompts, candidate summaries, approval requests, and JSON setup state when configuration is saved.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit recruiter approval before revealing contact information, spending contact credits, or sending candidate messages.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
