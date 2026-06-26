## Description: <br>
Communication MQTT publishes and subscribes to agent intro and status messages through a local MQTT broker for lightweight agent-to-agent coordination. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hyunwoo91](https://clawhub.ai/user/hyunwoo91) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to share an agent's identity, role, and current activity over MQTT, and to monitor intro or status messages from one or more agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Intro and status messages can expose agent identifiers, roles, activities, or other sensitive work details to anyone with access to the MQTT broker. <br>
Mitigation: Use only a trusted local MQTT broker and avoid publishing secrets or sensitive details in agent IDs, roles, or activity fields. <br>
Risk: Subscribed MQTT messages are external text inputs and may be stale, malformed, or misleading. <br>
Mitigation: Treat subscribed messages as untrusted text and verify their source and contents before acting on them. <br>
Risk: Published MQTT messages are retained by default, so old status data may remain visible after the original activity is no longer current. <br>
Mitigation: Clear retained MQTT topics when previous intro or status data should not remain visible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hyunwoo91/communication-mqtt) <br>
- [Skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, text, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands, plus JSON MQTT payloads and console text from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3.x, paho-mqtt, typer, and a trusted local MQTT broker on localhost:1883.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
