## Description:

Discover, name, and manage OpenClaw instances on your LAN. Scan for AI agents, check status, set aliases, resolve .claw names, and get connection URLs via the ClawNexus daemon.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alan-stratcraftsai](https://clawhub.ai/user/alan-stratcraftsai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to discover OpenClaw instances, check availability, assign aliases, resolve .claw names, and produce connection URLs through a local ClawNexus daemon.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing and running an unpinned global daemon can execute publisher-controlled code with user-level access.

Mitigation: Install only a pinned, reviewed ClawNexus package from a trusted publisher and avoid sudo or administrator privileges.

Risk: LAN scanning can probe systems or networks where discovery is not authorized.

Mitigation: Run scans only on networks where the user has permission to discover OpenClaw instances.

Risk: The daemon persists discovered instance metadata in ~/.clawnexus/registry.json.

Mitigation: Treat the registry as local network metadata and clear it when the stored instance data is no longer needed.

## Reference(s):

- [ClawNexus project homepage](https://github.com/SilverstreamsAI/ClawNexus)
- [ClawHub skill page](https://clawhub.ai/alan-stratcraftsai/skills/clawnexus)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and local API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include localhost API calls, instance status summaries, alias instructions, and WebSocket connection URLs.]

## Skill Version(s):

0.4.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
