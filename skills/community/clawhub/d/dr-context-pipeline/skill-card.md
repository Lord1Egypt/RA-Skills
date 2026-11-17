## Description:

Deterministic memory/context pipeline with semantic retrieval checks, compression/lint, safe fallback, and memory watchdog.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniel-refahi-ikara](https://clawhub.ai/user/daniel-refahi-ikara)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to standardize how persistent memory is routed, retrieved, compressed, validated, and supplied to an agent, with fallback behavior and optional debug or audit evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Memory workflows can make lasting changes after an ambiguous continuation request.

Mitigation: Require explicit save requests and review proposed changes to standing memory rules.

Risk: Diagnostic output can expose private context.

Mitigation: Redact diagnostics before display or retention, restrict access, and set a deletion period.

Risk: A forced refresh can replace customized skill files.

Mitigation: Back up customized skill files before forced refreshes.

## Reference(s):

- [Apply checklist](references/APPLY.md)
- [Runtime checklist](references/RUNTIME_CHECKLIST.md)
- [Semantic memory assurance](references/SEMANTIC_MEMORY_ASSURANCE.md)
- [ClawHub release page](https://clawhub.ai/daniel-refahi-ikara/skills/dr-context-pipeline)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and structured JSON artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include retrieval evidence and debug or audit artifacts, depending on runtime mode.]

## Skill Version(s):

2.1.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
