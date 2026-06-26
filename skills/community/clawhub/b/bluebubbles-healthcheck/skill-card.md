## Description: <br>
Diagnoses and auto-heals BlueBubbles to OpenClaw iMessage connectivity when messages stop arriving after a gateway restart, webhook registration breaks, or webhook backoff and stale gateway state need repair. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amzzzzzzz](https://clawhub.ai/user/amzzzzzzz) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to diagnose BlueBubbles webhook connectivity, restart the local OpenClaw gateway when needed, reset stale webhooks, and report whether iMessage delivery has recovered. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Auto-heal can delete existing BlueBubbles webhook settings and re-register a single webhook. <br>
Mitigation: Back up or list current BlueBubbles webhooks first and run heal.sh with --dry-run before applying changes. <br>
Risk: Healing can restart the local OpenClaw gateway and affect in-flight local messaging workflows. <br>
Mitigation: Run healing during an acceptable maintenance window and verify OpenClaw gateway status after completion. <br>
Risk: The BlueBubbles password can be embedded in webhook URLs stored by BlueBubbles or visible in full URL logs. <br>
Mitigation: Use only trusted local BlueBubbles and OpenClaw instances, avoid remote or shared servers, and rotate BB_PASSWORD if a full webhook URL may have leaked. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/amzzzzzzz/bluebubbles-healthcheck) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [BlueBubbles](https://bluebubbles.app) <br>
- [BlueBubbles API Reference](references/bluebubbles-api.md) <br>
- [Troubleshooting Guide](references/troubleshooting.md) <br>
- [BlueBubbles Postman API Documentation](https://documenter.getpostman.com/view/765844/UVR4PVmG) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and terminal-style diagnostic output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include health-check pass/fail status, auto-heal actions taken, dry-run guidance, and manual follow-up steps.] <br>

## Skill Version(s): <br>
0.1.3 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
