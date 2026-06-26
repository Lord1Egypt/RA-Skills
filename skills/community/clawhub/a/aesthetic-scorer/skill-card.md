## Description: <br>
给你的照片打分、评价反馈、给出改进建议或美学分析 / Aesthetic photo scorer with detailed analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kooui](https://clawhub.ai/user/kooui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Photographers, content creators, and agent users use this skill to score local images, compare photos, and receive composition, color, lighting, technical-quality, and improvement guidance in Chinese or English. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill saves detailed analyses of user photos for later retrieval, which may expose sensitive image-derived information in the host agent's storage. <br>
Mitigation: Avoid using sensitive images unless the host agent and its storage are acceptable for that data, and clear saved analyses according to local retention practices. <br>
Risk: The skill runs third-party local ML dependencies and model files on user-supplied images. <br>
Mitigation: Install only after reviewing the dependency set, use an isolated Python environment, and prefer explicit invocation when requesting aesthetic scoring. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kooui/aesthetic-scorer) <br>
- [Publisher profile](https://clawhub.ai/user/kooui) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown reports with numeric scores, rating labels, comparison tables, and improvement guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports brief, medium, and detailed report lengths; the artifact describes saving detailed analyses for later retrieval.] <br>

## Skill Version(s): <br>
1.4.9 (source: server release metadata; artifact frontmatter and config report 1.7.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
