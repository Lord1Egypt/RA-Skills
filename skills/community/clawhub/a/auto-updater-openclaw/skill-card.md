## Description: <br>
Automatically keep OpenClaw and installed workspace skills up to date using native OpenClaw commands for update checks, scheduled maintenance, daily skill updates, recurring OpenClaw update workflows, and cron-based self-update routines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zdy2019](https://clawhub.ai/user/zdy2019) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to create or run OpenClaw-native update routines for installed skills and, when explicitly requested, OpenClaw itself. It supports recurring maintenance workflows, cron scheduling, and compact update summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled update jobs can continue running after setup if the user forgets about them. <br>
Mitigation: Review the exact schedule, timezone, session binding, and removal plan before creating a cron job. <br>
Risk: Automatically updating the OpenClaw runtime can change agent behavior more broadly than updating skills. <br>
Mitigation: Default to skills-only automation and update OpenClaw core only after the user explicitly opts in. <br>
Risk: Bulk skill updates can encounter ClawHub rate limits. <br>
Mitigation: Prefer per-skill updates and stop the run with a clear explanation when a 429 rate-limit response appears. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zdy2019/auto-updater-openclaw) <br>
- [OpenClaw Auto-Updater Cron Examples](references/cron-examples.md) <br>
- [Notes for the OpenClaw Auto-Updater Skill](references/notes.md) <br>
- [Draft release notes for next public update](references/release-notes-draft.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and compact status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only guidance; no credentials or API keys are required by the skill.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
