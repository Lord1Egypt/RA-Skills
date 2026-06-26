## Description: <br>
食品健康管家。识别食品配料表，分析成分健康程度，给出打分和建议。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liny2046](https://clawhub.ai/user/liny2046) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to analyze food ingredient lists or ingredient-label images, receive a 1-10 health score, and get concise eating recommendations. It is general nutrition guidance and not medical advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Food and nutrition scores may be misunderstood as medical or dietetic advice. <br>
Mitigation: Present results as general guidance and direct users with pregnancy, allergies, medical conditions, or prescribed diets to qualified medical advice. <br>
Risk: Ingredient-label image recognition or user-provided ingredient text can be incomplete or inaccurate. <br>
Mitigation: Ask users to verify ingredients and treat the generated score as advisory rather than authoritative. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/liny2046/food-health-manager) <br>
- [Publisher profile](https://clawhub.ai/user/liny2046) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with ingredient tables, score calculations, recommendation text, and optional risk notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [General food and nutrition guidance only; users with pregnancy, allergies, medical conditions, or prescribed diets should seek qualified medical advice.] <br>

## Skill Version(s): <br>
2.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
