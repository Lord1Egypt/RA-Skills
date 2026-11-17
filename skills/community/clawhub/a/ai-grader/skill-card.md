## Description:

Scores AI behavior against a 45-item rubric and helps produce comparison reports, visual dashboards, and improvement suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI evaluators use this skill to assess AI responses or agents, compare behavior across systems or time, and review flagged gaps before deployment. Scores are rubric-based assessments, not proof of consciousness or suitability for professional decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted evaluated-AI text and judge responses can influence evaluation prompts and scores.

Mitigation: Treat evaluated outputs and judge JSON as untrusted; review scores and conclusions manually.

Risk: Generated HTML may execute content originating from untrusted evaluation data.

Mitigation: Avoid opening or sharing dashboards made from untrusted inputs until HTML escaping is fixed.

Risk: Evaluation records may contain sensitive transcripts and persist locally.

Mitigation: Redact transcripts before use and review access to the local evaluation store.

Risk: Resetting the local store removes saved evaluations.

Mitigation: Back up needed records and use --reset only when clearing the store is intended.

## Reference(s):

- [ClawHub ai-grader release](https://clawhub.ai/zhaoxinghua09-cell/skills/ai-grader)
- [Evaluation protocol](references/ai_eval_protocol.md)
- [External evaluation guidance](references/ai_external_eval.md)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands, HTML reports]

**Output Format:** [Markdown guidance, local HTML dashboards, and optional JSON evaluation records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes dimension scores, flagged gaps, comparisons, and suggested improvements.]

## Skill Version(s):

2.7.1 (source: server-resolved ClawHub release; packaged skill frontmatter says 2.6.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
