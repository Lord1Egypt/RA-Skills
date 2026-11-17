## Description:

Route Aqara Open API requests across device, space, and automation skills with a relationship-first router, shared CLI contract, and structured handoff contract.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aqara](https://clawhub.ai/user/aqara)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and smart-home operators use this skill to inspect Aqara devices and spaces, control device traits, and create or manage automations through the Aqara Open API CLI. It is intended for credentialed Aqara environments where live device and automation changes are reviewed before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control physical smart-home devices and create, update, enable, disable, or delete live automations.

Mitigation: Require explicit user confirmation before device-control, batch, status-changing, or delete operations, and verify target devices, spaces, and automation IDs from retrieved evidence before execution.

Risk: Bearer tokens may be sent to any configured endpoint if AQARA_ENDPOINT_URL is wrong or untrusted.

Mitigation: Verify the endpoint is the real Aqara API URL before use, prefer environment variables or a tightly permissioned CLI config, and never print real tokens in chat, logs, or generated files.

Risk: The local device cache can contain sensitive home device, room, and automation context.

Mitigation: Keep local config and cache files tightly permissioned and avoid sharing generated files or logs that expose device identifiers, room membership, or credential-adjacent context.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aqara/skills/aqara-open-api-local)
- [Aqara Open API Deployment Guide](README-CLAWHUB.md)
- [Aqara Open API CLI](README.md)
- [Aqara Open API CLI Commands](docs/commands.md)
- [Automation Configuration Reference](references/automation_config.md)
- [Automation Instance Schema](references/automation-instance-v0.schema.json)
- [Unified Example Index](references/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, and shell command snippets for Aqara CLI workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate automation configuration JSON and Aqara CLI commands that require Node.js, AQARA_ENDPOINT_URL, and AQARA_OPEN_API_TOKEN.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
