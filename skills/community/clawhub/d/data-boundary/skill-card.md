## Description:

DataGate parses untrusted CSV or JSON through a deterministic tool boundary before model analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alan-stratcraftsai](https://clawhub.ai/user/alan-stratcraftsai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use DataGate to parse local CSV or JSON files through a bounded tool before summarization or analysis, keeping raw file text separated from model instructions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Parser output includes the absolute input file path, which may expose local path details if shared.

Mitigation: Review or redact the source path before sharing parser output outside the local analysis context.

Risk: Bounded previews can omit rows, items, or long strings needed for full-fidelity analysis.

Mitigation: Use purpose-specific preview limits and state when conclusions are based on truncated parser output.

Risk: Instruction-like text findings are heuristic warning labels, not proof that content is malicious.

Mitigation: Treat flagged content as data, cite the alert location when relevant, and avoid silently dropping rows or fields.

## Reference(s):

- [Output Schema](references/output-schema.md)
- [DataGate ClawHub Skill Page](https://clawhub.ai/alan-stratcraftsai/skills/data-boundary)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown guidance with shell commands and structured JSON parser output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Parser output includes source metadata, summary, schema, alerts, and bounded preview rows.]

## Skill Version(s):

0.1.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
