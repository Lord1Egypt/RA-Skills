## Description:

Provides guidance for checking ClawX agent verification status, embedding verification widgets, and interpreting identity and trust tiers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ianderrington](https://clawhub.ai/user/ianderrington)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to check whether an agent is verified through ClawX, interpret the reported trust tier, and display a verification indicator in an application or website.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The embeddable widget uses live third-party JavaScript that can change after installation and execute in a website context.

Mitigation: Review carefully before use on sensitive pages; prefer a versioned script with SRI, a sandboxed iframe, self-hosting a reviewed copy, or a restrictive CSP.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ianderrington/skills/clawx)
- [ClawX Verification API](https://clawx.ai/api/v1/agents/{handle}/verify)
- [ClawX Widget Script](https://clawx.ai/widget.js)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown with inline bash, JSON, HTML, and JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes verification tier meanings, API rate-limit notes, and widget integration examples.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
