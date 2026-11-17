## Description:

Calorie Detective uses Kimi vision recognition and a local nutrition database to estimate calories, protein, carbohydrates, and fat from food photos or manual food descriptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaa2531349](https://clawhub.ai/user/aaa2531349)

### License/Terms of Use:

MIT

## Use Case:

People tracking meals can submit a food image or food description to receive a Chinese nutrition report with estimated calories and macronutrients. The skill is useful for everyday diet awareness, fitness tracking, and meal review, but its output should not be treated as medical or nutrition advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Food photos are sent to the Moonshot/Kimi API and may include private context.

Mitigation: Avoid uploading images with faces, documents, location clues, or other sensitive details; use manual description mode for sensitive meals.

Risk: Nutrition results are estimates and may be wrong because food recognition, portion size, cooking method, and ingredient data can vary.

Mitigation: Use results for general diet awareness only and consult a qualified professional for medical, nutritional, or special-diet decisions.

Risk: Dependency versions are range-based rather than pinned.

Mitigation: Install in a trusted environment and pin reviewed dependency versions before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaa2531349/skills/calorie1)
- [Moonshot chat completions API endpoint](https://api.moonshot.cn/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Chinese Markdown nutrition report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include recognized foods, estimated calories, macronutrients, per-item breakdowns, recognition source, and a reminder that values are estimates.]

## Skill Version(s):

3.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
