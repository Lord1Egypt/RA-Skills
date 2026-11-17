## Description:

Fail-safe policy gate for OpenClaw marketplace skills that intercepts tool calls before execution and checks them against an Authensor policy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[authensor](https://clawhub.ai/user/authensor)

### License/Terms of Use:

MIT

## Use Case:

Developers and teams use this skill to route OpenClaw tool activity through a policy gateway so low-risk actions can proceed, high-risk actions can require approval, and dangerous actions can be blocked. It is most relevant for teams running marketplace skills, needing audit receipts, or working under compliance expectations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill routes session-wide tool activity decisions through an external service and sends redacted action metadata outside the workspace.

Mitigation: Use only a trusted HTTPS control-plane URL, scope the Authensor API key narrowly, and avoid highly sensitive repositories unless sharing redacted action metadata is acceptable.

Risk: An Authensor allow decision could be mistaken for complete execution safety.

Mitigation: Keep host sandboxing and platform safety controls enabled, and review high-risk actions before approval.

## Reference(s):

- [Authensor Gateway ClawHub listing](https://clawhub.ai/authensor/skills/authensor-gateway)
- [Authensor for OpenClaw homepage](https://github.com/AUTHENSOR/Authensor-for-OpenClaw)
- [ClawHub marketplace metadata listing](https://www.clawhub.ai/AUTHENSOR/authensor-gateway)
- [ClawHavoc marketplace skill security article](https://snyk.io/blog/clawhavoc)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Shell commands]

**Output Format:** [Markdown instructions with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CONTROL_PLANE_URL and AUTHENSOR_API_KEY environment variables.]

## Skill Version(s):

0.7.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
