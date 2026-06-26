## Description: <br>
Navigate Florida for living, moving, working, seasonal stays, and road trips with region fit, storm planning, insurance reality, and daily logistics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill for Florida-specific relocation, resident, business, seasonal-living, and travel guidance. It helps compare regions, sequence administrative tasks, plan for storms and insurance, and decide when official state or local sources must be checked. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local memory could contain sensitive location, identity, insurance, healthcare, or payment details if the user asks the agent to save too much context. <br>
Mitigation: Ask before creating or updating ~/florida/, keep saved context coarse, and avoid storing precise addresses, government IDs, account numbers, Medicare numbers, credentials, or payment details. <br>
Risk: Florida rules, deadlines, insurance availability, school boundaries, evacuation guidance, and county execution can change or vary by locality. <br>
Mitigation: Use official state, county, district, emergency-management, tax collector, insurance, and health sources before giving precise compliance or address-specific guidance. <br>
Risk: General Florida guidance can be misleading when the user's mode, region, county, flood zone, school district, or seasonal-residency pattern is unknown. <br>
Mitigation: Classify the user as a visitor, future resident, current resident, business operator, or seasonal resident, then ask for the smallest location or timing detail needed before making specific recommendations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/florida) <br>
- [Skill homepage](https://clawic.com/skills/florida) <br>
- [Official Florida sources map](artifact/sources.md) <br>
- [Florida state services](https://www.myflorida.gov/) <br>
- [Florida Highway Safety and Motor Vehicles](https://www.flhsmv.gov/) <br>
- [Florida Division of Emergency Management](https://www.floridadisaster.org/) <br>
- [Florida insurance consumer resources](https://www.myfloridacfo.com/division/consumers) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration instructions] <br>
**Output Format:** [Markdown guidance with checklists, tradeoff summaries, and source links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May optionally create local memory under ~/florida/ after user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
