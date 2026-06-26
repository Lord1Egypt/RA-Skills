## Description: <br>
Audit and maintain OpenClaw-style long-term memory. Use for MEMORY.md cleanup, daily-note digestion, duplicate detection, stale-memory review, and promoting durable facts from memory/YYYY-MM-DD.md into curated memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[orime](https://clawhub.ai/user/orime) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to audit long-term memory files, identify duplicate or stale entries, surface follow-ups, and draft durable memory candidates from recent daily notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Memory files may contain sensitive personal or project information that appears in reports or dedupe output. <br>
Mitigation: Run the skill only in intended workspaces and avoid sharing generated reports or logs unless memory content has been reviewed. <br>
Risk: Digest suggestions may classify temporary notes as durable memory or miss context needed for accurate promotion. <br>
Mitigation: Review all suggestions before editing MEMORY.md and promote only stable facts the user wants retained. <br>
Risk: The skill reads local MEMORY.md and memory/*.md files from the selected root. <br>
Mitigation: Invoke commands from the intended project root and verify the --root path before running audits or digests. <br>


## Reference(s): <br>
- [Agent Memory Ops Playbook](references/playbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown reports or JSON summaries printed to standard output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local memory audit, dedupe, and digest suggestions; it does not mutate files by itself.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
