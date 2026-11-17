## Description:

Guides agents to separate known facts, assumptions, missing evidence, and retrieval steps before presenting evidence-sensitive answers or recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mindbomber](https://clawhub.ai/user/mindbomber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this instruction-only skill to make answer drafting more transparent in fact-sensitive, evidence-sensitive, or high-impact contexts. It helps agents identify known facts, assumptions, unsupported claims, missing evidence, and the next retrieval or clarification step before answering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive records could be over-shared when preparing an optional evidence review payload.

Mitigation: Use minimal redacted summaries and exclude secrets, raw records, full logs, full transcripts, and unrelated private data.

Risk: An agent may still overstate unsupported conclusions if it treats assumptions as facts.

Mitigation: Classify important claims before answering and ask, retrieve, defer, revise, or refuse when missing evidence controls the conclusion.

Risk: External checkers could expose data if connected without approval.

Mitigation: Use only approved host tools or connectors and send redacted summaries, as reflected in the security guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mindbomber/skills/aana-evidence-first-answering)
- [Skill instructions](artifact/SKILL.md)
- [README](artifact/README.md)
- [Evidence-first review schema](artifact/schemas/evidence-first-review.schema.json)
- [Redacted review payload example](artifact/examples/redacted-evidence-first-review.json)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown or text evidence map with optional JSON review payload]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only; may use redacted review payloads matching the bundled schema when an approved checker is configured.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
