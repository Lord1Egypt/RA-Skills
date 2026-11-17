## Description:

Tracks foreshadowing in novel manuscripts by identifying hints, surfacing unresolved threads, and recording resolved callbacks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuzhihui886](https://clawhub.ai/user/yuzhihui886)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, and editorial agents use this skill to analyze novel chapters, track unresolved foreshadowing, and generate records or reports that help maintain callbacks across a manuscript.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional LLM helper can send the full selected manuscript file to DashScope.

Mitigation: Use the local tracker for confidential drafts, or obtain approval before running the LLM helper with sensitive manuscript text.

Risk: The tracker can create or overwrite JSON record and report paths.

Mitigation: Review output and record paths before execution, and keep backups or version control for manuscript project files.

Risk: Foreshadowing detection may miss context or produce misleading matches.

Mitigation: Treat generated findings as editorial assistance and review them manually before changing the manuscript plan.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuzhihui886/skills/foreshadowing-tracker)
- [DashScope chat completions endpoint used by the LLM helper](https://coding.dashscope.aliyuncs.com/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown guidance with CLI commands, JSON foreshadowing records, and terminal summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The local tracker can create or overwrite record and report files; the optional LLM helper writes JSON results after sending selected text to DashScope.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
