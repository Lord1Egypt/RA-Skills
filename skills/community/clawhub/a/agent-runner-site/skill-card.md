## Description:

Creates a minimal browser-based OpenClaw agent runner page where users can provide an API key, base URL, model, prompt, and view agent output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pmuhammadagus-byte](https://clawhub.ai/user/pmuhammadagus-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical users use this skill to scaffold or specify a lightweight static web UI for running an OpenClaw agent through user-supplied Gateway configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser-based API key handling can expose credentials if keys are stored or displayed carelessly.

Mitigation: Keep keys in memory by default, make localStorage persistence strictly opt-in, and never log or render the key in page text.

Risk: Generated files may overwrite existing files in the chosen output directory.

Mitigation: Run the scaffold script in a new empty output directory and review generated files before adapting them.

Risk: Gateway REST or WebSocket endpoints may differ across OpenClaw deployments.

Mitigation: Confirm the target Gateway endpoints before adding live calls, then validate with a harmless request before running an agent.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance and generated static-site files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May scaffold index.html, style.css, and app.js into a user-selected output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
