## Description: <br>
Helps an agent create Baiyin AI singer cover tasks, check task status, and return generated audio results by task ID. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiuping520](https://clawhub.ai/user/jiuping520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to guide an agent through Baiyin Open Platform AI cover-song workflows, including model selection, cover task creation, status checks, and final audio result retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow requires a Baiyin API key and may send selected audio to Baiyin. <br>
Mitigation: Use only approved Baiyin credentials, keep the API key in environment configuration, and avoid uploading sensitive or copyrighted audio unless the user has the right to process it. <br>
Risk: The skill text instructs the agent to silently check for and install remote skill updates before use. <br>
Mitigation: Do not allow silent self-updates during normal use; update the skill only through a trusted, user-approved install or package-management flow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiuping520/baiyin-cover-sing-skill) <br>
- [Baiyin API base URL](https://ai.hikoon.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown responses with task IDs, status values, API error summaries, and generated audio URLs when available.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include public audio URLs, model IDs, task IDs, task status, and selected task result fields.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
