## Description: <br>
ClickMap helps agents save named on-screen browser targets and reuse them for deterministic click and type actions when selectors are brittle. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jayton123456789-hub](https://clawhub.ai/user/jayton123456789-hub) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation users use ClickMap to capture named points of interest in Chrome and run repeatable click and type flows for web tools, dashboards, and forms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved POIs may include selectors, labels, text snippets, URLs, and coordinates from pages the user visits. <br>
Mitigation: Use ClickMap only on sites where storing this browser UI data is acceptable, and review saved POIs before reuse. <br>
Risk: The local bridge is unauthenticated by default and reachable from browser pages. <br>
Mitigation: Set a strong CLICKMAP_TOKEN, avoid exposing or autostarting the bridge unnecessarily, and keep the bridge URL local unless remote sharing is intentional. <br>
Risk: Automated click and type actions can trigger sensitive operations such as submitting, purchasing, deleting, or logging in. <br>
Mitigation: Re-check saved points before using ClickMap for sensitive actions and require human review for workflows with irreversible effects. <br>


## Reference(s): <br>
- [ClickMap ClawHub listing](https://clawhub.ai/jayton123456789-hub/clickmap) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell command examples and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent instructions for saving and reusing named browser points of interest; the skill also includes Chrome extension assets, a local bridge script, and POI JSON data.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
