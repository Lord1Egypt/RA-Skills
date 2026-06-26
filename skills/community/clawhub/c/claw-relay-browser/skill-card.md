## Description: <br>
Controls a remote browser through Claw Relay using a CLI client for navigation, snapshots, screenshots, clicks, form input, keyboard actions, and page JavaScript evaluation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andreagriffiths11](https://clawhub.ai/user/andreagriffiths11) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when an agent needs controlled access to a user's real browser session through shell commands, especially for authenticated sites where local headless browsing is not suitable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can act inside logged-in browser sessions and expose private page content. <br>
Mitigation: Use strict site allowlists, minimal scopes, and a dedicated browser profile; require explicit approval before submitting forms, purchasing, deleting, publishing, changing account data, or sharing private page content. <br>
Risk: The evaluate action can run arbitrary page JavaScript. <br>
Mitigation: Avoid or disable evaluate unless necessary, grant execute scope only to trusted agents, and review JavaScript before execution. <br>
Risk: Relay credentials authorize browser actions for a specific agent. <br>
Mitigation: Protect relay tokens, use per-agent identities, and rotate or revoke credentials when access changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/andreagriffiths11/claw-relay-browser) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON, Files] <br>
**Output Format:** [Markdown guidance with bash examples; runtime actions return JSON and screenshots can be written as files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Claw Relay URL, token, and agent ID; actions are single-invocation browser operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
