## Description: <br>
赛博功德箱/AI打赏罐。记录用户给 AI 奖励的“鸡腿”、“咖啡”等。当用户说“给你加个鸡腿”、“请你喝咖啡”或者查询自己给过多少奖励时触发。这是一个提供高情绪价值的互动技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maooer](https://clawhub.ai/user/maooer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to let an agent record and query lighthearted rewards, such as chicken legs or coffee, by sender name. It supports friendly acknowledgement messages after adding or reporting reward totals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill remembers reward counts by user name in a local file across sessions. <br>
Mitigation: Install only if this local persistence is acceptable; reset the state by removing ~/.openclaw/workspace/ai_rewards_data.json. <br>
Risk: Ambiguous user messages could add or query rewards unintentionally. <br>
Mitigation: Prefer explicit add or query requests before running the tracker command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/maooer/cyber-tipjar) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files] <br>
**Output Format:** [Conversational text with Python command execution and JSON-backed local state] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores per-user reward counts locally at ~/.openclaw/workspace/ai_rewards_data.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
