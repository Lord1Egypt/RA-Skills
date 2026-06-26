## Description: <br>
Design Datadog dashboards and monitors, recommend metrics, widget layouts, alerting thresholds, and SLO definitions, and analyze existing dashboards for blind spots and noise. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SREs, and on-call engineers use this skill to design Datadog dashboards, monitors, and SLOs for services or to audit existing observability for blind spots and noisy alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recommended alert thresholds, no-data settings, notification routing, or SLO targets may not match a service's production behavior. <br>
Mitigation: Review and adapt those recommendations with service owners before applying them in production. <br>
Risk: Dashboard or monitor guidance may be incomplete if the user omits service tier, dependencies, traffic pattern, or current incident history. <br>
Mitigation: Collect the service profile and validate proposed widgets and monitors against real Datadog metrics before relying on the design. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/charlie-morrison/datadog-dashboard-builder) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown guidance with example Datadog widget, monitor, and SLO configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces recommendations and implementation steps for user review; it does not automatically modify Datadog resources.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
