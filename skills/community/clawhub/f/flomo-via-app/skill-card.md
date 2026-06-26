## Description: <br>
Sends selected notes, tags, and memo text to flomo using a configured Flomo webhook. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiantao1001](https://clawhub.ai/user/qiantao1001) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to capture notes, links, clipboard text, or piped content into a flomo inbox from an agent workflow or shell, with optional hashtags. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Flomo webhook token and sends selected note content to Flomo. <br>
Mitigation: Use the default local .env storage with restricted permissions, avoid shell startup files when possible, and only send content intended for Flomo. <br>
Risk: Older skill text mentions URL-scheme behavior that does not match the current webhook-only send script. <br>
Mitigation: Treat scripts/flomo_send.sh as the source of runtime behavior and configure FLOMO_WEBHOOK_URL or FLOMO_WEBHOOK_TOKEN before use. <br>


## Reference(s): <br>
- [Flomo API Reference](references/api.md) <br>
- [Flomo incoming webhook settings](https://flomoapp.com/mine?source=incoming_webhook) <br>
- [Flomo official API help](https://help.flomoapp.com/advance/api.html) <br>
- [ClawHub skill page](https://clawhub.ai/qiantao1001/flomo-via-app) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and note text sent through webhook requests] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a flomo PRO webhook token; note content is limited to 5000 characters.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
