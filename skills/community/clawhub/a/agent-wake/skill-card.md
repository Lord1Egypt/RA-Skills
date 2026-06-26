## Description: <br>
Wake an OpenClaw agent session from an external script or process when background work completes and the agent should be notified in the correct Discord channel. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krisco65](https://clawhub.ai/user/krisco65) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to let trusted local scripts, scheduled jobs, webhooks, or CLI tasks wake an OpenClaw agent after asynchronous work completes. It helps route the agent response to the intended Discord channel without manual prompting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Gateway tokens could be exposed if stored carelessly or committed with local configuration. <br>
Mitigation: Keep the gateway token private, avoid committing .env files, and use only trusted local configuration sources. <br>
Risk: Untrusted wake-message text could steer the agent toward unintended actions or disclosure. <br>
Mitigation: Send only trusted, summarized task status in wake messages and do not pass raw webhook content, logs, prompts, or credentials. <br>
Risk: An exposed or broadly enabled gateway could allow unwanted wake events. <br>
Mitigation: Keep the gateway local or access-controlled and enable only the cron tool required by this skill. <br>


## Reference(s): <br>
- [Setup Guide](references/setup.md) <br>
- [ClawHub skill page](https://clawhub.ai/krisco65/agent-wake) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The included Python script sends a wake event through the configured OpenClaw gateway and prints a success or error message.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
