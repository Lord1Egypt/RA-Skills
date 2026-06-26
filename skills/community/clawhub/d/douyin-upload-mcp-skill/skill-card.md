## Description: <br>
Automates Douyin Creator Platform publishing, login checks, Feishu notifications, analytics, interaction replies, and digital-human marketing workflows through MCP tools and local scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrchenyh](https://clawhub.ai/user/mrchenyh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run Douyin publishing, login recovery, Feishu-guided customer workflows, data reporting, comment/DM replies, and digital-human marketing automation from an agent environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control a Douyin account, send Feishu messages, read interaction data, and run persistent background jobs. <br>
Mitigation: Install it on a dedicated machine or browser profile, review bootstrap and scheduler behavior before use, and grant only the accounts and credentials needed for the intended workflow. <br>
Risk: Local daemon and browser automation ports may expose account-control surfaces if reachable from a network. <br>
Mitigation: Keep daemon ports bound to local use, do not expose them publicly, and run the automation in a restricted environment. <br>
Risk: Automatic comment and private-message replies can send customer-facing messages without manual review when enabled. <br>
Mitigation: Inspect or disable the scheduler and require explicit approval for reply workflows unless the deployment policy allows automated responses. <br>


## Reference(s): <br>
- [English README](README.en.md) <br>
- [Customer Install Guide](references/customer-install-guide.md) <br>
- [Publish Flow](references/publish-flow.md) <br>
- [Data, Comments, And DMs](references/data-interactions.md) <br>
- [Pitfalls And Generalization Rules](references/pitfalls.md) <br>
- [Local Configuration Template](references/skill-local-config.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON examples, shell commands, configuration snippets, and MCP tool instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May start persistent local browser, scheduler, and Feishu/Douyin automation jobs when configured and authorized.] <br>

## Skill Version(s): <br>
0.1.8 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
