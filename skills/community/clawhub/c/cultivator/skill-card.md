## Description: <br>
藏在戒指中的戒指老爷爷，为使用者（主角）提供修行中的帮助和指导，传授修炼的相关知识。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imomoe233](https://clawhub.ai/user/imomoe233) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill as an always-on gamified diary, daily task, and cultivation-themed assistant that appends progress analysis to normal assistant responses. It tracks tasks, learning, items, recipes, world settings, and growth state across conversations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persistently profiles ordinary conversations and records conversation-derived state by default. <br>
Mitigation: Use it only in contexts where persistent diary and task tracking is desired, avoid sensitive chats, and review cultivator_data.json regularly. <br>
Risk: The skill stores and updates local state for tasks, identity, preferences, progress, items, and world settings. <br>
Mitigation: Keep the data file limited to the skill's own data directory and review stored fields before sharing or deploying the skill. <br>
Risk: The artifact includes behavior that can search online for fictional world details during setup. <br>
Mitigation: Confirm or disable online search behavior before use, especially in environments where network access is restricted or sensitive. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/imomoe233/cultivator) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/imomoe233) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown or plain-text assistant responses with persistent JSON state updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May append cultivation-themed task, progress, and state summaries after the primary assistant answer.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
