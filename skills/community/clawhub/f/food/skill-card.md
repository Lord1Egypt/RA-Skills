## Description: <br>
Your intelligent food system. Absorbs, analyzes, and organizes everything you eat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to log meals, products, recipes, restaurants, preferences, and dietary restrictions, then receive organized food-history insights and optional nutrition estimates. It is not medical advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores meals, products, places, recipes, patterns, and dietary restrictions locally, including potentially sensitive allergy or avoidance information. <br>
Mitigation: Install only if persistent local food tracking is desired, and review or delete ~/food/memory.md when that data should no longer be retained. <br>
Risk: Nutrition estimates and food-pattern insights may be incomplete or unsuitable for medical decisions. <br>
Mitigation: Treat outputs as informational food-journal guidance and not as medical advice. <br>


## Reference(s): <br>
- [Food Input Processing](processing.md) <br>
- [ClawHub Food Tracker release page](https://clawhub.ai/ivangdavila/food) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown food journal entries, classifications, tags, summaries, and optional nutrition or meal-planning guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists food history and preferences in ~/food/memory.md.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
