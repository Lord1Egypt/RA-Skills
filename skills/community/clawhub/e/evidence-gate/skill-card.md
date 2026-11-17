## Description:

Generates evidence obligations for a claim or action, evaluates explicit evidence against them, and returns a structured verdict with downgrade guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shanicky](https://clawhub.ai/user/shanicky)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to gate strong claims, diagnoses, safety assertions, or high-impact recommendations with explicit evidence requirements before presenting or acting on them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can auto-activate before strong claims or high-impact recommendations, which may add extra gating or soften wording.

Mitigation: Use the skill when structured evidence checks are desired and tune invocation policy where unnecessary gating would add more cost than value.

## Reference(s):

- [Evidence Gate Skill Page](https://clawhub.ai/shanicky/skills/evidence-gate)
- [Evidence Gate Protocol](references/protocol.md)
- [Evidence Gate Input Template](references/input-template.md)
- [Evidence Gate Output Template](references/output-template.md)
- [Evidence Gate Verdict Schema](references/verdict-schema.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Structured JSON with guidance suitable for Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns PASS, SOFT_PASS, BLOCK, or CONFLICT verdicts with evidence requirements, missing evidence, allowed actions, blocked actions, fallback wording, and next evidence actions.]

## Skill Version(s):

0.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
