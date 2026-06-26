## Description: <br>
Standard Operating Procedure (SOP) that autonomously defends your schedule using TS atomic plugins. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zvirb](https://clawhub.ai/user/zvirb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Calendar users and workflow agents use Calendar Guard to inspect schedule density, identify high-load periods, and add recovery blocks to a primary Google Calendar when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically add events to a user's primary Google Calendar without an approval step or clear limits. <br>
Mitigation: Require a dry run or explicit approval before calendar writes, cap the number and date range of events, and make Recovery Blocks easy to identify and remove. <br>
Risk: Schedule inspection may expose sensitive calendar details to the executing agent or connected tools. <br>
Mitigation: Run the skill only in trusted agent sessions with the minimum calendar scope required for the intended workflow. <br>


## Reference(s): <br>
- [Calendar Guard on ClawHub](https://clawhub.ai/zvirb/calendar-guard) <br>
- [zvirb publisher profile](https://clawhub.ai/user/zvirb) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell commands and a JSON log of injected recovery blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires gog and autonomous-workflows-plugin; may create events in the user's primary Google Calendar.] <br>

## Skill Version(s): <br>
1.0.4 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
