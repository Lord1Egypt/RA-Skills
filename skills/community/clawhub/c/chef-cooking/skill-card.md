## Description:

AI 智能家庭厨助 helps users recommend recipes from available ingredients or preferences, generate cooking steps, suggest ingredient substitutions, plan multi-day meals, answer cooking questions, provide kitchen safety guidance, and create card-style HTML reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

Home cooks and agents assisting them use this skill to turn ingredients, dish names, or dietary preferences into recipe recommendations, guided steps, substitutions, meal plans, cooking tips, safety notes, and HTML recipe reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cooking questions can trigger online lookup behavior.

Mitigation: Review network access expectations before installation and disable or avoid online fallback where offline-only behavior is required.

Risk: Generated HTML reports may persist and may not safely escape dynamic recipe, query, or plan content.

Mitigation: Treat generated reports as untrusted, open them only from trusted inputs, and sanitize dynamic content before sharing or publishing reports.

Risk: Food safety guidance may be inconsistent for higher-risk topics such as raw seafood or home fermentation.

Mitigation: Use authoritative food-safety sources for high-risk preparations and review safety notes before following or sharing generated guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bettermen/skills/chef-cooking)
- [Project homepage](https://github.com/bettermen/chef-cooking)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance, Files]

**Output Format:** [Markdown or text summaries, optional JSON, and generated HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create persistent HTML report files from recipe, menu, or tips data.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
