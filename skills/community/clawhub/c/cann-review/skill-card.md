## Description: <br>
Reviews CANN GitCode pull requests for memory safety, security, readability, and logic issues, then produces structured review reports and can post PR comments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hzrky](https://clawhub.ai/user/hzrky) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers working on CANN repositories use this skill to review GitCode PRs, generate structured Markdown review reports, and optionally run scheduled scans that comment on candidate PRs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release ships embedded GitCode credentials. <br>
Mitigation: Remove embedded tokens before use, rotate any exposed token, and configure a least-privilege GitCode token through environment or local config. <br>
Risk: Automation can comment on PRs or mark PRs reviewed without a confirmed completed review. <br>
Mitigation: Disable scheduled or bulk review until the workflow is verified, and require human approval before comments or review status changes are posted. <br>
Risk: Scheduled scans can operate across configured repositories using write-capable GitCode API access. <br>
Mitigation: Restrict the repository list and token permissions, start with manual or dry-run review, and audit generated reports before enabling recurring execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/hzrky/cann-review) <br>
- [CANN runtime repository](https://gitcode.com/cann/runtime) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact setup guide](artifact/SETUP_GUIDE.md) <br>
- [Artifact auto-review guide](artifact/AUTO_REVIEW_GUIDE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown review reports, JSON result summaries, and shell/API command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May post GitCode PR comments or run scheduled batch scans when configured with GitCode credentials.] <br>

## Skill Version(s): <br>
4.2.1 (source: server release metadata and SKILL.md version history) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
