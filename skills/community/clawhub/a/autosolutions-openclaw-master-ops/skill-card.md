## Description: <br>
The OpenClaw Master Ops skill helps an agent operate, troubleshoot, secure, automate, and maintain OpenClaw deployments, including release tracking for breaking-change review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[autosolutionsai-didac](https://clawhub.ai/user/autosolutionsai-didac) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and administrators use this skill to set up, run, debug, harden, monitor, and update OpenClaw gateways, channels, agents, sessions, plugins, and release-tracking workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill covers high-privilege OpenClaw administration, including fixes, resets, secret handling, plugin changes, publishing, and scheduled jobs. <br>
Mitigation: Require explicit user approval before running state-changing commands, reading or writing secrets, changing plugins, publishing, resetting state, or adding cron jobs. <br>
Risk: The bundled release tracker uses local paths and can query local OpenClaw state or remote release data. <br>
Mitigation: Review and adapt paths before running the tracker, and avoid exposing credential paths, tokens, or sensitive directory listings in chat or logs. <br>


## Reference(s): <br>
- [Release Tracking Workflow](references/release-tracking.md) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>
- [OpenClaw GitHub Releases API](https://api.github.com/repos/openclaw/openclaw/releases) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline shell commands, JSON snippets, and operational checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose commands that require user approval before modifying OpenClaw configuration, credentials, plugins, schedules, or release-tracking state.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
