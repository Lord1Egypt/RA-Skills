## Description: <br>
Discover Xinjiang's vast landscapes - Silk Road heritage, Tianshan mountains, Kanas Lake in autumn, Taklamakan Desert, and Uyghur culture and cuisine - and support travel booking workflows through the flyai CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-focused agents use this skill to plan Xinjiang trips and retrieve flights, hotels, attractions, itineraries, and booking links from flyai CLI results. It is intended for English and Chinese travel queries about destinations such as Urumqi, Kanas, Kashgar, and Silk Road routes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs agents to install and rely on an external, unpinned global flyai CLI package. <br>
Mitigation: Review and verify the CLI package before installation, install it deliberately rather than through unattended agent action, and use the skill only if the external CLI is trusted. <br>
Risk: Travel requests may be sent through the external flyai CLI. <br>
Mitigation: Use the skill only for queries that may be shared with the CLI provider and avoid entering sensitive personal or confidential travel details unless the deployment has approved that data flow. <br>
Risk: The skill may persist raw travel requests locally in .flyai-execution-log.json. <br>
Mitigation: Delete or disable .flyai-execution-log.json when local retention of travel queries is not desired, and define retention expectations before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dingtom336-gif/explore-xinjiang) <br>
- [templates.md](references/templates.md) <br>
- [playbooks.md](references/playbooks.md) <br>
- [fallbacks.md](references/fallbacks.md) <br>
- [runbook.md](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with booking links, comparison tables, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be derived from flyai CLI results, include booking detailUrl links when showing results, and avoid raw JSON.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
