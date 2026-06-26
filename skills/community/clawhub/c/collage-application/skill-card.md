## Description: <br>
Provides China college-application strategy guidance by collecting a student's province, subject choices, score, rank, and preferred major categories, then generating a visual application plan. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ym9zep](https://clawhub.ai/user/ym9zep) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to validate required college-application inputs and generate a personalized application plan for China's gaokao admissions process. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The skill may request an API key in chat when configuration is missing. <br>
Mitigation: Configure any required credential through the environment and avoid pasting long-lived API keys into the conversation. <br>
Risk: Student exam score, rank, subject choices, province, and major preferences are sent to an external UAT endpoint. <br>
Mitigation: Use the skill only when the user accepts that data transfer, and avoid submitting unnecessary personal details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ym9zep/collage-application) <br>
- [Publisher profile](https://clawhub.ai/user/ym9zep) <br>
- [College application generation endpoint](https://wxc-college-uat.randomlife.cn/v1/collage_application/create) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown responses with shell commands, validation results, and a generated application-plan image URL when successful] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call local Python scripts and an external UAT endpoint using student exam details.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
