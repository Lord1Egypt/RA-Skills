## Description:

干饭决策助手 helps users decide what to eat, discover nearby restaurants, navigate to restaurants, and generate restaurant-specific skill files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hash-panda](https://clawhub.ai/user/hash-panda)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill as a meal-decision assistant: it selects food categories, recommends restaurants, supports reminders, searches nearby places through AMap, plans routes, and can create restaurant-specific skill files from structured or POI data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores a local food profile and meal history that can include location, taste, budget, diet, and restaurant history.

Mitigation: Review the generated profile before use, remove sensitive fields you do not want retained, and keep the profile in a trusted local workspace.

Risk: Nearby search and route planning can send user-provided location, restaurant, and route data to AMap.

Mitigation: Use AMap features only when comfortable sharing that data with the map provider, and avoid entering precise home or sensitive locations unless needed.

Risk: Default weekday lunch and dinner reminders are enabled by the included schedule configuration.

Mitigation: Disable or edit the scheduled reminders before installation if recurring execution is not desired.

Risk: Restaurant skill generation from POI or YAML data can create files from untrusted input.

Mitigation: Generate restaurant skills only from trusted data, review generated Markdown/YAML before installing or sharing it, and validate slugs and escaping before broader use.

Risk: AMap API keys may be configured for map features.

Mitigation: Prefer environment variables for API keys, avoid committing key files, and rotate credentials if they are exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hash-panda/skills/eat-skill)
- [README_EN.md](README_EN.md)
- [Command details](docs/commands-detail.md)
- [AMap Web Service API overview](https://lbs.amap.com/api/webservice/summary)
- [AMap Web Service key setup](https://lbs.amap.com/api/webservice/create-project-and-key)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and plain text responses with optional JSON profile data, YAML restaurant data, generated Markdown skill files, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use local profile/history files, scheduled reminder configuration, Node.js scripts, and AMap Web Service calls when an API key is available.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter and package.json report 0.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
