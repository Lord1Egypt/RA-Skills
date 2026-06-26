## Description: <br>
Free email for AI agents. No sign-up needed. One call to get a mailbox and send. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agents-mail](https://clawhub.ai/user/agents-mail) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to give an AI agent an email mailbox, send messages, check inboxes, and configure notification or reply workflows through the Agents Mail REST API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent sends and receives email through a third-party service. <br>
Mitigation: Use the skill only when the operator is comfortable with agentsmail.org handling the mailbox, and avoid sensitive mail unless the service is trusted for that use. <br>
Risk: The returned API key grants mailbox access and may be exposed in logs, chat transcripts, or source control. <br>
Mitigation: Store the API key in an environment variable or secret store, and avoid pasting it into chat logs or committing it to files. <br>
Risk: Heartbeat polling, webhooks, and auto-replies can cause the agent to read, summarize, or send email automatically. <br>
Mitigation: Enable automation only with explicit limits on what the agent may read, summarize, and send. <br>


## Reference(s): <br>
- [Agents Mail homepage](https://agentsmail.org) <br>
- [Agents Mail ClawHub listing](https://clawhub.ai/agents-mail/agents-mail) <br>
- [API Reference](references/API.md) <br>
- [Common Patterns](references/EXAMPLES.md) <br>
- [API Help](https://agentsmail.org/api/help) <br>
- [Agents Mail docs](https://agentsmail.org/docs) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with REST API examples, bash commands, and Python code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent-facing instructions for creating and using an Agents Mail mailbox; API responses are JSON.] <br>

## Skill Version(s): <br>
0.4.4 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
