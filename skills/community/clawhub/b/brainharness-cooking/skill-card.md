## Description:

Helps home cooks choose a dish from cravings or available ingredients and prepare it with practical recipe and technique guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zning1994](https://clawhub.ai/user/zning1994)

### License/Terms of Use:

MIT

## Use Case:

Home cooks and other users can get a practical dish recommendation, a recipe based on ingredients they have, or help fixing a cooking technique, with a focus on Chinese home cooking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests file-writing, file-editing, and shell-command permissions that cooking advice does not need.

Mitigation: Review and pin the release before installation; remove Write, Edit, and Bash permissions unless explicitly needed.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/zning1994/skills/brainharness-cooking)
- [Project homepage (listed in skill metadata)](https://github.com/zning1994/brainharness-cooking)
- [Cooking framework](artifact/references/cooking-framework.md)
- [Cooking techniques](artifact/references/techniques.md)
- [Dish coverage](artifact/references/dish-coverage.md)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dish recommendations or recipes with ingredients, ordered steps, doneness cues, failure points, and substitutions when useful.]

## Skill Version(s):

0.2.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
