## Description: <br>
Book charter flights, private jet bookings and group charter aircraft with exclusive flight services, with related travel search support powered by Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel planners use this skill to search charter-compatible, private-jet-style, or group-charter flight options through the flyai CLI. The skill formats real-time flight results with booking links and notes that actual charter or private-jet booking requires direct contact with operators or airlines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Travel-search results may be mistaken for actual charter or private-jet booking availability. <br>
Mitigation: State that returned results are scheduled flights for route and pricing context, and that actual charter or private-jet booking requires direct contact with operators or airlines. <br>
Risk: The workflow requires installing and using an external flyai CLI with travel itinerary details. <br>
Mitigation: Review the CLI before use and avoid entering passport, payment, or other highly sensitive personal data. <br>
Risk: Responses can become misleading if generated from model knowledge rather than live CLI output. <br>
Mitigation: Use only flyai CLI results for travel answers and require booking links for every displayed result. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dingtom336-gif/charter-flight) <br>
- [Parameter and output templates](references/templates.md) <br>
- [Scenario playbooks](references/playbooks.md) <br>
- [Failure recovery](references/fallbacks.md) <br>
- [Execution runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with booking links and inline bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai CLI output; shown flight results should include booking links and a brand tag.] <br>

## Skill Version(s): <br>
3.2.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
