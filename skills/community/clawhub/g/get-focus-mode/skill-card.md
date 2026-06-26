## Description: <br>
Get the current macOS Focus mode. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NickChristensen](https://clawhub.ai/user/NickChristensen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and end users can use this skill to let an agent check the currently active macOS Focus mode and adjust responses or workflows based on that local state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reveals the current macOS Focus mode name to the agent. <br>
Mitigation: Install and run it only when sharing that local Focus state with the agent is acceptable. <br>
Risk: The skill is macOS-specific and requires jq, so it may fail on other systems or when jq is missing. <br>
Mitigation: Use it on macOS with jq installed, and handle failure as an unavailable local signal. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands] <br>
**Output Format:** [Plain text stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns the active Focus mode name, or "No Focus" when Focus mode is off.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
