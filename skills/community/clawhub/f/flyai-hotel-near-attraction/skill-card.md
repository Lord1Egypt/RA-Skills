## Description: <br>
Finds hotels closest to a specified attraction or landmark by verifying the POI, searching FlyAI/Fliggy hotel results sorted by distance, and presenting walking or driving time with booking links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travel-planning users and agents use this skill to find lodging near a named attraction, validate the point of interest, compare nearby hotels by distance, and surface booking details and practical stay advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on an external FlyAI/Fliggy CLI and may send travel search details such as destination, dates, and attraction names to that service. <br>
Mitigation: Confirm the user is comfortable using FlyAI/Fliggy before execution and avoid sending unnecessary personal or sensitive travel details. <br>
Risk: The workflow is distance-first and can conflict with a user's stated preference for cheapest, highest-rated, or another sorting criterion. <br>
Mitigation: Preserve explicit user sorting or quality preferences in the response and clearly state when distance is prioritized by the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/flyai-hotel-near-attraction) <br>
- [Parameter collection and output templates](artifact/references/templates.md) <br>
- [Attraction hotel playbooks](artifact/references/playbooks.md) <br>
- [Fallback handling](artifact/references/fallbacks.md) <br>
- [Execution logging runbook](artifact/references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown response with CLI command snippets and distance-sorted hotel comparison tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses POI verification before hotel search and includes booking links, POI context, fallback handling, and a FlyAI data-source statement.] <br>

## Skill Version(s): <br>
1.0.55596 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
