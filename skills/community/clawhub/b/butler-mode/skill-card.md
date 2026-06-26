## Description: <br>
Butler Mode transforms an agent into a manager that plans, delegates work to teammate agents, monitors progress, and reviews results instead of directly executing substantive tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[csuwl](https://clawhub.ai/user/csuwl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use Butler Mode to coordinate multi-agent work by decomposing requests, spawning teammate agents, tracking progress, and reviewing completed work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may spawn teammate agents with broad local authority. <br>
Mitigation: Install only when multi-agent manager mode is intentional, keep normal permission prompts enabled, and confirm before spawning, killing, or continuing agent sessions. <br>
Risk: The artifact encourages maximum autonomy and broad permissions for delegated agents. <br>
Mitigation: Avoid bypass-permission modes and review teammate outputs before accepting or applying changes. <br>


## Reference(s): <br>
- [Butler Mode on ClawHub](https://clawhub.ai/csuwl/butler-mode) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown guidance with tool-specific command and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include task plans, delegation prompts, progress updates, and review feedback for teammate agent sessions.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
