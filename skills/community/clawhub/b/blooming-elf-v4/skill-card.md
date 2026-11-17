## Description:

绿灵·Blooming Elf-v4 is a Chinese-language plant-care assistant that helps users onboard plants, maintain watering and care schedules, persist plant state in local JSON, and apply pet-toxicity and microclimate-aware guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shirley1011](https://clawhub.ai/user/shirley1011)

### License/Terms of Use:

MIT-0

## Use Case:

External users and plant-care hobbyists use this skill to create local plant records, receive watering and care reminders, update plant state after care actions, and get concise Chinese-language care guidance for household plants, cut flowers, and pet-safety concerns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores ongoing plant, location, schedule, and pet-safety details in local files.

Mitigation: Review configured storage paths before first use and keep sensitive user-specific plant data outside the published skill package.

Risk: Reminder automation may act on stored schedules and location-specific care data.

Mitigation: Create or update reminder automation only after explicit user confirmation, and keep reminder prompts data-driven rather than hard-coded.

Risk: Migration and real-data end-to-end tools have imperfect safeguards.

Mitigation: Run validation on demo data first, require explicit authorization for real data, and use temporary copies when exercising real-data workflows.

Risk: Care guidance may depend on local microclimate and pet-safety context that can become stale or incomplete.

Mitigation: Ask users to confirm current soil moisture, measured temperature and humidity, and pet exposure before making higher-risk care recommendations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shirley1011/skills/blooming-elf-v4)
- [Publisher profile](https://clawhub.ai/user/shirley1011)
- [CHANGELOG](CHANGELOG.md)
- [Authorization design](references/authorization.md)
- [Care quick reference](references/care-quickref.md)
- [Expert audit map](references/expert-audit-map.md)
- [Onboarding flow](references/onboarding.md)
- [Plant library](references/plant-library.md)
- [State schema](references/state-schema.md)
- [Supplemental care rules](references/supplements.md)
- [Pet toxicity reference](references/toxicity-reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Chinese-language Markdown responses with inline JSON state updates, shell command suggestions, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local file writes, validation commands, and user-confirmed reminder automation.]

## Skill Version(s):

4.0.4 (source: frontmatter, release evidence, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
