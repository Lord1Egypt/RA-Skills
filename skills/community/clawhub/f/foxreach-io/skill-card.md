## Description: <br>
Manage FoxReach cold email outreach: leads, campaigns, sequences, templates, email accounts, inbox, and analytics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[concaption](https://clawhub.ai/user/concaption) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and operators use this skill to manage FoxReach cold email outreach workflows through the FoxReach SDK and CLI, including lead management, campaign setup, sequence editing, inbox triage, and analytics review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change FoxReach account data, including creating or deleting leads, templates, campaigns, sequences, and email accounts. <br>
Mitigation: Use a least-privileged FoxReach API key and require explicit user confirmation plus a dry-run summary before destructive or bulk-changing operations. <br>
Risk: The skill can add recipients or senders and start live cold-email campaigns. <br>
Mitigation: Require explicit confirmation before adding recipients or senders or starting campaigns, and show the campaign, sequence, account, and recipient summary before execution. <br>
Risk: The skill depends on a referenced SDK or CLI that may execute authenticated FoxReach API calls. <br>
Mitigation: Inspect the SDK or CLI before giving it an API key, keep keys out of source files, and pass credentials through the environment or approved CLI configuration. <br>


## Reference(s): <br>
- [FoxReach API Reference](api-reference.md) <br>
- [FoxReach SDK Examples](examples.md) <br>
- [ClawHub skill page](https://clawhub.ai/concaption/foxreach-io) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce FoxReach API operation plans, SDK snippets, CLI commands, summaries, and confirmation prompts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
