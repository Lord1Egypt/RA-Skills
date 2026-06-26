## Description: <br>
Recommends three food choices from a local menu database based on a user's location, weather, mood, budget, dining mode, time, cuisine, and spice preferences, with reasons and image references. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Pancat009](https://clawhub.ai/user/Pancat009) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent builders use this skill to quickly answer meal-choice requests such as what to eat, order, dine out for, or cook. It turns brief user preferences into concise recommendations with budget, spice level, dining mode, reasons, and image references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional image hydration helper can send dish names and prompts to third-party image services and write image files locally. <br>
Mitigation: Use the normal recommendation scripts for local suggestions; run scripts/hydrate_food_images.py only after reviewing the external-service behavior and confirming that the dish names or prompts are acceptable to share. <br>
Risk: The optional --external-ai-cmd parameter executes a user-provided command template. <br>
Mitigation: Avoid --external-ai-cmd unless the exact command is trusted, quoted, and run in a constrained environment. <br>
Risk: Feishu or OpenClaw image sending may share local images beyond the current workspace audience. <br>
Mitigation: Send only images intended for the recipient and keep image sending limited to the paths selected for the recommendation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Pancat009/eat-what-today-skill) <br>
- [Publisher profile](https://clawhub.ai/user/Pancat009) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown text with recommendation bullets, inline image links, and optional shell command usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommendation output normally includes three dishes, reasons, budget range, spice level, dining mode, and local image paths when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
