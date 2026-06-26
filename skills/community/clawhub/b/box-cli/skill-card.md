## Description: <br>
Box CLI skill for working with files, folders, metadata, search, and Box AI in headless environments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hbkwong](https://clawhub.ai/user/hbkwong) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation agents use this skill to configure and run the Box CLI in headless environments for file, folder, metadata, search, and Box AI workflows with user-provided Box credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Box credentials or generated configuration files could be exposed if stored in the workspace, committed to source control, pasted into chat, or left in local CLI configuration. <br>
Mitigation: Use a dedicated secret store or protected file outside the workspace, restrict file permissions, avoid committing credential files, rotate credentials regularly, and delete local CLI configuration when the integration is no longer needed. <br>
Risk: A Box app or service account with broad scopes could expose or modify more enterprise content than intended. <br>
Mitigation: Use a dedicated least-privilege Box app or service account, limit app scopes and accessible folders, and prefer a dedicated demo folder when showcasing functionality. <br>


## Reference(s): <br>
- [Box CLI documentation](https://developer.box.com/guides/cli/) <br>
- [ClawHub Box skill listing](https://clawhub.ai/hbkwong/box-cli) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Assumes the Box CLI binary is installed and credentials are supplied by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
