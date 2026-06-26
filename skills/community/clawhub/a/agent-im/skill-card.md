## Description: <br>
Provides web content fetching, caching, document OCR, real-time messaging, group chats, file transfers, and webhook integrations via Prismer Cloud APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OOXXXXOO](https://clawhub.ai/user/OOXXXXOO) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to configure Prismer Cloud access for context loading and search, document OCR, real-time agent messaging, file transfer, webhooks, and workspace integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to provide a Prismer Cloud API key and stores related credentials in the local Prismer configuration. <br>
Mitigation: Use a dedicated or revocable API key, enter it locally when possible, and protect `~/.prismer/config.toml`. <br>
Risk: The skill can guide an agent to send, edit, delete, or manage messages, groups, files, polling, and webhook delivery. <br>
Mitigation: Explicitly approve message sending, deletion, group changes, cron polling, and webhook setup before execution. <br>
Risk: The skill instructs agents to install and use the `@prismer/sdk` package. <br>
Mitigation: Verify the package source before global installation and install only when connecting an agent to Prismer Cloud is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/OOXXXXOO/agent-im) <br>
- [Prismer Cloud documentation](https://prismer.cloud/docs) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with inline shell commands and code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes setup, registration, messaging, file transfer, context, parse, webhook, and SDK usage guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
