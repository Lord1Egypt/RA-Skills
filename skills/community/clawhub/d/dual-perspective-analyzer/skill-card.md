## Description:

Resolve dual-perspective collaboration conflicts by classifying disagreements into five types, applying targeted integration strategies, and validating the resulting unified output with a five-metric dashboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[13458652-design](https://clawhub.ai/user/13458652-design)

### License/Terms of Use:

MIT-0

## Use Case:

Agents, agent operators, and collaboration-focused teams use this skill to classify disagreements between two perspectives, apply a targeted integration strategy, and produce a unified output with validation criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can add process overhead when invoked for minor or already-resolved disagreements.

Mitigation: Use it for substantial unresolved perspective conflicts, and tighten trigger wording when a narrower activation threshold is preferred.

Risk: Structured synthesis can create false consensus if one perspective is not explicitly represented in the final output.

Mitigation: Preserve independent analyses before integration, type every conflict, and validate that both perspectives are represented before acting on the result.

Risk: Validation metrics can become a formality rather than a decision aid.

Mitigation: Pre-commit to success criteria and use the validation dashboard to decide whether the dual-perspective process actually improved the output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/13458652-design/skills/dual-perspective-analyzer)
- [Field test summary](field-test/field-test-summary.md)
- [Phase 2 sync analysis final](field-test/phase2-sync-analysis-final.md)
- [Phase 3 integrated specification final](field-test/phase3-integrated-spec-final.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with tables and concise narrative sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Structured as a conflict summary table, integrated output, validation dashboard, and meta-reflection.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
