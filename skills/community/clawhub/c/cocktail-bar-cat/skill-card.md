## Description:

Cocktail Bar Cat helps bartenders and home mixologists explore source-aware cocktail recipes, create and adapt drinks, plan menus, and estimate ingredient costs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[homleeliu-yishe](https://clawhub.ai/user/homleeliu-yishe)

### License/Terms of Use:

MIT-0

## Use Case:

Bartenders and home mixologists use this agent to look up cocktail recipes and history, develop recommendations and menus, adapt drinks, and estimate ingredient and shopping costs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation phrases may cause the agent to engage beyond the user's intended cocktail task.

Mitigation: Review the activation phrases and invoke the skill for cocktail-related requests.

Risk: The scanner flags uncertainty around dataset provenance and pricing consistency.

Mitigation: Check source links and dates, and treat bundled prices as synthetic estimates rather than current market quotes.

Risk: Two data files were only partially inspected, so the security review is incomplete.

Mitigation: Review those files before relying on their contents.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/homleeliu-yishe/skills/cocktail-bar-cat)
- [Project homepage](https://github.com/homleeliu-yishe/cocktail-bar-cat)
- [Recipe and recommendation guidance](artifact/references/recommendation-creation.md)
- [Historical reference guide](artifact/references/history.md)
- [Bar reference guide](artifact/references/bars.md)
- [Operations and cost guidance](artifact/references/operations.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands]

**Output Format:** [Concise prose or Markdown, with recipe and menu suggestions, source-aware history, cost estimates, and optional local query commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bundled prices are synthetic estimates, not market quotes; historical and bar references retain their stated evidence and date limits.]

## Skill Version(s):

2.7.4 (source: SKILL.md frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
