## Description: <br>
旅行提案生成器，帮用户生成一份用真实数据说服伴侣/老板/爸妈/朋友的旅行方案。调用FlyAI获取机票酒店景点真实价格，针对性击破顾虑，可直接转发微信。触发词：帮我说服、旅行提案、怎么说服、太贵了怎么办、帮我写个方案。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hello-ahang](https://clawhub.ai/user/hello-ahang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to gather destination, date, budget, and audience concerns, then generate a data-backed travel proposal for a partner, manager, parents, or friends. The agent uses FlyAI travel data to draft persuasive copy and an optional HTML proposal that can be shared directly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to install or update unpinned CLI software globally and suggests sudo as a fallback. <br>
Mitigation: Install only if the FlyAI CLI source is trusted, prefer user-scoped installs, pin a reviewed CLI version, and review commands before execution. <br>
Risk: The skill uses NODE_TLS_REJECT_UNAUTHORIZED=0 for travel-data queries, which disables TLS certificate verification. <br>
Mitigation: Remove the TLS bypass where possible and run travel-data queries only in trusted environments after reviewing the command. <br>
Risk: The skill may persist travel preferences in Qoder Memory or ~/.flyai/user-profile.md across sessions. <br>
Mitigation: Ask before saving preferences and review or delete the stored profile data when persistent travel preferences are not desired. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/hello-ahang/flyai-persuade-ta) <br>
- [FlyAI command reference](artifact/reference/flyai-commands.md) <br>
- [Persuasion templates](artifact/reference/persuasion-templates.md) <br>
- [Scenario templates](artifact/reference/scenario-templates.md) <br>
- [User profile storage](artifact/reference/user-profile-storage.md) <br>
- [Tool guidance](artifact/reference/tools.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, files, guidance] <br>
**Output Format:** [Markdown and shareable text with optional HTML file content and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include travel search results, budget breakdowns, audience-specific persuasion copy, and a generated HTML proposal file.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
