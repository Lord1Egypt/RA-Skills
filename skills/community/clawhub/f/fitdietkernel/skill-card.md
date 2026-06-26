## Description: <br>
A personal fitness diet knowledge base that helps an AI calculate diet plans for carbon cycling, ketogenic, muscle gain, and fat loss workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yibinpro](https://clawhub.ai/user/yibinpro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and AI-assisted fitness practitioners use this skill to read local profile, food registry, recipe, and log files so an agent can calculate macro targets, track carbohydrate variance, register foods, and draft diet check-ins or weekly reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores diet, weight, sleep, meal, and daily log records locally, which may be sensitive health-related personal data. <br>
Mitigation: Keep the skill directory private, avoid committing personal logs or profile data to public repositories, and review stored files before sharing them. <br>
Risk: Agent-assisted updates to the food registry or logs could overwrite or add incorrect personal tracking data. <br>
Mitigation: Ask the agent to preview proposed changes before writing to food_registry.json or logs, and review the resulting file diffs. <br>
Risk: The HTML UI may load Chart.js from an external CDN. <br>
Mitigation: Use the HTML UI only when external CDN loading is acceptable for the environment. <br>


## Reference(s): <br>
- [ClawHub FitDietKernel release page](https://clawhub.ai/yibinpro/fitdietkernel) <br>
- [README](README.md) <br>
- [FitDietKernel skill definition](SKILL.md) <br>
- [Core diet rules](knowledge_base/rules.md) <br>
- [BioContext-Kernel logic rules](knowledge_base/logic_rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text guidance, JSON-compatible local data updates, and optional generated Markdown reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and update local profile, food registry, recipe, and log files when the user asks the agent to track meals or register foods.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
