## Description: <br>
A tool to manage Baidu Wangpan (Baidu Netdisk) files using the official Baidu Open API, including quota checks, file listing, search, download-link generation, and file management with user-provided API keys and manual authorization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangyi-3](https://clawhub.ai/user/zhangyi-3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent operate Baidu Wangpan through Baidu's Open API after the user supplies developer credentials and completes manual authorization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent sensitive Baidu Netdisk access and stores Baidu API credentials and OAuth tokens in a local configuration file. <br>
Mitigation: Install only if comfortable with that account access, protect or remove ~/.openclaw/workspace/bwp_config.json when it is not needed, and avoid sharing command output that contains tokens or generated download URLs. <br>
Risk: File-changing commands can delete, move, rename, create, or upload files in the user's Baidu Netdisk. <br>
Mitigation: Require explicit user confirmation before delete, move, rename, mkdir, or directory-upload actions, and verify the target path before running the script. <br>
Risk: The security review verdict is suspicious because the skill has weak safeguards around credentials and file-changing actions. <br>
Mitigation: Review the script path and command arguments before execution, and follow the security guidance from the release evidence before deployment. <br>


## Reference(s): <br>
- [Baidu Netdisk Open Platform](https://pan.baidu.com/union) <br>
- [Baidu Disk Helper on ClawHub](https://clawhub.ai/zhangyi-3/baidu-disk-helper) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and command-line text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce authorization URLs, file metadata tables, download URLs, and curl examples; generated download URLs should be treated as secrets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
