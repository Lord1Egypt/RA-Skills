## Description: <br>
Automatically update OpenClaw and all installed skills once daily. Runs via cron, checks for updates, applies them, and messages the user with a summary of what changed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Gitchegumi](https://clawhub.ai/user/Gitchegumi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to configure daily unattended updates for OpenClaw and installed skills, then receive a summary of what changed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unattended daily updates can change OpenClaw or installed skill behavior without per-update review. <br>
Mitigation: Enable the skill only where unattended updates are acceptable, and review the delivered update summaries after each run. <br>
Risk: Restarting the OpenClaw service with elevated privileges can cause downtime or broaden local privilege exposure if configured too broadly. <br>
Mitigation: Restrict any passwordless sudo rule to the exact restart command and confirm how to remove the cron job before enabling it. <br>


## Reference(s): <br>
- [OpenClaw Updating Guide](https://docs.openclaw.ai/cli/update) <br>
- [OpenClaw Cron Jobs](https://docs.openclaw.ai/cron) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces cron setup commands, update commands, troubleshooting guidance, and summary-message examples; it does not execute updates by itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter lists 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
