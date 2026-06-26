## Description: <br>
Stops your OpenClaw agent from reporting the wrong time by requiring timezone-aware local-time checks before time output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ferrentinomj-dev](https://clawhub.ai/user/ferrentinomj-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to configure an OpenClaw agent with a persistent IANA timezone, answer time questions through a local-time helper script, and reduce UTC-as-local mistakes in scheduling or heartbeat workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup can modify persistent agent instruction files by patching AGENTS.md. <br>
Mitigation: Inspect the generated Timezone Standing Order block before relying on it, and remove that block if the skill is uninstalled or persistent timezone steering is no longer desired. <br>
Risk: Timezone configuration can be wrong if the user supplies an invalid or unintended timezone. <br>
Mitigation: Use a valid IANA timezone string, verify tz_config.json after setup, and run now.py to confirm the displayed local time. <br>
Risk: The skill does not automatically intercept every time-related response. <br>
Mitigation: Ensure the agent explicitly runs now.py before reporting times and rerun timezone_setup.py when the user's timezone changes. <br>


## Reference(s): <br>
- [Timezone Conversion Rules & Edge Cases](references/timezone_rules.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/ferrentinomj-dev/agent-timezone-lock) <br>
- [Publisher Profile](https://clawhub.ai/user/ferrentinomj-dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and text output from Python helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write tz_config.json and patch AGENTS.md when setup is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
