## Description: <br>
Book airport transfer services - private cars, shared shuttles, and limo services for comfortable, stress-free arrivals and departures, with related travel booking support powered by Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and travel-assistance agents use this skill to search airport pickup, drop-off, private car, shared shuttle, and limo services through the flyai CLI and present real-time booking options with required booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can save raw travel queries locally in .flyai-execution-log.json without clear retention limits. <br>
Mitigation: Avoid entering unnecessary personal, passport, payment, or full itinerary details, and disable or delete .flyai-execution-log.json after use. <br>
Risk: The skill requires installing and using the global flyai CLI, which sends travel search details to the provider. <br>
Mitigation: Install and run the CLI only in trusted environments, review commands before execution, and share only the minimum travel details needed for the search. <br>


## Reference(s): <br>
- [Templates](references/templates.md) <br>
- [Playbooks](references/playbooks.md) <br>
- [Fallbacks](references/fallbacks.md) <br>
- [Runbook](references/runbook.md) <br>
- [Parent flyai skill](https://github.com/alibaba-flyai/flyai-skill/tree/main/skills/flyai) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses must be sourced from flyai CLI output, include Book links when showing results, and avoid raw JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter states 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
