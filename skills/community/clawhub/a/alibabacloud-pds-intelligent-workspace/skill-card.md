## Description: <br>
This skill helps agents operate Alibaba Cloud PDS cloud drives, including file search, upload, download, archive download, document and media analysis, image editing, visual search, mount app workflows, and share link management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to automate Alibaba Cloud PDS file operations through Aliyun CLI workflows. It is intended for credentialed PDS environments where users need controlled search, transfer, analysis, sharing, archive, image-processing, or mount operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables broad credentialed access to Alibaba Cloud PDS drives. <br>
Mitigation: Install only when PDS automation is intended, use least-privilege RAM users or short-lived tokens, and avoid root or administrator cloud credentials. <br>
Risk: Credential setup and CLI workflows can expose sensitive access keys or tokens if handled in chat, shell history, logs, or plaintext configuration. <br>
Mitigation: Configure credentials outside the agent session, do not print AK/SK values, and use only status checks such as `aliyun configure list` during agent workflows. <br>
Risk: Share links and signed download URLs can expose private files. <br>
Mitigation: Review generated share links before sending them and keep raw analysis JSON and signed URLs out of shared logs or temporary public locations. <br>
Risk: Mount-app installation can add persistent host-level background software. <br>
Mitigation: Treat mount-app installation as an administrative action, verify the vendor source, and require manual approval before installation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/alibabacloud-pds-intelligent-workspace) <br>
- [CLI Installation Guide](references/cli-installation-guide.md) <br>
- [PDS Aliyun CLI Configuration Guide](references/config.md) <br>
- [RAM Permission Policies](references/ram-policies.md) <br>
- [PDS Drive Operations](references/drive.md) <br>
- [PDS Upload Guide](references/upload-file.md) <br>
- [PDS Download Guide](references/download-file.md) <br>
- [PDS Archive Download Guide](references/archive-download.md) <br>
- [PDS Share Link Guide](references/share-link.md) <br>
- [PDS Mount App Guide](references/mountapp.md) <br>
- [Aliyun CLI Documentation](https://help.aliyun.com/zh/cli/) <br>
- [Alibaba Cloud PDS Mount Drives Documentation](https://help.aliyun.com/zh/pds/drive-and-photo-service-ent/user-guide/mount-drives) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, API Calls, Code, Files, Markdown, Guidance] <br>
**Output Format:** [Markdown with inline bash commands, JSON examples, and file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or download local files, generate signed URLs, run Python helper scripts, and invoke Aliyun CLI commands with a required skill user agent.] <br>

## Skill Version(s): <br>
0.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
