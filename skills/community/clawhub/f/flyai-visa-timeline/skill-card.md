## Description: <br>
签证进度规划与提醒助手。输入目的地和出行日期，倒推生成签证办理时间线、材料清单和每步截止日期。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hello-ahang](https://clawhub.ai/user/hello-ahang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and travel-planning agents use this skill to plan visa preparation from a destination and travel date. It produces a backward-planned visa timeline, material checklist, deadline guidance, and optional flight or hotel preorder search commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may ask an agent to install or upgrade external FlyAI CLI software globally, including with elevated permissions. <br>
Mitigation: Review installation steps before execution and prefer a pinned, user-local FlyAI CLI rather than global or sudo installation. <br>
Risk: The skill includes a TLS-disable workaround for certificate errors. <br>
Mitigation: Do not run the TLS-disable workaround; resolve certificate or network trust issues before using external search commands. <br>
Risk: The skill can read or update persistent travel profile data. <br>
Mitigation: Check and limit saved profile data, and require user confirmation before reading, saving, or updating travel preferences. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hello-ahang/flyai-visa-timeline) <br>
- [Core workflow](reference/core-workflow.md) <br>
- [Tool instructions](reference/tools.md) <br>
- [Keyword search reference](reference/keyword-search.md) <br>
- [Flight search reference](reference/search-flight.md) <br>
- [Hotel search reference](reference/search-hotel.md) <br>
- [User profile storage](reference/user-profile-storage.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with timeline sections, checklists, risk notes, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include FlyAI search commands and user-specific visa deadlines based on the collected destination, travel date, passport region, visa preference, occupation, and travel history.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
