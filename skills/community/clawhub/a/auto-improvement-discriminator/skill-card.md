## Description:

A multi-signal scoring skill for ranking improvement candidates with heuristic rules, optional evaluator evidence, LLM-as-judge semantic review, and multi-reviewer blind panels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanyasheng](https://clawhub.ai/user/lanyasheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill to score and rank proposed skill improvements, run blind-panel or LLM-assisted reviews, and produce accept, hold, or reject recommendations before a separate gate or executor acts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted skill paths or manipulated review data could influence downstream actions.

Mitigation: Use the skill only in an isolated review environment, avoid using it as an automatic approval or execution gate, and sandbox untrusted skill paths without inherited secrets.

Risk: LLM judge backends may disclose confidential artifacts externally.

Mitigation: Use the mock LLM backend for confidential artifacts unless external disclosure is acceptable.

Risk: Human-review receipts may be unauthenticated.

Mitigation: Treat human-review receipts as advisory unless additional signature and reviewer controls are added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lanyasheng/skills/auto-improvement-discriminator)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [JSON, Guidance, Shell commands]

**Output Format:** [Markdown guidance with CLI commands and JSON scoring artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes scores, recommendations, blockers, panel reviews, and optional LLM verdicts.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
