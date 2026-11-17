## Description:

Run an Asyntai AI customer support agent (website chatbot) from OpenClaw through the Asyntai MCP server - add knowledge, crawl a site, edit the agent's instructions, change the widget look, read conversations, leads and analytics, find topics that need more knowledge, and reply live to website visitors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asyntai](https://clawhub.ai/user/asyntai)

### License/Terms of Use:

MIT-0

## Use Case:

Website operators and customer support teams use this agent skill to connect OpenClaw to Asyntai and manage chatbot knowledge, behavior, appearance, conversations, leads, and analytics. It also guides setup and requires user approval for sensitive changes and live replies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Changes to website knowledge, support instructions, widget settings, or live conversations can affect customer-facing service.

Mitigation: Select the intended website, read current settings or knowledge before changing them, and get user approval before deletions, configuration changes, or live replies; show proposed instructions before saving.

Risk: Account credentials could be exposed during setup.

Mitigation: Use the browser-based OAuth sign-in flow and never ask for the user's Asyntai password.

## Reference(s):

- [Asyntai MCP documentation](https://asyntai.com/documentation/mcp/)
- [Asyntai](https://asyntai.com)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, API calls]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance for MCP tool use and account setup; actions that change a website or reply to a live visitor require user approval.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
