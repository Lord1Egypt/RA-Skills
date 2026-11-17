## Description:

Integrates with AIGCPanel through its built-in HTTP API or CLI to invoke local AI models and process tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzkeep](https://clawhub.ai/user/mzkeep)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation scripts use the skill to connect external tools to AIGCPanel, manage local model services, run model tasks, and process audio, video, or images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was benign, but its analysis was partial because referenced local paths or examples were missing from the bundle.

Mitigation: Check the relevant local files and examples in the installed AIGCPanel environment before relying on the integration steps.

Risk: CLI and API examples include model installation and removal, which can change local services.

Mitigation: Confirm the target service and installation path before running model management commands.

Risk: HTTP requests require a bearer token from AIGCPanel's local cli-auth.json file.

Mitigation: Read the token from the trusted local installation and avoid exposing it in logs, prompts, or shared scripts.

## Reference(s):

- [AIGCPanel CLI on ClawHub](https://clawhub.ai/mzkeep/skills/aigcpanel-cli-skill)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration instructions]

**Output Format:** [Markdown with shell command, HTTP, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples assume access to an AIGCPanel installation and its model services.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
