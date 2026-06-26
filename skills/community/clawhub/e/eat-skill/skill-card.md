## Description: <br>
干饭 skill helps users decide what to eat, discover nearby restaurants, plan routes, compare options, receive meal reminders, and generate restaurant-specific skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hash-panda](https://clawhub.ai/user/hash-panda) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to quickly choose meals, adapt recommendations to taste, budget, time, weather, and scenario, and find or generate restaurant information for future use. Developers and agent users can also use its bundled scripts to search AMap, plan routes, schedule meal reminders, and create restaurant skill files. <br>

### Deployment Geography for Use: <br>
China and regions supported by AMap/Gaode services <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores taste, location, budget, dietary preference, and meal history data locally. <br>
Mitigation: Keep the profile minimal, avoid sensitive details, and review or delete local profile and history files when they are no longer needed. <br>
Risk: Restaurant search and route planning can send location, search, and route information to AMap services. <br>
Mitigation: Use a limited AMap Web Service key, keep it in the environment rather than a saved config file, and avoid sharing sensitive locations. <br>
Risk: The skill can generate restaurant skill files and schedule local meal-reminder commands. <br>
Mitigation: Review generated restaurant skills and scheduled commands before keeping, sharing, or enabling them. <br>
Risk: The release evidence includes broad capability tags such as crypto and can-make-purchases that are not needed for normal meal recommendation use. <br>
Mitigation: Do not grant purchase, crypto, or unrelated authority to this skill unless a separate review proves it is necessary. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/hash-panda/eat-skill) <br>
- [Command reference](docs/commands-detail.md) <br>
- [AMap Web Service API](https://lbs.amap.com/api/webservice/summary) <br>
- [AMap Web Service key setup](https://console.amap.com/dev/key/app) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance] <br>
**Output Format:** [Markdown-style agent responses with command snippets, JSON configuration, and generated skill files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local profile/history data, schedule configuration, and restaurant skill files; may call AMap services when an API key is configured.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata; artifact frontmatter and package.json report 0.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
