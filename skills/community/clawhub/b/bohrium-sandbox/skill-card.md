## Description: <br>
Bohrium Sandbox (`lbg sdbx`) guides agents in creating and operating Bohrium on-demand cloud VMs for shell, Python, debugging, data processing, and GPU jobs with optional user-storage mounts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sorrymaker0624](https://clawhub.ai/user/sorrymaker0624) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to run short-lived Bohrium sandboxes for command execution, script debugging, file transfer, data processing, and GPU validation. It is not intended for large batch jobs or persistent development machines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mounting user or shared storage gives sandboxed commands access to those files. <br>
Mitigation: Mount only the folders needed for the task, avoid sensitive data when running untrusted code, and review commands before allowing writes or network access. <br>
Risk: Killing a sandbox destroys its disk, so files cannot be read afterward. <br>
Mitigation: Retrieve required logs, outputs, and model artifacts with `lbg sdbx files read` before killing the sandbox. <br>
Risk: The skill requires a Bohrium accessKey and may bill against a personal wallet or project budget. <br>
Mitigation: Treat the accessKey as a secret, use trusted shells or environment configuration, and confirm the intended wallet or project budget before creating sandboxes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sorrymaker0624/bohrium-sandbox) <br>
- [lbg package version history](https://pypi.org/project/lbg/#history) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON-oriented CLI snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that create, operate, transfer files to and from, and terminate Bohrium sandboxes; users supply their own access key and sandbox IDs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
