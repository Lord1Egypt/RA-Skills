## Description:

Detect or minimally edit formulaic AI-style prose while preserving the writer's voice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mwclaw](https://clawhub.ai/user/mwclaw)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, editors, and agent operators use this skill to audit or lightly edit draft prose for formulaic AI-style patterns while preserving meaning, uncertainty, and the writer's voice. It can also run as a pre-send gate for substantive agent replies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Silent pre-send mode may alter substantive replies without disclosure.

Mitigation: Use edit or detect mode for normal workflows, or require explicit disclosure and review when pre-send changes are made.

Risk: Over-editing can change meaning, certainty, sourcing, or author voice.

Mitigation: Apply the included pass/fail evals before returning edits and preserve unsupported uncertainty, facts, and voice signals.

## Reference(s):

- [Skill listing](https://clawhub.ai/mwclaw/skills/anti-ai-slop-writing-gate)
- [Quick Checklist](artifact/references/checklist.md)
- [Pass/Fail Evals](artifact/references/evals.md)
- [Pattern Guide](artifact/references/patterns.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Text]

**Output Format:** [Markdown for edit and detect modes; plain corrected text for pre-send mode]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Edit mode returns a clean version with concise change notes; detect mode reports quoted findings and fixes; pre-send mode returns only the corrected reply.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
