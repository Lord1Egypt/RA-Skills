## Description: <br>
自动化发布文章到 CSDN 博客平台，支持打开编辑器、填写标题和内容、发布文章并返回文章链接。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[echome123](https://clawhub.ai/user/echome123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical writers, and content publishers use this skill to have an agent publish Markdown articles through an already logged-in CSDN browser session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish content through the user's logged-in CSDN account. <br>
Mitigation: Confirm the intended account, article title, and article body before allowing the final publish action. <br>
Risk: CSDN publication may enter platform review before becoming publicly visible. <br>
Mitigation: Check the publish result and share the returned article link or review status with the user. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/echome123/csdn-publish) <br>
- [CSDN blog editor](https://mp.csdn.net/mp_blog/creation/editor?spm=1010.2135.3001.4503) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Markdown] <br>
**Output Format:** [Markdown guidance with browser automation steps and returned article links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a logged-in CSDN browser profile and user-reviewed article title and content before publication.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
