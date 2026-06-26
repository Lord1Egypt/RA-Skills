## Description: <br>
中文番茄钟专注计时工具。开始25分钟专注时段，统计今日完成数量，本地存储无需账号。支持开始、暂停、继续、查看状态、统计等功能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People who use Chinese-language productivity workflows can use this skill to start, pause, resume, inspect, and summarize Pomodoro focus sessions. It stores session state and daily completion history locally without requiring an account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes focus-session state and history to a local JSON file in the user's home directory. <br>
Mitigation: Review the local data path before use and back up or remove ~/.qclaw/data/pomodoro.json if local Pomodoro history should not be retained. <br>
Risk: The timer scripts can run for the configured focus and break durations, which may occupy the terminal session. <br>
Mitigation: Run the timer only in an intended interactive shell and interrupt it with Ctrl+C if the session should stop early. <br>
Risk: Security evidence is clean, but the security guidance still recommends reviewing commands before running ClawHub skills. <br>
Mitigation: Review the provided commands and local file behavior before execution, especially in shared or automated environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freedompixels/cn-pomodoro-timer) <br>
- [Publisher profile](https://clawhub.ai/user/freedompixels) <br>
- [AISoBrand website](https://aisobrand.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files] <br>
**Output Format:** [Plain text Chinese status messages and local JSON records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes Pomodoro state and history to ~/.qclaw/data/pomodoro.json.] <br>

## Skill Version(s): <br>
1.2.7 (source: server release evidence; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
