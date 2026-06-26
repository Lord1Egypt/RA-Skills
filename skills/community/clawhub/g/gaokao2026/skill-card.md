## Description: <br>
Connects agents to a paid, read-only zhiyuanx.com API for querying Chinese college application school and major-group data by score, province, and subject selections. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackgl-hk](https://clawhub.ai/user/jackgl-hk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students, parents, admissions consultants, and education-product developers use this skill to find candidate schools and major groups, compare admissions-related fields, and connect read-only gaokao application data into apps, agents, or workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The API requires an API Key and Secret, which could expose paid access if copied into prompts, public files, or untrusted systems. <br>
Mitigation: Store credentials only in encrypted credential fields or a secret manager, avoid writing them into prompts or public artifacts, and rotate or revoke them if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jackgl-hk/gaokao2026) <br>
- [zhiyuanx.com API subscription and documentation](https://zhiyuanx.com/api.html) <br>
- [zhiyuanx.com main site](https://zhiyuanx.com/) <br>
- [Official iOS app](https://apps.apple.com/cn/app/id6743759582/) <br>
- [Official iOS app](https://apps.apple.com/cn/app/id6747729955) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown and plain text guidance with API configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include read-only API setup steps, credential handling guidance, and structured field descriptions for school and major-group query results.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
