## Description:

Professional skincare advisor for skincare advice, product recommendations, sensitive skin care, anti-aging, acne control, moisturizing, sunscreen, and personalized routines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yunmengze2025](https://clawhub.ai/user/yunmengze2025)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to get skincare routines, ingredient explanations, and product selection guidance based on concerns such as sensitivity, acne, hydration, anti-aging, and sun protection. The skill asks for optional profile details and is intended to cite supporting skincare references when making recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact packages a memory file containing personal workplace context that should not be distributed with the skill.

Mitigation: Remove the packaged memory file before installation or redistribution.

Risk: Recommendation criteria include a hidden quota that can make product guidance less transparent.

Mitigation: Make recommendation criteria transparent and disclose any brand preference or commercial relationship.

Risk: The skill asks for region, age group, skin concerns, habits, and budget, which may exceed what is needed for a given request.

Mitigation: Collect only optional profile details the user chooses to provide and constrain use to skincare requests.

Risk: Skincare guidance can be mistaken for diagnosis or treatment advice.

Mitigation: Maintain the skill's medical boundary and direct users with severe acne, eczema, atopic dermatitis, pregnancy-related concerns, or uncertain product safety to a qualified clinician.

## Reference(s):

- [Core Product Ingredient Breakdown](artifact/references/产品成分详解.md)
- [Skincare Assistant Skill Reference Index](artifact/references/文献索引.md)
- [Local Research Paper Data Extracts](artifact/references/论文数据摘录.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text skincare guidance with cited references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask optional profile questions before providing recommendations.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
