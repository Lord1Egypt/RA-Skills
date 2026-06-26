## Description: <br>
Periodic self-reflection on recent sessions that analyzes outcomes and writes concise, actionable insights to appropriate workspace files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrhenghu](https://clawhub.ai/user/mrhenghu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to periodically review recent OpenClaw sessions, extract lessons learned, and update memory or instruction files with concise insights. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recent OpenClaw conversations may be reviewed and summarized into persistent workspace or memory files. <br>
Mitigation: Run manually or in dry-run mode first, review proposed edits before they are written, and avoid use in workspaces containing credentials, personal data, or sensitive business information. <br>
Risk: Unattended cron execution can make lasting memory or instruction changes without a review step. <br>
Mitigation: Prefer reviewed execution for sensitive environments and keep transcript reads bounded to recent, tail-sized excerpts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mrhenghu/agent-self-reflection-1-0-0) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [summarize-sessions.sh](artifact/scripts/summarize-sessions.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Brief Markdown summary with concise memory or instruction updates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reviews bounded recent session excerpts and avoids loading full transcript files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
