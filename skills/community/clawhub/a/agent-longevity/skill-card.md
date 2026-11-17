## Description:

Agent Longevity helps long-running autonomous agents audit output repetition, value contamination, decision logs, memory bloat, and perception scheduling using documented patterns and local scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[citriac](https://clawhub.ai/user/citriac)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to inspect degradation modes in long-running autonomous agents, including repetitive output, circular preference claims, unbounded memory, and wasteful perception loops. It provides audit scripts and operational guidance for deciding what to measure, log, compress, and review externally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent plain-text memory can capture secrets, API keys, precise locations, or private personal and family information.

Mitigation: Keep sensitive data out of MEMORY.md, USER.md, FAMILY.md, and raw logs unless consent, redaction, retention, and file-permission controls are added.

Risk: Audit scripts inspect local files and the decision logger writes local JSONL records.

Mitigation: Run the scripts only on files intended for inspection and set AGENT_DATA_DIR deliberately before logging decisions.

## Reference(s):

- [Agent Longevity on ClawHub](https://clawhub.ai/citriac/skills/agent-longevity)
- [anti_homogenization.md](references/anti_homogenization.md)
- [memory_architecture.md](references/memory_architecture.md)
- [perception_scheduling.md](references/perception_scheduling.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with Python script outputs and JSONL log files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts read supplied text or JSONL files and may write local decision logs under AGENT_DATA_DIR or ./data.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
