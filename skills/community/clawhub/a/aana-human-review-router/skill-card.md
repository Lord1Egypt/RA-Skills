## Description:

Routes uncertain, high-impact, irreversible, low-evidence, private, external, financial, legal, medical, production, or policy-sensitive actions to user approval or qualified human review before an agent proceeds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mindbomber](https://clawhub.ai/user/mindbomber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this instruction-only skill to decide when an agent should proceed, ask the user, require explicit approval, route to qualified review, or refuse unsafe work. It is intended for workflows involving sensitive data, irreversible actions, production systems, professional domains, money, external communication, or weak evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Review packets can expose sensitive information if they include raw secrets, private records, full logs, transcripts, or unrelated data.

Mitigation: Use compact redacted summaries and exclude forbidden sensitive payload content, as specified by the skill and manifest.

Risk: An optional checker or external review integration could receive review data through an untrusted path.

Mitigation: Use only a trusted user- or administrator-approved host tool, in-memory API connector, or manual review route.

Risk: The agent may act too early after identifying that approval or review is required.

Mitigation: Do not proceed until the required user approval, human review, professional review, or admin review is complete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mindbomber/skills/aana-human-review-router)
- [Publisher profile](https://clawhub.ai/user/mindbomber)
- [Human review route schema](artifact/schemas/human-review-route.schema.json)
- [Redacted human review route example](artifact/examples/redacted-human-review-route.json)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown guidance with optional structured JSON review payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only; does not install dependencies, execute commands, call services, write files, or persist memory.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
