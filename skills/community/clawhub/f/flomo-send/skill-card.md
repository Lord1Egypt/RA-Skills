## Description: <br>
Sends text notes and tags to flomo through a configured webhook, with setup guidance for storing the webhook token. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiantao1001](https://clawhub.ai/user/qiantao1001) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to capture short notes, links, clipboard text, and tagged memos from command-line workflows into their flomo inbox. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Notes passed to the skill can be sent to flomo over the network. <br>
Mitigation: Use the skill only for content intended for flomo, and avoid sending secrets or highly sensitive notes. <br>
Risk: The webhook token is a credential and may be stored in a local .env file or shell startup file. <br>
Mitigation: Prefer the default local .env storage with restricted permissions, protect the token like a password, and avoid storing it in shared shell configuration. <br>
Risk: The documentation is inconsistent about URL Scheme behavior versus webhook-only delivery. <br>
Mitigation: Review the installed README and script behavior during setup; expect webhook delivery unless the artifact is updated to support another path. <br>


## Reference(s): <br>
- [Flomo API Reference](references/api.md) <br>
- [flomo incoming webhook settings](https://flomoapp.com/mine?source=incoming_webhook) <br>
- [flomo official API help](https://help.flomoapp.com/advance/api.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and plain-text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May send user-provided note content to flomo over the network when the webhook script is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
