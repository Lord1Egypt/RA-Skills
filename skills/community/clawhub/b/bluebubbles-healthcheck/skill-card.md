## Description:

Diagnoses and auto-heals BlueBubbles and OpenClaw iMessage connectivity by running targeted checks and repairing common webhook, backoff, and gateway issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amzzzzzzz](https://clawhub.ai/user/amzzzzzzz)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw operators use this skill to diagnose and repair BlueBubbles webhook delivery problems when iMessages stop flowing after gateway restarts, stale webhook registration, or webhook backoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The repair path can delete existing BlueBubbles webhook settings.

Mitigation: Run diagnose.sh first, use heal.sh --dry-run when possible, and avoid running repairs on servers with other webhook integrations unless replacing webhook configuration is acceptable.

Risk: Password-bearing webhook URLs can expose BB_PASSWORD in logs, transcripts, or copied output.

Mitigation: Use trusted local runs, avoid sharing command transcripts with secrets, and rotate BB_PASSWORD if prior output may have exposed the password.

Risk: Remote BB_URL or OPENCLAW_WEBHOOK_URL values can send credentials or callbacks outside the intended local setup.

Mitigation: Use the localhost defaults for normal operation and do not point the scripts at remote BlueBubbles or webhook services.

Risk: Auto-healing can restart the OpenClaw gateway and disrupt active message handling.

Mitigation: Review diagnostic output before repair and run disruptive fixes during an acceptable maintenance window.

## Reference(s):

- [BlueBubbles API Reference](references/bluebubbles-api.md)
- [Troubleshooting Guide](references/troubleshooting.md)
- [BlueBubbles API Documentation](https://documenter.getpostman.com/view/765844/UVR4PVmG)
- [OpenClaw](https://openclaw.ai)
- [BlueBubbles](https://bluebubbles.app)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON diagnostic output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs health status, repair recommendations, command results, and exit status from local diagnostic and healing scripts.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
