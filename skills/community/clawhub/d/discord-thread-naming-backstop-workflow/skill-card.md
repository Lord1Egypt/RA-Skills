## Description: <br>
Checks recent Discord threads in a fixed dispatch parent channel, renames malformed thread titles to a standard pattern, and stays silent unless a final failure or recovery notification is needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[can4hou6joeng4](https://clawhub.ai/user/can4hou6joeng4) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run a low-noise backstop workflow for Discord dispatch threads, correcting only recent or clearly polluted thread names while avoiding historical cleanup. It is intended for environments where an agent has permission to list threads, rename matching thread channels, and send incident or resolved notifications only when required. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can rename Discord threads in the configured dispatch channel. <br>
Mitigation: Install it only when that mutation is intended, use least-privilege Discord credentials, and keep access scoped to the target guild and parent channel. <br>
Risk: Overly broad execution could rename historical or unrelated threads. <br>
Mitigation: Keep the workflow limited to the documented guild and parent channel, skip compliant names, and process only recent threads or same-day titles with clear truncation or JSON pollution. <br>
Risk: Discord API failures or permission limits can leave a malformed thread name unchanged. <br>
Mitigation: Use the documented retry and consistency-check flow, then send a single P2 notification only when the final state still fails the naming rule. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/can4hou6joeng4/discord-thread-naming-backstop-workflow) <br>
- [Dispatch thread rename notification templates](references/dispatch-thread-rename-notification-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Text] <br>
**Output Format:** [Markdown workflow guidance with Discord message action calls and optional plain-text notifications] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Normal successful runs are silent; final failures and resolved recoveries use bounded notification templates.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
