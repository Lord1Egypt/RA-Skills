## Description:

Offloads low-stakes daily decisions. Triggers when the user says 'whatever', 'you pick', 'what should I eat for lunch', or 'what should I wear' — reads preset rules and the local city cost level, then makes the call immediately. No pros/cons matrices. Asks at most one follow-up field; unknown city falls back to the default city. Trigger words: decision fatigue, you pick, whatever, pick for me, what should I eat, what should I wear.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snowhola](https://clawhub.ai/user/snowhola)

### License/Terms of Use:

MIT-0

## Use Case:

People who want help with low-stakes daily choices can use the skill to get a direct dining, clothing, shopping, or leisure recommendation based on preset rules and their city. It also adapts future choices when users share preference feedback or update their home city.

### Deployment Geography for Use:

Global; built-in cost estimates primarily cover major Chinese cities.

## Known Risks and Mitigations:

Risk: A statement such as ‘I'm in [city]’ updates the saved home city, including during travel, which could affect later suggestions.

Mitigation: Review the Home City field in references/user-rules.md after travel and correct or remove it if needed.

Risk: Built-in cost estimates are primarily for major Chinese cities, so price thresholds may be inaccurate elsewhere.

Mitigation: For a city outside the table, add a suitable multiplier to references/user-rules.md or check suggested price thresholds against local costs.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/snowhola/skills/decision-fatigue-offloader-en)
- [Default Rules](references/default-rules.md)
- [User Custom Rules](references/user-rules.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration]

**Output Format:** [Four-line Markdown decision card; may update a Markdown preference file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Asks at most one follow-up question and may save city and preference feedback for future suggestions.]

## Skill Version(s):

1.1.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
