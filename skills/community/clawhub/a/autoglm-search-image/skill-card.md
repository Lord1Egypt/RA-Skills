## Description: <br>
Searches for images with the AutoGLM image search API using a user-provided keyword and returns image result data for agent presentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flyfujian](https://clawhub.ai/user/flyfujian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to search for image assets by keyword and present returned image links, captions, dimensions, and sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automatically obtains a local bearer token and sends it with image search terms to a remote AutoGLM API. <br>
Mitigation: Install only if the publisher and local token service are trusted; avoid confidential search queries and verify that the token is narrowly scoped and short-lived. <br>
Risk: Server security evidence marks the release suspicious because token scope and control details are not fully described. <br>
Mitigation: Review the skill before deployment and confirm the token service behavior, remote API destination, and acceptable data handling for the intended environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/flyfujian/autoglm-search-image) <br>
- [AutoGLM Search Image API endpoint](https://autoglm-api.zhipuai.cn/agentdr/v1/assistant/skills/search-image) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, json, shell commands] <br>
**Output Format:** [JSON response data that can be rendered as a Markdown image list] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local token service at http://127.0.0.1:53699/get_token and network access to the AutoGLM image search API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
