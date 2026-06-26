## Description: <br>
Generates a daily morning brief with Shanghai weather and the top five V2EX hot posts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alibaba4184hub](https://clawhub.ai/user/alibaba4184hub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users or automation agents use this skill to produce a concise daily briefing when requested or on an 8:00 AM cron schedule. The brief combines current Shanghai weather with five current V2EX hot-post titles and node names for Telegram delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts wttr.in and V2EX to build the brief. <br>
Mitigation: Install only if outbound access to those services is acceptable for the deployment environment. <br>
Risk: The workflow sends the generated brief to a Telegram destination. <br>
Mitigation: Verify the bot token and chat destination before enabling delivery. <br>
Risk: An enabled cron trigger can send daily messages automatically. <br>
Mitigation: Keep the cron trigger disabled unless automatic daily delivery is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alibaba4184hub/daily-every) <br>
- [wttr.in Shanghai weather endpoint](https://wttr.in/Shanghai?format=3) <br>
- [V2EX hot topics API](https://www.v2ex.com/api/topics/hot.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-style daily brief with date, weather, and a numbered list of V2EX posts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Designed for Telegram delivery after contacting wttr.in and V2EX.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
