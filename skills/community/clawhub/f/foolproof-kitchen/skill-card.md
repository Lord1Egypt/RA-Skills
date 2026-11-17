## Description:

Foolproof Kitchen generates quick, healthy daily meal plans and beginner-friendly recipe instructions from a user's body metrics, dietary goal, available ingredients, seasonings, and cooking tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mayabts](https://clawhub.ai/user/mayabts)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to turn personal nutrition context and pantry inventory into a same-day breakfast, lunch, dinner, and snack plan with fast recipe steps. It is aimed at kitchen beginners, busy solo diners, and people pursuing fat-loss, maintenance, or muscle-gain meal planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill collects body metrics and health-condition details and saves a generated report in the workspace.

Mitigation: Use only with explicit user consent, minimize sensitive inputs, and delete generated reports when they are no longer needed.

Risk: The skill provides nutrition guidance for sensitive situations such as pregnancy, diabetes, hypertension, gout, allergies, kidney or liver disease, medications, or eating-disorder history.

Mitigation: Treat outputs as general meal-planning guidance and seek qualified medical or dietitian advice for medical conditions or complex dietary restrictions.

Risk: The HTML report uses script-based rendering, external chart code, and dynamic HTML insertion.

Mitigation: Review the generated HTML before opening or sharing it, avoid untrusted input in report fields, and prefer a future version with bundled or integrity-pinned scripts and safer DOM rendering.

Risk: Some recipe references may permit raw or undercooked egg options.

Mitigation: Avoid raw or undercooked eggs and use fully cooked alternatives, especially for pregnancy, immunocompromised users, older adults, and children.

## Reference(s):

- [China Dietary Guidelines and Nutrition Reference](references/dietary_guidelines.md)
- [Quick Recipe Database](references/quick_recipe_database.md)
- [Recipe HTML Template](assets/recipe_template.html)
- [ClawHub Skill Page](https://clawhub.ai/mayabts/skills/foolproof-kitchen)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Files, Guidance]

**Output Format:** [HTML file plus concise meal-planning summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates a workspace HTML report for a personalized daily meal plan.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
