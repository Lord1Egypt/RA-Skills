## Description: <br>
Checks Google Antigravity AI model quota and token balance by detecting a local Antigravity language server process and querying its local API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[finderstrategy-cyber](https://clawhub.ai/user/finderstrategy-cyber) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Antigravity users use this skill to check remaining model quota, token balance, reset timing, and account tier from a local Antigravity or Windsurf session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill displays account identity and quota details that may be sensitive in shared shells, recordings, CI logs, or support transcripts. <br>
Mitigation: Avoid verbose mode and JSON output in shared or recorded environments, and treat generated terminal output as sensitive. <br>
Risk: The script reads local Antigravity process arguments, including the local CSRF token, to query the local API. <br>
Mitigation: Run it only on a trusted local machine where Antigravity or Windsurf is already running, and do not share verbose logs or process output. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; script output is terminal text or JSON when --json is used.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and a running local Antigravity or Windsurf process.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
