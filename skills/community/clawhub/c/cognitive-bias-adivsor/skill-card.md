## Description:

Chinese-language agent skill that routes decision, learning, action, communication, influence, and management questions into cognitive-bias self-checks, diagnostic reports, and strategy templates based on Munger-style psychology and classic cognitive-bias concepts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jacksu](https://clawhub.ai/user/jacksu)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this Chinese-language skill to structure cognitive-bias self-checks before everyday decisions, learning plans, action follow-through, communication, influence work, and team management. It helps an agent ask guided questions and return bias signals, practical mitigation strategies, and reusable wording templates without making decisions for the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger phrases may activate the coaching workflow during ordinary conversations.

Mitigation: Confirm the user's selected domain before routing and let the user decline or restart the workflow.

Risk: Communication and influence sections include persuasion tactics that could be misused.

Mitigation: Use the tactics only transparently and follow the skill's non-harm, transparency, and two-way self-check rules.

Risk: Users may over-rely on cognitive-bias coaching for medical, legal, financial, or other licensed professional advice.

Mitigation: Present outputs as thinking support and recommend qualified professional advice for high-stakes or regulated decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jacksu/skills/cognitive-bias-adivsor)
- [README](README.md)
- [Skill definition](SKILL.md)
- [Decision domain workflow](references/domain-decision.md)
- [Learning domain workflow](references/domain-learning.md)
- [Action domain workflow](references/domain-action.md)
- [Communication domain workflow](references/domain-communication.md)
- [Influence domain workflow](references/domain-influence.md)
- [Management domain workflow](references/domain-management.md)
- [Doubt-avoidance tendency reference](references/bias-doubt-avoidance.md)
- [Inconsistency-avoidance tendency reference](references/bias-inconsistency-avoidance.md)
- [Liking/loving tendency reference](references/bias-liking-tendency.md)
- [Curiosity tendency reference](references/bias-curiosity-tendency.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown diagnostic cards, guided questions, bias-signal summaries, strategy lists, and wording templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language coaching output; no code execution, data access, persistence, or exfiltration behavior identified in server security evidence.]

## Skill Version(s):

2.1.3 (source: server release evidence; artifact frontmatter reports 2.9.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
