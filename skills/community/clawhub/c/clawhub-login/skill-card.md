## Description:

Helps agents guide ClawHub login on headless servers by generating an OAuth authorization URL, checking login status, and supporting local logout.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mengwuzhi](https://clawhub.ai/user/mengwuzhi)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators working on headless servers use this skill to authenticate the ClawHub CLI when browser-based login is unavailable. Agents can use it to provide the user with commands and step-by-step login guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authorization URLs, callback URLs, and tokens may grant account access if exposed.

Mitigation: Treat URLs and tokens as sensitive, avoid sharing terminal output publicly, and clear saved tokens when access should be revoked.

Risk: Callback automation is described in the artifact but appears incomplete in the security guidance.

Mitigation: Use the generated authorization URL and login-status check as the reliable workflow, and verify the final login state before publishing or accessing ClawHub resources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mengwuzhi/skills/clawhub-login)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and plain-text status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include OAuth authorization or callback URLs that should be treated as sensitive.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
