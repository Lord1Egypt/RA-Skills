## Description: <br>
Plan Sanya travel by using flyai CLI results for flights, hotels, attractions, itinerary options, and booking links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travel-planning users and agent developers use this skill to retrieve current Sanya flight, hotel, attraction, and itinerary options through flyai and present concise Markdown results with booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to install a global third-party CLI. <br>
Mitigation: Treat npm global installation as a manual setup step and avoid letting an agent run npm i -g automatically. <br>
Risk: Travel queries may be retained in a local .flyai-execution-log.json file. <br>
Mitigation: Review, disable, or delete local execution logging before entering personal travel details. <br>
Risk: Results rely on flyai/Fliggy as the travel data provider and may include booking links. <br>
Mitigation: Install only if that provider and booking-link workflow are acceptable for the deployment context. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dingtom336-gif/explore-sanya) <br>
- [templates.md](references/templates.md) <br>
- [playbooks.md](references/playbooks.md) <br>
- [fallbacks.md](references/fallbacks.md) <br>
- [runbook.md](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses flyai CLI output as the required data source and avoids raw JSON in user-facing responses.] <br>

## Skill Version(s): <br>
3.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
