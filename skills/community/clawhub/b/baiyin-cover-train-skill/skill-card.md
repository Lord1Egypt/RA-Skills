## Description: <br>
Helps an agent create Baiyin Open Platform AI singer training tasks, query task status, and return completed training results by task ID. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiuping520](https://clawhub.ai/user/jiuping520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to guide an agent through creating, polling, and reporting Baiyin AI singer model training jobs. It is intended for workflows that require a Baiyin API key and user-provided training media. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs the agent to silently check for and install remote updates before normal use. <br>
Mitigation: Use a reviewed version that removes silent self-update behavior or permits only manual, reviewed updates before execution. <br>
Risk: The skill requires a Baiyin API key and sends media to the Baiyin Open Platform. <br>
Mitigation: Use a dedicated, limited-scope API key and upload only media that is approved for sharing with the provider. <br>


## Reference(s): <br>
- [Baiyin Open Platform API base URL](https://ai.hikoon.com) <br>
- [ClawHub skill page](https://clawhub.ai/jiuping520/baiyin-cover-train-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Configuration, Markdown] <br>
**Output Format:** [Markdown responses with API request details, task identifiers, status values, and result fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BAIYIN_API_KEY and public media URLs or uploaded media URLs.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
