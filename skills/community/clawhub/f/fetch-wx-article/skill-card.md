## Description: <br>
Fetches WeChat public account article content from mp.weixin.qq.com links and converts the fetched HTML into Markdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tomjamescn](https://clawhub.ai/user/tomjamescn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when a user provides a WeChat public article link and needs the title, author, body, and article text extracted into Markdown for reading, processing, or archiving. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script fetches a user-provided URL over the network. <br>
Mitigation: Use it with public WeChat article links and add domain validation in stricter environments. <br>
Risk: Runtime behavior depends on external Python packages. <br>
Mitigation: Pin dependency versions before deployment in controlled environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tomjamescn/fetch-wx-article) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands] <br>
**Output Format:** [Markdown article content printed to standard output, with Python code and shell commands provided by the skill.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Ignores links and images by default when converting fetched HTML to Markdown.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
