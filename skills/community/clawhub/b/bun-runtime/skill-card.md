## Description: <br>
Bun Runtime provides native Bun filesystem, process, and network operations for agents working with Bun APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rabin-thami](https://clawhub.ai/user/rabin-thami) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to ask an agent to read and write files, match paths, run process commands, and make HTTP requests through Bun runtime helpers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad local shell, filesystem, and network capability through Bun. <br>
Mitigation: Install it only in trusted workspaces and review each command, path, URL, and request body before execution. <br>
Risk: Untrusted strings passed into shell, filesystem, or network helpers can expand the impact of agent mistakes or misuse. <br>
Mitigation: Avoid passing untrusted input and prefer a safer version that removes eval, constrains file access to an approved workspace, and requires explicit approval for command execution and outbound requests. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, files, API calls, JSON] <br>
**Output Format:** [Shell command invocations with JSON responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [File helpers can read and write local paths, process helpers can execute commands, and network helpers can return HTTP status, success state, and response text.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
