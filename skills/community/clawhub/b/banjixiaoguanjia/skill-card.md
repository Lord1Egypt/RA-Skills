## Description: <br>
Automates Banji Xiaoguanjia homework screenshot capture, original image download, and optional AI-assisted homework analysis for teachers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wosuiyu](https://clawhub.ai/user/wosuiyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Educators and agents supporting educators use this skill to collect student homework screenshots from Banji Xiaoguanjia, download original homework images, and generate AI-assisted grading notes and reports. It is intended for authorized class workflows where student work may be processed locally and, when analysis is enabled, by an external AI service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Student homework images may be uploaded to DashScope/Qwen or similar external AI services during analysis. <br>
Mitigation: Use the skill only with proper authorization, consent, and data-retention review; disable AI analysis when external upload is not permitted. <br>
Risk: The artifact handles credentials unsafely and includes API-key material that should not be trusted. <br>
Mitigation: Treat included keys as compromised, revoke or ignore them, and use new scoped credentials supplied through a controlled secret-management process. <br>
Risk: The artifact contains many archived or deprecated scripts, increasing the chance of running an unintended workflow. <br>
Mitigation: Run only the documented current scripts from SCRIPT-GUIDE.md after reviewing where screenshots, original images, and reports will be written. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wosuiyu/banjixiaoguanjia) <br>
- [Publisher profile](https://clawhub.ai/user/wosuiyu) <br>
- [SCRIPT-GUIDE.md](artifact/SCRIPT-GUIDE.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [package.json](artifact/package.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript and shell command examples; runtime scripts may create screenshots, downloaded images, TXT reports, and Word documents.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, npm, Playwright, Chrome access, and optional DashScope/Qwen credentials for AI analysis.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata, artifact frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
