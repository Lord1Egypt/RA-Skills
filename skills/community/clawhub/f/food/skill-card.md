## Description:

Your intelligent food system. Absorbs, analyzes, and organizes everything you eat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users use this skill to log meals, nutrition labels, recipes, menus, restaurants, inventory, and food preferences into a local food history, then receive organized food insights and optional nutrition estimates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local food history can contain sensitive allergies, restrictions, eating patterns, restaurants, recipes, and personal routines.

Mitigation: Install only when local food-history persistence is desired, and periodically review and delete entries in ~/food/memory.md that should not be retained.

Risk: Nutrition estimates and food insights may be incomplete or unsuitable for medical decisions.

Mitigation: Treat outputs as informational, keep nutrition estimation optional, and use qualified medical or nutrition guidance for health decisions.

## Reference(s):

- [Food Input Processing](artifact/processing.md)
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/food)
- [Publisher Profile](https://clawhub.ai/user/ivangdavila)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Files]

**Output Format:** [Markdown food-history entries with concise text analysis and guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists food history and preferences locally in ~/food/memory.md; nutrition estimates are optional and not medical advice.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
