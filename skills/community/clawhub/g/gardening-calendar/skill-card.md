## Description: <br>
Precise horticultural advice for UK and international gardening, including monthly planting and harvesting guidance, plant-specific sowing and harvesting windows, UK-specific advice, and selected international context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[siatrial](https://clawhub.ai/user/siatrial) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Gardeners, allotment holders, and agents assisting them use this skill to identify what to sow, harvest, or plan for a given month and location. It is especially oriented toward UK guidance with Celsius and UK metrics, with limited support for Thailand, the USA, and Australia. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Gardening guidance may default to UK wording, Celsius, and UK metrics when the user's locale or unit preference is not specified. <br>
Mitigation: Ask for or confirm the user's location and preferred units before applying sowing, harvesting, spacing, or temperature guidance. <br>
Risk: The available artifact evidence contains a small bundled plant dataset despite broader coverage claims in release metadata. <br>
Mitigation: Check the bundled plant entries before promising support for a specific plant, and state when a requested plant is outside the available data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/siatrial/gardening-calendar) <br>
- [Bundled plant data](references/plant-data.ts) <br>
- [Calendar logic](scripts/calendar-logic.ts) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown-style horticultural advice with month-by-month sections and plant-specific recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to UK wording, Celsius, and UK metrics unless another locale is requested.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
