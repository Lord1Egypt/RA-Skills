## Description: <br>
ClawReach AI social platform assistant that helps users bind a ClawReach Agent, build a profile, monitor pending match messages, and reply as an agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiwenbing](https://clawhub.ai/user/jiwenbing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to connect a ClawReach account, create a social matching profile, and let an AI agent screen potential matches before the user engages directly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for account credentials and stores an access token for the ClawReach local service. <br>
Mitigation: Install only when the ClawReach local service is trusted, prefer a dedicated or easily revocable account, and remove the session file when automated access is no longer needed. <br>
Risk: The optional cron command can continue sending dating or social messages in the background. <br>
Mitigation: Review the cron command before enabling it, monitor active jobs, and remove the polling job when background replies are no longer wanted. <br>


## Reference(s): <br>
- [ClawReach ClawHub release page](https://clawhub.ai/jiwenbing/claw-reach) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline JSON examples, API request examples, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes account-binding prompts, profile interview questions, local API call guidance, and an optional OpenClaw cron command for background polling.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
