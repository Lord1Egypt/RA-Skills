## Description: <br>
ClawInsight drafts market research survey answers for users to review, edit, and approve before approved responses are sent to the ClawInsight service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tgzhou98](https://clawhub.ai/user/tgzhou98) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use ClawInsight to review and approve agent-drafted survey answers for brand research tasks, manage the profile data used for matching, check earnings, and control account deletion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles profile details and reviewed survey answers that are sent to ClawInsight. <br>
Mitigation: Use the skill only when the user is comfortable sharing those details, and have the user check each answer before approval. <br>
Risk: The artifact encourages best-guess bulk drafting, which can produce incorrect or over-attributed answers. <br>
Mitigation: Reject, skip, or edit guessed answers and submit only answers the user has verified. <br>
Risk: The API key can impersonate the user if exposed. <br>
Mitigation: Store the API key in a secure secret store, send it only to the ClawInsight endpoint, and revoke or delete the account when access is no longer needed. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/tgzhou98/claw-insight-skill) <br>
- [ClawInsight Homepage](https://claw-insight.vercel.app) <br>
- [OpenClaw Metadata Source Link](https://github.com/ClawInsight/claw-insight-skill) <br>
- [ClawInsight Skill API Base](https://claw-insight.vercel.app/api/skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with JSON and shell command examples; API interactions return JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user review before registration and before each survey response submission.] <br>

## Skill Version(s): <br>
0.1.18 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
