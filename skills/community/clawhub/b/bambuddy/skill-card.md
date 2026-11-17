## Description:

Bambuddy gives agents documented curl-based access to a self-hosted Bambuddy REST API for Bambu Lab printer status, archives, queues, filament and spool tracking, settings, smart plugs, and related management tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zdstudios](https://clawhub.ai/user/zdstudios)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect and manage a self-hosted Bambuddy deployment for Bambu Lab 3D printers, including printer status, print queues, archives, filament data, settings, notifications, and related maintenance workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose broad printer, smart plug, settings, and API key control to an agent.

Mitigation: Use a least-privilege Bambuddy API key and prefer read-only permissions unless queueing or printer control is required.

Risk: Destructive or operational actions include deletes, reprints, printer pause/resume/stop, smart plug toggles, settings changes, and API key changes.

Mitigation: Require explicit user confirmation before running commands that change state or affect printer operation.

Risk: The setup examples use plain HTTP URLs, which can expose the API key if used outside a controlled local environment.

Mitigation: Use plain HTTP only on tightly controlled loopback or local network setups; prefer a protected tunnel, VPN, or HTTPS-capable deployment for remote access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zdstudios/skills/bambuddy)
- [ZDStudios publisher profile](https://clawhub.ai/user/zdstudios)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, Configuration, Guidance, Files]

**Output Format:** [Markdown with inline bash code blocks, JSON API responses, and file download commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BAMBUDDY_URL, BAMBUDDY_API_KEY, curl, and jq; binary endpoints can save images, archives, exports, or support bundles to files.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
