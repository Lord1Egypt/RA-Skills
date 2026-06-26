## Description: <br>
Agent Dream gives OpenClaw agents a scheduled local dream cycle that consolidates memory, prunes stale notes safely, and writes self-reflection summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ahaaiclub](https://clawhub.ai/user/ahaaiclub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to help OpenClaw agents periodically review local sessions, consolidate persistent memories, prune stale entries with safeguards, and report what changed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reviews local session transcripts and memory files, which may contain personal or sensitive information. <br>
Mitigation: Install and schedule it only for the workspace and agent where memory consolidation is desired, and inspect dream-config.json after setup. <br>
Risk: Dream runs can update persistent memory files, including MEMORY.md, LEARN.md, topic files, and dream records. <br>
Mitigation: Keep MEMORY.md rewriting disabled if unsure; the skill also documents backups, two-pass stale deletion, and change gates before large rewrites. <br>
Risk: Scheduled unattended runs may preserve incorrect, stale, or overbroad memories. <br>
Mitigation: Review dream notifications, proposed MEMORY.md changes, stale markers, and resurfaced old memories before relying on consolidated memory. <br>


## Reference(s): <br>
- [Memory Types - Classification Guide](references/memory-types.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local memory summaries, dream records, notifications, and setup configuration guidance.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
