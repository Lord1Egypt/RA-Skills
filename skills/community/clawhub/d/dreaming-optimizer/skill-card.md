## Description: <br>
Optimizes OpenClaw memory entries with scoring, semantic deduplication, fact tagging, persistent commits, and traceable REM summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chongjie-ran](https://clawhub.ai/user/chongjie-ran) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to consolidate daily memory notes by scoring, deduplicating, tagging, committing, archiving, and summarizing entries for long-term memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes and persists long-term memory text that may contain sensitive or private information. <br>
Mitigation: Avoid storing secrets or highly private text in memory notes, and review committed entries, previews, archives, and summaries before regular use. <br>
Risk: The skill can modify local OpenClaw memory storage and archive files. <br>
Mitigation: Back up important memory data before enabling routine optimization cycles. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/chongjie-ran/dreaming-optimizer) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [DESIGN.md](artifact/DESIGN.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands, JSON summaries, Markdown summaries, and local SQLite memory updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes optimized memory entries, archives lower-scoring entries, and produces traceable dreaming summaries in the local OpenClaw workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
