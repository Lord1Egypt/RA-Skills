## Description:

Cognitive Bias Adivsor helps users diagnose cognitive biases across decision-making, learning, action, communication, influence, and management, then produces structured assessments, strategy recommendations, and suggested phrasing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jacksu](https://clawhub.ai/user/jacksu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and workplace practitioners use this skill to structure cognitive-bias self-checks and receive practical strategies for decisions, learning, execution, communication, influence, and management. The skill supports reflection and planning, but it does not make decisions for the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A documented install path points to a different package name than the ClawHub release.

Mitigation: Install only the ClawHub package named cognitive-bias-advisor unless the separate package has been independently verified.

Risk: Influence and persuasion modules can produce operational tactics that may be misused in coercive communication.

Mitigation: Use those modules only for transparent, non-harmful communication that respects the other person's autonomy.

Risk: Broad decision, learning, and communication triggers may activate the workflow for loosely related user requests.

Mitigation: Confirm the user's intended domain before applying a diagnostic workflow or generating recommendations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jacksu/skills/cognitive-bias-advisor)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)
- [Decision domain workflow](artifact/references/domain-decision.md)
- [Learning domain workflow](artifact/references/domain-learning.md)
- [Action domain workflow](artifact/references/domain-action.md)
- [Communication domain workflow](artifact/references/domain-communication.md)
- [Influence domain workflow](artifact/references/domain-influence.md)
- [Management domain workflow](artifact/references/domain-management.md)
- [Bias checklists and strategies](artifact/references/checklists-and-strategies.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown reports, option-card prompts, diagnostic summaries, strategy checklists, and suggested phrasing]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language coaching workflow with domain routing and staged diagnostic questions]

## Skill Version(s):

2.10.2 (source: server release metadata; artifact frontmatter reports 2.11.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
