## Description:

Autonomous Deep Research helps an agent break down open-ended research questions, retrieve available local or web evidence, synthesize findings, identify gaps, and iterate toward a structured answer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to run iterative research workflows that decompose broad questions, collect available evidence, produce a structured report, and surface unresolved follow-up work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local learning can store research notes or preferences in plaintext.

Mitigation: Do not record secrets or sensitive research material in learned_patterns.json, and review or remove that file before sharing the skill workspace.

Risk: When local RAG or web-fetch helpers are unavailable, research results may fall back to low-confidence heuristic answers.

Mitigation: Review coverage and open_gaps in the generated report, then rerun with appropriate retrieval helpers for claims that need external evidence.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/autonomous-deep-research)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [JSON report containing decomposed questions, findings, a synthesized Markdown answer, coverage, gaps, and next steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local report files and optional plaintext learned-pattern data when its helper is used.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
