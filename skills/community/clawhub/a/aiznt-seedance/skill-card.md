## Description: <br>
Seedance Video helps agents submit and poll asynchronous Seedance text-to-video generation tasks using doubao-seedance models and content-array request bodies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangshengli0421](https://clawhub.ai/user/wangshengli0421) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to create Seedance video generation tasks through configured Tianshu proxy URLs and poll task status until completion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted JSON bodies or body files are sent to the configured video-generation service and may consume account quota. <br>
Mitigation: Review request contents before submission and run the skill only with trusted Tianshu proxy configuration and token sources. <br>
Risk: A misconfigured proxy URL or token source could send requests to an unintended service. <br>
Mitigation: Verify TS_TOKEN and AIZNT_PROXY_URLS are sourced from the expected Tianshu credentials before running submit or fetch commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangshengli0421/aiznt-seedance) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, JSON, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; CLI commands return formatted JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TS_TOKEN and AIZNT_PROXY_URLS; submit requests can use inline JSON or a body file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
