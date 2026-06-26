## Description: <br>
Looks up Zurich waste collection dates through the public OpenERZ calendar API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MBjoern](https://clawhub.ai/user/MBjoern) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to find upcoming municipal waste, cardboard, paper, organic, special disposal, and related collection dates in Zurich by postal area or waste type. <br>

### Deployment Geography for Use: <br>
Zurich, Switzerland <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on live network requests to the public OpenERZ endpoint, so schedule answers may depend on endpoint availability and current API data. <br>
Mitigation: Confirm important disposal dates against the returned API data or the official municipal source before acting on time-sensitive guidance. <br>


## Reference(s): <br>
- [OpenERZ calendar API](https://openerz.metaodi.ch/api/calendar) <br>
- [ClawHub skill page](https://clawhub.ai/MBjoern/erz-entsorgung-recycling-zurich) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, JSON] <br>
**Output Format:** [Markdown guidance with optional curl commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Network requests go to the documented OpenERZ calendar endpoint when collection schedules are queried.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
