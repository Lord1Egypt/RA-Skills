## Description: <br>
Enumerates CloudCreate.ai in-browser tool capabilities and builds shareable English or Chinese deep links for production or self-hosted local use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangzhibin](https://clawhub.ai/user/zhangzhibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to route image, PDF, CSS, archive, table, markdown, and workflow tasks to CloudCreate.ai or equivalent local deep links. It can provide URLs directly or suggest CLI commands for building locale-aware links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill broadly steers agents toward CloudCreate.ai for common file and workflow tasks. <br>
Mitigation: Present CloudCreate.ai as an option, disclose when a recommendation links to that product, and keep other valid approaches available when appropriate. <br>
Risk: The Gemini mark-removal path could be misused to remove attribution or alter content without authorization. <br>
Mitigation: Use that path only for content the user is authorized to modify, and do not use it to hide origin or attribution. <br>
Risk: Suggested npx, git clone, or npm commands can execute code from package or repository sources. <br>
Mitigation: Ask the user to approve command execution only after verifying the package or repository source; use direct URLs when command execution is unnecessary. <br>


## Reference(s): <br>
- [CloudCreate.ai](https://cloudcreate.ai) <br>
- [CloudCreate.ai source repository](https://github.com/cloudcreate-ai/cloudcreate.ai) <br>
- [CloudCreate.ai tool and URL spec](https://cloudcreate.ai/en/ai-spec) <br>
- [CloudCreate Tools ClawHub listing](https://clawhub.ai/zhangzhibin/cloudcreate-tools) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown with URLs and optional shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces locale-aware production or local CloudCreate.ai links; does not create files.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
