## Description:

Deploy a lightweight status API that exposes an OpenClaw bot's runtime health, service connectivity, cron jobs, skills, system metrics, and related operational status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[suspect80](https://clawhub.ai/user/suspect80)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to set up an operator-facing monitoring endpoint or dashboard source for an OpenClaw agent. It helps expose bot health, configured service checks, cron status, installed skills, and host metrics as status JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The status API can expose sensitive OpenClaw runtime, service, skill, and host metric data if reachable by untrusted users.

Mitigation: Run it only as a private operator-facing service, bind it to localhost or protect it behind authentication, and avoid exposing it directly to public networks.

Risk: Persistent service setup can keep the API running beyond an interactive session and broaden exposure if hardening is incomplete.

Mitigation: Use loginctl linger only when necessary, document removal steps, and verify systemd configuration before enabling the service.

Risk: Configurable collectors can perform command, HTTP, and file checks that may reveal or access unnecessary operational data.

Mitigation: Review the configuration before deployment and disable collectors or checks that are not required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/suspect80/skills/bot-status-api-test)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON, INI, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces deployment and configuration guidance for a Node.js status API.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
