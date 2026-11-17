## Description:

Use the Fusion 360 Bridge to inspect or control Autodesk Fusion 360 over HTTP from OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smicbee](https://clawhub.ai/user/smicbee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and CAD automation users use this skill to inspect Fusion 360 state, check bridge health, review logs, and run helper-style or raw Python automation through the Fusion Bridge add-in.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bridge exposes raw Python execution that can modify Fusion documents and affect the host user environment.

Mitigation: Install only from trusted sources, review the add-in/plugin source at a pinned commit, and run the bridge in a tightly controlled environment.

Risk: The bridge may be reachable over the network on TCP port 8765 without sufficient security boundaries.

Mitigation: Prefer localhost-only binding, avoid exposing port 8765 to LAN or public networks, and use host firewall rules to restrict access.

## Reference(s):

- [Fusion 360 Bridge source repository](https://github.com/smicbee/fusion-360-bridge)
- [Fusion Bridge API Reference](artifact/references/api.md)
- [Fusion Bridge Recipes](artifact/references/recipes.md)
- [ClawHub skill page](https://clawhub.ai/smicbee/skills/fusion-bridge)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON request examples, and Python snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Fusion Bridge HTTP requests and Python snippets for execution in a trusted Fusion 360 environment.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
