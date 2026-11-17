## Description:

Designs agent-evaluated flow tests for browser tasks, LLM outputs, and tool workflows. Invoke when exact asserts are brittle and semantic success matters more than literal equality.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qipengguo](https://clawhub.ai/user/qipengguo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design flow tests for browser tasks, LLM outputs, and multi-tool workflows where exact assertions are brittle. It helps them define deterministic checks, evidence to collect, semantic rubrics, and bounded verdicts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A flow test design may browse live sites, call external tools, or collect evidence from private systems.

Mitigation: Review proposed flow tests before running them, limit allowed sources and tools, and avoid private-system evidence collection unless explicitly approved.

Risk: Semantic evaluation can produce an overconfident pass when evidence is incomplete or ambiguous.

Mitigation: Require inspectable evidence, preserve deterministic checks for stable invariants, and use needs_review when evidence is weak or contradictory.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown structured test specification]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes deterministic checks, evidence schema, semantic rubric, execution notes, and a final verdict format using pass, fail, or needs_review.]

## Skill Version(s):

0.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
