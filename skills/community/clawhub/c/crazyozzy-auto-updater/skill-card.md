## Description: <br>
Helps agents configure scheduled OpenClaw and ClawHub update routines that update OpenClaw, update installed skills, and summarize results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[crazyozzy](https://clawhub.ai/user/crazyozzy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to set up recurring OpenClaw maintenance that updates the core toolchain, updates installed ClawHub skills, checks health when needed, and reports concise results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled update jobs may update OpenClaw and installed skills without per-update review. <br>
Mitigation: Use dry-run or notification-first scheduling when practical, keep rollback or backup options available, and make sure the scheduled job can be disabled. <br>
Risk: Forced skill updates can overwrite or conflict with local modifications. <br>
Mitigation: Avoid `clawhub update --all --force` unless local changes have been checked and the user accepts the overwrite risk. <br>
Risk: OpenClaw updates may require follow-up health checks or service recovery. <br>
Mitigation: Run `openclaw doctor` when update output reports configuration or service issues, and summarize any manual follow-up clearly. <br>


## Reference(s): <br>
- [CrazyOzzy Auto Updater ClawHub release page](https://clawhub.ai/crazyozzy/crazyozzy-auto-updater) <br>
- [Agent Implementation Guide](references/agent-guide.md) <br>
- [Update Summary Examples](references/summary-examples.md) <br>
- [Local OpenClaw update documentation](docs/cli/update.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Concise user-facing setup and update-summary text] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
