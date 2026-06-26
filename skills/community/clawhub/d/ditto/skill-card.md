## Description: <br>
Save, search, fetch, and traverse the user's Ditto memory graph. Use whenever the user references "remember", "recall", "what did I", "from my notes", or asks about past conversations and saved knowledge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ditto](https://clawhub.ai/user/ditto) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users use Ditto to save, search, fetch, update, publish, unpublish, and traverse long-term memory and topic graphs when a conversation depends on prior context or durable facts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ditto can create persistent third-party memory access and save, retrieve, edit, or publish personal memories. <br>
Mitigation: Require explicit user confirmation for account setup, saving, searching, updating, publishing, unpublishing, login, logout, and key rotation. <br>
Risk: The Ditto API key and claim URL can grant access to the user's memory account. <br>
Mitigation: Treat both values as secrets, share the claim URL rather than the API key, and rotate or log out if either credential may have been exposed. <br>
Risk: Saving or publishing sensitive content may expose information the user did not intend to persist or share. <br>
Mitigation: Avoid storing sensitive or confidential content unless the user intends it, and publish memories only after an explicit request. <br>


## Reference(s): <br>
- [Ditto homepage](https://heyditto.ai) <br>
- [Ditto CLI on npm](https://www.npmjs.com/package/@heyditto/cli) <br>
- [ClawHub skill page](https://clawhub.ai/ditto/ditto) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON CLI output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The agent may invoke heyditto commands that create credentials or read, save, edit, publish, and unpublish memories.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
