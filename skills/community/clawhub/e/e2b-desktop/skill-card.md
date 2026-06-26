## Description: <br>
Control E2B Desktop sandboxes (virtual Linux desktops) for computer-use agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EYHN](https://clawhub.ai/user/EYHN) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to create and control E2B cloud Linux desktop sandboxes for computer-use agent workflows, including screenshots, mouse and keyboard actions, shell commands, browser or app launch, and VNC streaming. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Desktop-control scripts accept raw arguments that can execute unintended local Python code when crafted inputs are passed through shell heredocs. <br>
Mitigation: Only call the scripts with trusted or validated arguments; add escaping, validation, and confirmations before using raw model output or untrusted webpage text. <br>
Risk: The skill controls a live E2B desktop and can run shell commands inside the sandbox. <br>
Mitigation: Use a dedicated E2B API key, confirm destructive actions before execution, and run kill_sandbox.sh when the task is complete. <br>
Risk: VNC stream URLs and authentication keys can expose remote desktop access if logged or shared. <br>
Mitigation: Avoid printing or storing stream URLs and auth keys in shared logs; use authenticated streams when access control is needed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and script-produced text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scripts may produce sandbox IDs, stream URLs, screenshots, command output, cursor or screen state, and sandbox lifecycle messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
