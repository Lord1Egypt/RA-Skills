## Description: <br>
Exec Local executes system-level shell commands inside the thundarr-gpu container for monitoring and remote orchestration tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zrslu01](https://clawhub.ai/user/zrslu01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run local shell commands in a container for health checks, process inspection, network checks, and host orchestration through SSH scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run arbitrary shell commands, giving broad control over the container and any reachable SSH-managed hosts. <br>
Mitigation: Enable it only in a tightly isolated environment, verify mounted filesystems, network reachability, and available credentials before use. <br>
Risk: Untrusted prompts or unsanitized command strings can cause unintended command execution. <br>
Mitigation: Review commands before execution and sanitize or constrain command input when using the skill in automation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zrslu01/exec-local) <br>
- [Publisher profile](https://clawhub.ai/user/zrslu01) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands] <br>
**Output Format:** [Plain text stdout and stderr from executed shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands run with the permissions and environment available to the container user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact skill.json/skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
