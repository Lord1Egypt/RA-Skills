## Description: <br>
Manage ClickUp tasks, lists, spaces, folders, comments, goals, and workspace data via the ClickUp API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to manage ClickUp project work from chat, including task, list, space, folder, comment, goal, view, template, tag, dependency, custom field, and chat-message workflows. The skill is suited to ClickUp workspace automation where ClawLink provides the hosted connection flow and authenticated tool access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires connection to a ClickUp account and can operate within that account's workspace permissions. <br>
Mitigation: Install only when the user is comfortable granting ClawLink access to the connected ClickUp workspace, and rely on the connected account's permissions to scope access. <br>
Risk: Create, update, delete, and bulk operations can change or remove ClickUp workspace data. <br>
Mitigation: Use discovery and preview steps before writes, confirm the target resource and intended effect with the user, and execute only after explicit approval. <br>
Risk: The available ClickUp tool catalog includes chat-message and direct-message channel operations. <br>
Mitigation: Review previews carefully before approving chat or direct-message actions, and disclose the specific message or channel effect before execution. <br>


## Reference(s): <br>
- [ClickUp API Documentation](https://clickup.com/api) <br>
- [ClickUp API Reference](https://clickup.com/api/docs) <br>
- [ClawLink OpenClaw Documentation](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink Verification](https://claw-link.dev/verify) <br>
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/clickup-tasks) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Markdown] <br>
**Output Format:** [Markdown with inline bash command examples and JSON tool-call parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Write and destructive operations require preview and explicit user confirmation before execution.] <br>

## Skill Version(s): <br>
1.0.5 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
