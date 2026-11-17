## Description:

Optimizes OpenClaw memory entries by scoring, deduplicating, tagging, and writing consolidated results to persistent local memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chongjie-ran](https://clawhub.ai/user/chongjie-ran)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to curate daily memory notes into higher-value long-term memory by prioritizing important entries, reducing duplicates, assigning fact/opinion/preference/context tags, and producing traceable consolidation summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads OpenClaw memory notes and writes selected content into long-term local memory.

Mitigation: Install only when this memory access is acceptable, and keep a process for inspecting and deleting committed memories, archives, and summaries.

Risk: Persistent local memory storage has limited controls and local storage safety concerns.

Mitigation: Review storage permissions, restrict agent names, and confirm where SQLite memory, archives, and summaries are written before using the skill with sensitive notes.

Risk: Automated scoring and deduplication can archive, merge, or discard entries that a user may still consider useful.

Mitigation: Review generated summaries and archive output after optimization cycles, especially before relying on the consolidated memory for important work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chongjie-ran/skills/dreaming-optimizer)
- [Skill documentation](artifact/SKILL.md)
- [Technical design](artifact/DESIGN.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Files, JSON, Markdown, Guidance]

**Output Format:** [Shell execution with local SQLite memory writes, archived Markdown files, and JSON or Markdown summary files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses configurable score and deduplication thresholds; writes to OpenClaw memory, archive, and dreaming-summary paths.]

## Skill Version(s):

1.0.0 (source: server release evidence, skill documentation, and config/default_threshold.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
