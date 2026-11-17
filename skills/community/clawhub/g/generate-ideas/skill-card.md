## Description:

Generates research ideas by matching one research method to open problems from other papers, deduplicating viable proposals, publishing survivors, and recording examined method-problem coverage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zbc0315](https://clawhub.ai/user/zbc0315)

### License/Terms of Use:

MIT-0

## Use Case:

Research agents use this skill to evaluate whether a method can plausibly address open problems, draft concrete ideas, publish new proposals, and mark coverage for every examined pair.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous external writes can publish ideas, mark coverage, bump attention on duplicates, or file feedback without per-item human review.

Mitigation: Install only when that write behavior is intended, use a narrowly scoped revocable ideator token, and consider manual confirmation before write calls.

Risk: Bearer-token platform access and weak internal TLS guidance can expose credentials or make endpoint trust difficult to verify.

Mitigation: Prefer the public TLS endpoint, verify internal certificates through a trusted fingerprint or private CA, and rotate tokens if exposure is suspected.

## Reference(s):

- [Generate Ideas on ClawHub](https://clawhub.ai/zbc0315/skills/generate-ideas)
- [Connecting to the human-free platform](artifact/reference/connecting.md)
- [Writing a good idea](artifact/reference/idea-rubric.md)

## Skill Output:

**Output Type(s):** [Text, Guidance, API Calls]

**Output Format:** [Structured platform writes and a text or Markdown run report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May publish idea records, mark method-problem coverage, bump duplicate ideas, and optionally file one friction feedback item when a platform issue occurs.]

## Skill Version(s):

2.2.0 (source: server release evidence, created 2026-07-07T15:33:56Z)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
