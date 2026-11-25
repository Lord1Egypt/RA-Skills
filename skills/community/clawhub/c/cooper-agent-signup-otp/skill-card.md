## Description:

Sign up for a website or service as the agent and finish email verification using a Cooper Email inbox to receive the one-time code or confirmation link.

This skill is ready for commercial/non-commercial use.

## Publisher:

[f-o-x11](https://clawhub.ai/user/f-o-x11)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill when a user asks them to create or log into an account and complete email verification with a Cooper Email inbox. It retrieves a one-time code or confirmation link while following the service's terms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is incomplete and identifies low-confidence concerns about external transmission and unresolved skill references, especially relevant before sharing an API key.

Mitigation: Review the unresolved references and data destinations before installation; store COOPER_API_KEY securely, never print or log it, and only use this flow for services the user requested.

## Reference(s):

- [Cooper Email documentation index](https://cooperemail.com/llms.txt)
- [Cooper Email CLI skill](https://cooperemail.com/skills/cooper-email-cli/SKILL.md)
- [Cooper Email MCP server](https://cooperemail.com/mcp)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, Configuration instructions]

**Output Format:** [Markdown instructions with inline shell commands, API examples, and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses COOPER_API_KEY when configured; keep credentials and received codes private.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
