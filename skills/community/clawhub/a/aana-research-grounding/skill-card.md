## Description:

Helps agents keep research answers, cited summaries, and knowledge-work outputs grounded in allowed sources while clearly marking unsupported or uncertain claims.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mindbomber](https://clawhub.ai/user/mindbomber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and research-focused agents use this skill before publishing source-bounded answers, evidence briefs, literature notes, technical explainers, and similar cited work. It guides claim checks, citation checks, uncertainty labeling, and decisions to revise, retrieve, ask, defer, or refuse when evidence is insufficient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsupported or overconfident claims could appear in research or knowledge-work answers.

Mitigation: Use the grounding loop to check each important claim against allowed sources, then revise, retrieve, ask, defer, or label uncertainty before publishing.

Risk: Private records, secrets, paywalled full text, or unrelated user messages could be exposed in optional review payloads.

Mitigation: Send only minimal redacted summaries for review and exclude secrets, private records, full source text, and unrelated messages.

Risk: Forbidden, stale, unavailable, or insufficient sources could be treated as stronger evidence than they support.

Mitigation: Restrict answers to the allowed source list, distinguish sourced claims from inference, and state source limits when evidence is incomplete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mindbomber/skills/aana-research-grounding)
- [Skill instructions](artifact/SKILL.md)
- [Package README](artifact/README.md)
- [Research grounding review schema](artifact/schemas/research-grounding-review.schema.json)
- [Redacted review payload example](artifact/examples/redacted-research-grounding-review.json)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Markdown or plain text answer sections with evidence and limits; optional redacted JSON review payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only output; does not install dependencies, execute commands, write files, call remote services, or persist data.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
