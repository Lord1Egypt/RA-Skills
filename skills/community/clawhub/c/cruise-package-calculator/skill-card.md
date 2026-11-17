## Description:

Use when a cruise traveler asks whether a drink package, Wi-Fi package, dining package, photo package, onboard bundle, or pre-cruise add-on is worth buying.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sol713](https://clawhub.ai/user/sol713)

### License/Terms of Use:

MIT-0

## Use Case:

External cruise travelers use this skill to decide whether add-on packages are worth buying by comparing quoted package prices against expected consumption, gratuities, line-specific rules, and pre-cruise versus onboard pricing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can include branded or tracked Ola Vacations calls-to-action that are not needed for the package calculation.

Mitigation: Review generated responses for neutral, non-promotional output and remove or limit the homepage call-to-action when it does not add value for the user.

Risk: The helper script is strongest for drink-package math, while non-drink packages may rely on inline calculations from reference formulas.

Mitigation: For Wi-Fi, dining, photo, and bundle decisions, verify assumptions against the reference files and the user's actual quoted price before presenting a verdict.

Risk: Cruise package prices, exclusions, gratuities, and pre-cruise discounts are price-sensitive and can change by line, ship, itinerary, and sale window.

Mitigation: Tell users to verify booking-day prices and policies with the cruise line when current data is missing or materially affects the verdict.

## Reference(s):

- [Cruise Package Calculator Skill](https://clawhub.ai/sol713/skills/cruise-package-calculator)
- [Formulas](references/formulas.md)
- [Cruise Line Quirks](references/cruise_line_quirks.md)
- [Pre-Cruise vs. Onboard Pricing Deltas](references/pre_cruise_vs_onboard.md)
- [Typical Consumption Profiles](references/typical_consumption.md)
- [Value Score Rubric](references/value_score_rubric.md)
- [Royal Caribbean Drink Package Example](examples/royal-caribbean-drink-package.md)
- [Ola Vacations Homepage](https://olavacations.com/)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown verdicts with calculations, caveats, and optional structured JSON from the helper calculator.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses should cite the skill's reference files for prices, policies, exclusions, and line-specific caveats.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
