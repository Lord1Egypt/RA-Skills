## Description: <br>
Deprecated OpenClaw memory-consolidation skill that reads local memory logs, updates long-term memory files, scores memory health, and can generate a memory dashboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fortunateadventurer](https://clawhub.ai/user/fortunateadventurer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users and developers use this retired skill to consolidate local interaction logs into MEMORY.md, maintain memory/index.json, archive stale entries, and produce memory health reports. OpenClaw 2026.4.5+ users should prefer the built-in /dreaming feature. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local memory logs and rewrites long-term memory files that may contain sensitive information. <br>
Mitigation: Review the memory directory for sensitive content before enabling the skill or any daily scheduler. <br>
Risk: The release is retired and no longer maintained. <br>
Mitigation: Prefer the official OpenClaw /dreaming feature when using OpenClaw 2026.4.5 or later. <br>
Risk: Scheduled runs can change MEMORY.md and related memory files without an interactive review step. <br>
Mitigation: Run the skill manually first, inspect the generated changes, and keep backups enabled before using recurring automation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fortunateadventurer/claws-dream) <br>
- [Nightly Dream - Memory Consolidation Prompt](references/dream-prompt.md) <br>
- [First Dream - Initial Memory Setup](references/first-dream-prompt.md) <br>
- [Dream Consolidation Prompts](references/dream-prompts.md) <br>
- [Scoring & Health - Memory Evaluation Algorithms](references/scoring.md) <br>
- [Memory Taxonomy](references/memory-types.md) <br>
- [Memory Templates](references/memory-template.md) <br>
- [Memory Dashboard Template](references/dashboard-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON snippets, and generated local files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write MEMORY.md, memory/index.json, memory/archive.md, memory/dream-log.md, memory/dashboard.html, logs, and backups in the OpenClaw workspace.] <br>

## Skill Version(s): <br>
2.2.2 (source: server release evidence and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
