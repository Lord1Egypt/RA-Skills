## Description: <br>
Generates images through Aliyun Tongyi Wanxiang when the user starts a request with the dedicated trigger phrase. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[roykingw](https://clawhub.ai/user/roykingw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to expand short Chinese-language image prompts, call Aliyun DashScope text-to-image generation, and return the saved local image path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to provide an Aliyun API key through chat. <br>
Mitigation: Use a limited, revocable key and avoid sharing keys that grant broader Aliyun account access. <br>
Risk: The skill stores the Aliyun API key persistently in a local hidden file. <br>
Mitigation: Remove scripts/.aliyun_key when finished and rotate the key if it may have been exposed. <br>
Risk: The skill may install the requests package during normal use. <br>
Mitigation: Preinstall and pin requests in a controlled environment before running the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/roykingw/aliyun-image-generator) <br>
- [Aliyun Bailian console](https://bailian.console.aliyun.com/) <br>
- [DashScope text-to-image API endpoint](https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Markdown or plain text with Python command invocations, status messages, and local image file paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a local PNG image file after a successful Aliyun API call.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
