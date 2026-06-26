## Description: <br>
Structured task snapshot and automatic post-compaction recovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[obekt](https://clawhub.ai/user/obekt) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and coding agents use Big Memory to capture structured task state before context compaction and recover the latest task snapshot afterward. It is intended for long multi-step sessions where exact files, decisions, code context, blockers, and next steps need to survive context loss. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Durable task snapshots can retain sensitive project context, secrets, or personal data if users include them. <br>
Mitigation: Review memory files periodically and avoid storing secrets or personal data in snapshots. <br>
Risk: Automatic or broad memory indexing can expand the amount of session context retained or searched. <br>
Mitigation: Prefer explicit /big-memory commands for control and use caution before enabling session transcript indexing or cloud embedding search. <br>


## Reference(s): <br>
- [Task Snapshot Template](references/TASK-SNAPSHOT.md) <br>
- [Recommended OpenClaw Configuration](references/openclaw-config.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/obekt/big-memory) <br>
- [Homepage](https://github.com/obekt/big-memory) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown task snapshots, concise recovery summaries, and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces structured local task snapshots and recovery guidance without external dependencies.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
