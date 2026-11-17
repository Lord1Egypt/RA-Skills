## Description:

Operate and troubleshoot the OpenClaw Control UI: navigate connected clients, organize sessions, build session dashboards, and handle direct or Tailscale-hosted Gateways.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to navigate OpenClaw Control UI clients, manage sessions, build and verify dashboards, and troubleshoot direct or remotely hosted Gateways.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security analysis was partial because two local path-like references could not be resolved, so its benign verdict has medium confidence.

Mitigation: Review the skill and its references before use, and confirm that referenced material is available and understood.

Risk: Screen commands can affect every connected Control UI client that supports them, and incorrect remote hosting or sandbox routing can expose sensitive content or leave widgets unavailable.

Mitigation: Confirm the target session and connected-client scope before making changes; follow the two-origin hosting guidance and verify the rendered widget.

## Reference(s):

- [Dashboard operations](artifact/references/dashboards.md)
- [Control UI hosting paths](artifact/references/hosting.md)
- [ClawHub release page](https://clawhub.ai/hillstreet-ph/skills/control-ui)

## Skill Output:

**Output Type(s):** [Guidance, API calls, Code, Configuration instructions]

**Output Format:** [Tool instructions and calls, Markdown guidance, and HTML/SVG widget content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
