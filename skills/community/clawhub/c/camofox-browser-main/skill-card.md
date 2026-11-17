## Description:

Use the main local camofox-browser service for standard browser automation in this workspace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lotfinity](https://clawhub.ai/user/lotfinity)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace agents use this skill to route browser automation tasks to the main local Camofox service at 127.0.0.1:9377, including health checks, tab reuse, actions, and post-action snapshots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser automation can click, type, navigate, and affect active browser sessions through the local service.

Mitigation: Install and use this skill only where user-directed browser actions through 127.0.0.1:9377 are acceptable; check /health, send userId, prefer sessionKey, and re-snapshot after state-changing actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lotfinity/skills/camofox-browser-main)
- [Local Camofox browser service endpoint](http://127.0.0.1:9377)

## Skill Output:

**Output Type(s):** [Guidance, API Calls]

**Output Format:** [Markdown guidance with ordered steps and routing rules]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires userId on requests, prefers sessionKey when creating or reusing tabs, and calls for a fresh snapshot after state-changing browser actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
