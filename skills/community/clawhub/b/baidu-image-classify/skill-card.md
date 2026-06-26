## Description: <br>
Supports general object recognition, product recognition, and scene recognition with Baidu image-classification APIs, returning labels, product information, scene tags, and confidence scores. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maple-8899](https://clawhub.ai/user/maple-8899) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to classify image inputs through Baidu APIs, including object, product, and scene recognition workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary reports a hardcoded Baidu API key and unclear credential handling. <br>
Mitigation: Remove embedded credentials before use and configure Baidu API credentials through a protected secret or environment mechanism. <br>
Risk: Image inputs are submitted to Baidu for processing. <br>
Mitigation: Avoid sending private, regulated, or sensitive images unless the deployment owner has approved that data flow. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/maple-8899/baidu-image-classify) <br>
- [Baidu Advanced General Image Classification API](https://aip.baidubce.com/rest/2.0/image-classify/v2/advanced_general) <br>
- [Baidu OAuth Token Endpoint](https://aip.baidubce.com/oauth/2.0/token) <br>


## Skill Output: <br>
**Output Type(s):** [Code, API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown with Python code blocks and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Baidu OAuth credentials; image inputs are documented as jpg, png, or bmp files under 4 MB.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
