## Description:

Control Ecovacs Deebot vacuums via the IoT API and a gateway using a user-provided Open Platform Access Key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ecovacs-ai](https://clawhub.ai/user/ecovacs-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, operators, and integrators use this skill to let an agent list Ecovacs Deebot robots, check battery and status, and issue supported cleaning or charging commands through an Open Platform AK and gateway.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An exposed Ecovacs Open Platform AK can control the user's Ecovacs robots.

Mitigation: Use a trusted HTTPS Ecovacs gateway or trusted self-hosted gateway, avoid placing the AK in chat, shell history, or URLs, protect or avoid ~/.ecovacs_session.json, and rotate the AK if it may have been exposed.

Risk: Robot-control commands affect physical devices and may fail or behave differently by model, firmware, battery state, region, or connectivity.

Mitigation: Confirm the target nickname, account region, command intent, and returned gateway response before relying on the result; review model-specific support and common error codes when a command fails.

## Reference(s):

- [Skill instructions](SKILL.md)
- [README](README.md)
- [Ecovacs Deebot Control API Reference](references/api.md)
- [Agent internal implementation reference](references/agent-internal.md)
- [Ecovacs Open Platform China](https://open.ecovacs.cn/)
- [Ecovacs Open Platform Global](https://open.ecovacs.com/)
- [ClawHub skill page](https://clawhub.ai/ecovacs-ai/skills/ecovacs-skills-deebot-control)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash, curl, Python CLI commands, and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided Ecovacs Open Platform AK and a matching regional gateway; behavior depends on robot model, firmware, account region, battery level, and online status.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
