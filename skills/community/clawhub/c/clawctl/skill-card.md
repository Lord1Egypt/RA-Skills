## Description: <br>
Coordination layer for OpenClaw agent fleets (tasks, messaging, activity feed, dashboard). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lludlow](https://clawhub.ai/user/lludlow) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use Clawctl to coordinate OpenClaw agent fleets through shared task tracking, inter-agent messaging, fleet presence, activity review, and an optional dashboard. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional dashboard exposes task-changing controls over the network using a long-lived token in URLs. <br>
Mitigation: Keep the dashboard on localhost or a private network, treat dashboard URLs as secrets, and avoid sharing them through terminals, logs, screenshots, or browser history. <br>
Risk: The shared coordination database and dashboard token can affect task state for the whole fleet if exposed to untrusted agents or local users. <br>
Mitigation: Use the skill only with trusted agent fleets and trusted local users, and do not expose the database path or token to untrusted terminals, logs, browsers, or network peers. <br>


## Reference(s): <br>
- [Clawctl on ClawHub](https://clawhub.ai/lludlow/clawctl) <br>
- [lludlow publisher profile](https://clawhub.ai/user/lludlow) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown instructions with CLI commands and terminal output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the clawctl binary; uses CLAW_AGENT for agent identity and CLAW_DB for the local SQLite database path.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
