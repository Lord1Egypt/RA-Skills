## Description:

Chinese naming analysis and candidate generation skill that prioritizes favorable-element filtering and uses WuGe as a secondary reference for personal, company, brand, bilingual, stage, screen, online, and pet naming scenarios.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianlinle](https://clawhub.ai/user/tianlinle)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate and evaluate Chinese name candidates by surname, favorable element, pronunciation, meaning, style, and optional San Cai / WuGe structure. It supports personal names as well as company, brand, store, bilingual, stage, screen, online, and pet naming workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill description covers broad naming scenarios, while the scanner summary says the implementation mainly automates Chinese-character name scoring.

Mitigation: Use the local scoring scripts as structured evidence and review final recommendations for fit, cultural nuance, pronunciation, and scenario-specific meaning before presenting them.

Risk: Optional runtime setup may require installing tsx on Node versions below 24.

Mitigation: Prefer Node 24; when tsx is needed, pin and review the dependency before installation.

Risk: Names containing characters missing from the bundled hanzi dataset cause script errors rather than fallback analysis.

Mitigation: Check unsupported characters and either choose candidates from the bundled dataset or explain that the requested character cannot be scored by the skill.

## Reference(s):

- [Cantian AI](https://cantian.ai)
- [Cantian BaZi companion skill](https://clawhub.ai/tianlinle/cantian-bazi)
- [ClawHub skill page](https://clawhub.ai/tianlinle/skills/cantian-naming)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown reports or JSON from local TypeScript scripts, with concise natural-language recommendations for agent responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include candidate names, scores, character attributes, San Cai / WuGe summaries, favorable-element matching, and interpretation guidance.]

## Skill Version(s):

0.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
