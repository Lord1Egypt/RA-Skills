## Description: <br>
Claw Mechanic helps agents diagnose, audit, and repair OpenClaw hosts by identifying failing layers, proposing focused fixes, and verifying live runtime health. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bkf-gitty](https://clawhub.ai/user/bkf-gitty) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, operators, and maintenance agents use this skill to triage OpenClaw host issues across gateway, service, plugin, cron, model, memory, channel, approval, and security layers. It supports focused repair plans and full audits that preserve evidence, avoid broad rewrites, and verify the host after changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may guide an agent toward live OpenClaw host changes, including restarts, plugin updates, cron edits, and configuration repair. <br>
Mitigation: Review and approve proposed live changes before execution, keep repairs targeted to the failing layer, and verify gateway health after the change. <br>
Risk: Diagnostics may encounter secrets, OAuth material, session content, or agent workspace data. <br>
Mitigation: Use redacted probes and metadata first, and require explicit approval before inspecting raw secrets, env files, session bodies, or workspace contents. <br>
Risk: Direct file or database edits can damage host state if supported OpenClaw APIs are available but bypassed. <br>
Mitigation: Back up state first, prefer supported CLI or Gateway RPC paths, and re-read the changed state through OpenClaw after repair. <br>


## Reference(s): <br>
- [Claw Mechanic release page](https://clawhub.ai/bkf-gitty/claw-mechanic) <br>
- [Claw Mechanic Failure Map](references/failure-map.md) <br>
- [Host Profile Template](references/host-profile-template.md) <br>
- [Root Failure Taxonomy](references/root-failure-taxonomy.md) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [OpenClaw CLI documentation](https://docs.openclaw.ai/cli) <br>
- [OpenClaw doctor documentation](https://docs.openclaw.ai/doctor) <br>
- [OpenClaw plugins documentation](https://docs.openclaw.ai/cli/plugins) <br>
- [OpenClaw cron documentation](https://docs.openclaw.ai/cli/cron) <br>
- [OpenClaw models documentation](https://docs.openclaw.ai/cli/models) <br>
- [OpenClaw secrets documentation](https://docs.openclaw.ai/cli/secrets) <br>
- [OpenClaw exec approvals documentation](https://docs.openclaw.ai/tools/exec-approvals) <br>
- [OpenClaw gateway configuration documentation](https://docs.openclaw.ai/gateway/configuration) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured repair plans] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include redacted diagnostics, verification evidence, rollback notes, and next recommended actions.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
