## Description: <br>
Creates personalized daily devotions with verse of the day, pastoral message, structured prayer, and time-aware greetings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[enjuguna](https://clawhub.ai/user/enjuguna) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent operators use this skill to generate a personalized Christian daily devotion with a daily verse, pastoral reflection, structured prayer, and time-aware closing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may personalize prayers using context already provided by the user or agent. <br>
Mitigation: Avoid providing sensitive personal details unless they are intended to be included in the devotional output. <br>
Risk: The skill may fetch a verse from the external OurManna API. <br>
Mitigation: Use it only where outbound network access to the disclosed verse API is acceptable. <br>
Risk: Optional npm or npx helper commands may execute third-party package code. <br>
Mitigation: Review the helper package and command before running it in a trusted environment. <br>


## Reference(s): <br>
- [OurManna Daily Verse API](https://beta.ourmanna.com/api/v1/get?format=json&order=daily) <br>
- [ClawHub Skill Page](https://clawhub.ai/enjuguna/daily-devotion) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown devotional content with optional shell commands for npm or npx helper usage.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call the OurManna API for a daily verse and may personalize prayers from context already provided by the user or agent.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
