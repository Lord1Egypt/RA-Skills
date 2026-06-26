## Description: <br>
Helps agents read, inspect, overwrite, append to, and delete blocks in DingTalk enterprise documents when DingTalk document context is confirmed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shyzhen](https://clawhub.ai/user/shyzhen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and developers use this skill to let an agent operate on DingTalk enterprise documents after confirming the target is a DingTalk document. It supports document reading, structure inspection, full-document overwrite, paragraph append, and block deletion workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make live changes to enterprise DingTalk documents, including overwrite, append, insert, and delete operations. <br>
Mitigation: Use a least-privilege DingTalk app and require human confirmation of the exact document and block before any update, delete, append, or insert operation. <br>
Risk: DINGTALK_CLIENTSECRET and operator identity settings can expose privileged document access if shared broadly. <br>
Mitigation: Protect DINGTALK_CLIENTSECRET, avoid shared privileged DINGTALK_OPERATOR_ID values in multi-user deployments, and rely on per-user sender identity where available. <br>
Risk: The scan summary notes an under-disclosed insert command compared with the skill-facing usage instructions. <br>
Mitigation: Review available commands before installation and document whether insert is allowed in the deployment policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shyzhen/dingtalk-doc-enterprise) <br>
- [DingTalk Open Platform](https://open.dingtalk.com/) <br>
- [DingTalk OpenClaw connector docs](https://github.com/DingTalk-Real-AI/dingtalk-openclaw-connector?tab=readme-ov-file#%E9%92%89%E9%92%89%E6%96%87%E6%A1%A3docs%E4%B8%8E-mcpdocs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and text or JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js plus DingTalk application credentials in DINGTALK_CLIENTID and DINGTALK_CLIENTSECRET.] <br>

## Skill Version(s): <br>
1.0.6 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
