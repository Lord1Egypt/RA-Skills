## Description: <br>
Discover design-forward boutique hotels, Instagram-worthy interiors, unique architectural concepts, and curated artistic experiences using real-time Fliggy-powered flyai CLI results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel-planning agents use this skill to search for boutique, art, stylish, or design-forward hotels and format live CLI results with booking links. It can also support related travel planning requests when routed through the flyai CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release requires installing and running the @fly-ai/flyai-cli package. <br>
Mitigation: Verify the package source and version before installation, and use the skill in a controlled environment. <br>
Risk: Travel searches can involve sensitive personal details such as passport, payment, date, location, and lodging preferences. <br>
Mitigation: Avoid entering passport, payment, or other sensitive personal details unless required by a trusted booking flow. <br>
Risk: The skill can retain local travel-query history in .flyai-execution-log.json when filesystem writes are available. <br>
Mitigation: Delete or disable the local execution log if travel-query history should not be retained. <br>
Risk: Fallback behavior may broaden budget, date, location, or lodging-type constraints. <br>
Mitigation: Confirm material constraint changes with the user before acting on booking links. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiejinsong/design-hotel) <br>
- [templates.md](references/templates.md) <br>
- [playbooks.md](references/playbooks.md) <br>
- [fallbacks.md](references/fallbacks.md) <br>
- [runbook.md](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with hotel comparison tables, booking links, concise guidance, and inline shell commands when setup or retry steps are needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results are expected to be derived from flyai CLI output, include Book links, and avoid raw JSON.] <br>

## Skill Version(s): <br>
3.2.0 (source: server release evidence; artifact frontmatter declares 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
