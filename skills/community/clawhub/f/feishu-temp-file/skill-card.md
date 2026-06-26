## Description: <br>
Feishu File Sender helps stage files in a temporary directory so OpenClaw can send Feishu images or files that would otherwise be blocked by path allowlist checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yingyangdao](https://clawhub.ai/user/yingyangdao) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw users and developers use this skill to configure Feishu file-sending permissions, copy a local file into an approved temporary media directory, and clean staged files after sending. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup can persistently grant broad or whole-system OpenClaw file access that is broader than the file-staging task requires. <br>
Mitigation: Review and manually control permission changes; prefer a narrow configuration limited to the exact temporary media directory needed. <br>
Risk: Medium and loose permission presets may expose paths beyond the intended temporary media directory, including the whole filesystem for the loose preset. <br>
Mitigation: Avoid medium and loose presets, especially any configuration using /**, unless a reviewer has accepted that access scope. <br>
Risk: Sensitive documents may remain staged after Feishu sending. <br>
Mitigation: Run the cleanup flow after sending sensitive files and verify staged files have been removed. <br>


## Reference(s): <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>
- [Feishu Developer Documentation](https://open.feishu.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands; helper scripts return JSON status and file path output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stages local files into a temporary media directory and returns file paths or file URLs for Feishu sending.] <br>

## Skill Version(s): <br>
1.2.0 (source: package.json, _meta.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
