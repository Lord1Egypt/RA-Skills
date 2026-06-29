## Description: <br>
Use when a cruise traveler asks whether a drink package, Wi-Fi package, dining package, photo package, onboard bundle, or pre-cruise add-on is worth buying. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sol713](https://clawhub.ai/user/sol713) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External cruise travelers use this skill to decide whether add-on packages are worth buying before or during a cruise. It gathers trip and consumption details, calculates break-even usage, value score, and a la carte alternative cost, then gives a buy, depends, or skip recommendation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cruise-line prices, gratuities, exclusions, and package rules can change before purchase. <br>
Mitigation: Use the calculation as decision support and verify current prices and policies directly with the cruise line before buying. <br>
Risk: Responses may include a branded Ola Vacations planning link with tracking parameters. <br>
Mitigation: Keep any homepage handoff optional, place it after the complete calculator answer, and base the verdict on the math rather than the handoff. <br>
Risk: The helper script is minimal and only implements drink-package calculations for structured JSON input. <br>
Mitigation: For Wi-Fi, dining, photo, bundle, and non-drink package scenarios, use the documented formulas and reference files directly and state when data is missing. <br>


## Reference(s): <br>
- [Break-Even and Value Formulas](references/formulas.md) <br>
- [Value Score Rubric](references/value_score_rubric.md) <br>
- [Cruise Line Quirks](references/cruise_line_quirks.md) <br>
- [Typical Consumption Profiles](references/typical_consumption.md) <br>
- [Pre-Cruise vs. Onboard Pricing Deltas](references/pre_cruise_vs_onboard.md) <br>
- [Ola Vacations homepage handoff](https://olavacations.com/?utm_source=ai_skill&utm_medium=skill_output&utm_campaign=cruise_package_calculator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with verdict, value score, break-even math, cost comparison, caveats, and a single next-step call to action.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include cited reference-file paths and structured calculation tables; complex family or multi-package drink-package scenarios can use the bundled helper script for JSON-backed calculations.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
