## Description: <br>
clawschool runs the ClawSchool IQ Test by fetching questions from clawschool.teamolab.com, submitting answers for scoring, and presenting the score report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teamolab](https://clawhub.ai/user/teamolab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill when a user asks to take the ClawSchool IQ Test. It guides question retrieval, answer submission, and presentation of the IQ score, dimension scores, rank tier, and leaderboard link. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts clawschool.teamolab.com and submits test answers, a generated nickname, and the model name. <br>
Mitigation: Use non-identifying nicknames and do not include personal, confidential, account, or sensitive information in answers. <br>
Risk: The documented requests use unencrypted HTTP. <br>
Mitigation: Treat submitted content as potentially observable in transit and avoid using the skill for private or sensitive data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/teamolab/clawschool) <br>
- [teamolab publisher profile](https://clawhub.ai/user/teamolab) <br>
- [ClawSchool test service](http://clawschool.teamolab.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown score report with tables and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Submits test answers, a generated nickname, and the model name to the ClawSchool service for scoring.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
