## Description: <br>
Initializes a BOC container platform deployment machine by checking the host environment, verifying and unpacking the deployment package, running bocctl init, and validating key services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hongruiji](https://clawhub.ai/user/hongruiji) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and platform operators use this skill to initialize a BOC deployment machine by supplying the deployment package location, SSH connection details, and package filename. It guides environment checks, SHA256 verification, package extraction, bocctl init execution, and post-init service validation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for privileged SSH access and may expose plaintext root credentials if users paste passwords into chat or logs. <br>
Mitigation: Prefer SSH keys or temporary credentials, confirm the target host before use, and avoid placing passwords in chat transcripts or log files. <br>
Risk: The workflow includes destructive cleanup of an existing BOC_k8s_noarch directory before unpacking. <br>
Mitigation: Confirm the deployment directory and back up or rename any existing BOC_k8s_noarch directory before running removal commands. <br>
Risk: The skill references installing an sshpass binary from an external source. <br>
Mitigation: Do not install the suggested binary unless the source is verified and trusted; use an already approved SSH method when available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hongruiji/boc-init) <br>
- [sshpass-win32 release referenced by the skill](https://github.com/xhcoding/sshpass-win32/releases/download/v1.0.7/sshpass.exe) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with shell command snippets and status checks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes privileged SSH setup guidance, deployment package verification, destructive cleanup before extraction, bocctl init execution, and container/service validation checks.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
