## Description:

中文番茄钟专注计时工具。开始25分钟专注时段，统计今日完成数量，本地存储无需账号。支持开始、暂停、继续、查看状态、统计等功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and external users can use this Chinese-language Pomodoro skill to start, pause, resume, and check 25-minute focus sessions. It also helps users review today's completed sessions and locally stored focus history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may write focus-session records to ~/.qclaw/data/pomodoro.json.

Mitigation: Review local storage behavior before use and remove the local data file if session history should not persist.

Risk: The included documentation and secondary script have quality mismatches, including an unrelated promotional footer.

Mitigation: Confirm the intended timer entry point and user-facing copy before packaging or deploying the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/cn-pomodoro-timer)
- [Publisher profile](https://clawhub.ai/user/freedompixels)
- [AISoBrand](https://aisobrand.com)
- [AISoBrand free diagnosis](https://aisobrand.com/free-diagnosis.html)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Chinese-language plain text responses and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local focus-session records at ~/.qclaw/data/pomodoro.json.]

## Skill Version(s):

1.2.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
