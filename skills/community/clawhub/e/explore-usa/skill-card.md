## Description: <br>
Plan American trips across cities, parks, and coast-to-coast routes using FlyAI/Fliggy CLI results for flights, hotels, attractions, itineraries, visa information, insurance, car rental, and booking links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to search and compare USA travel options, format real-time FlyAI/Fliggy results, and produce booking-oriented Markdown responses with links. Developers can also use it as a command orchestration workflow for FlyAI CLI travel searches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install and execute a global third-party FlyAI CLI package. <br>
Mitigation: Install only in trusted environments after reviewing the FlyAI CLI package and keep execution scoped to travel-search commands requested by the user. <br>
Risk: Travel searches may send itinerary details to FlyAI/Fliggy and the artifact describes local logging of raw user queries. <br>
Mitigation: Avoid entering passport, payment, or highly personal itinerary details, and disable or remove the .flyai-execution-log.json behavior before use when local persistence is not acceptable. <br>
Risk: Visa and policy guidance can be incomplete or outdated if CLI data is unavailable. <br>
Mitigation: Verify visa requirements and official travel policies with government or consulate sources before acting. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [Templates](references/templates.md) <br>
- [Playbooks](references/playbooks.md) <br>
- [Fallbacks](references/fallbacks.md) <br>
- [Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with tables, booking links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai CLI output for travel data and should include booking links when results are available.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
