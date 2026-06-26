## Description: <br>
Plan culinary travel experiences, including local food tours, Michelin restaurants, street food crawls, cooking classes, food markets, and regional specialty tasting routes, with real-time travel data and booking links from flyai. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travel-focused agent users use this skill to search for culinary travel options, compare food-related points of interest or experiences, and produce user-facing recommendations with booking links. It is intended for food tour, street food, cooking class, and fine dining planning workflows that depend on flyai CLI results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install and run a third-party npm CLI and send travel queries to an external travel-search service. <br>
Mitigation: Review the flyai CLI and provider terms before use, run it in an appropriate environment, and avoid sending sensitive travel, payment, passport, or private booking information unless the provider's practices are acceptable. <br>
Risk: The skill may persist raw interaction details in local execution logs when filesystem writes are available. <br>
Mitigation: Keep prompts free of sensitive personal data, review generated logs, and delete or restrict access to local execution logs according to the user's retention requirements. <br>
Risk: Travel results depend on live external CLI responses and can be unavailable, incomplete, or delayed. <br>
Mitigation: Use the documented fallback and retry behavior, show only results returned by flyai with booking links, and report partial or failed retrieval honestly. <br>


## Reference(s): <br>
- [ClawHub food-tour page](https://clawhub.ai/xiejinsong/food-tour) <br>
- [Parent flyai skill](https://github.com/alibaba-flyai/flyai-skill/tree/main/skills/flyai) <br>
- [templates.md](artifact/references/templates.md) <br>
- [playbooks.md](artifact/references/playbooks.md) <br>
- [fallbacks.md](artifact/references/fallbacks.md) <br>
- [runbook.md](artifact/references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown recommendations with comparison tables, booking links, and inline shell commands when setup or retries are needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses flyai CLI output as the source for travel results and may include a local execution log when filesystem writes are available.] <br>

## Skill Version(s): <br>
v3.2.3 (source: server release metadata; artifact frontmatter version 3.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
