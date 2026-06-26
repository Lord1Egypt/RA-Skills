## Description: <br>
Dining OS v2.1 helps an assistant make concrete meal decisions for home cooking, dining out, delivery, gatherings, fitness goals, and special dining scenarios while respecting stated preferences, allergies, and health constraints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenchen913](https://clawhub.ai/user/chenchen913) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and assistants use this skill to choose meal plans, menus, or ordering decisions from user constraints such as headcount, dining format, dietary restrictions, health goals, cuisine preferences, and social context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may ask for or summarize dietary preferences and health-related dietary constraints. <br>
Mitigation: Share only details needed for the meal decision, avoid unnecessary medical information, and review or delete any generated profile before saving or reusing it. <br>
Risk: Meal guidance can be mistaken for medical or nutritional advice when health constraints are involved. <br>
Mitigation: Treat recommendations as meal-planning assistance and consult an appropriate professional for medical dietary requirements. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/chenchen913/dining) <br>
- [README](README.md) <br>
- [README English](README_EN.md) <br>
- [Algorithm Engine](references/algorithm-engine.md) <br>
- [Mode Routing](references/mode-routing.md) <br>
- [Cuisine Profiles](references/cuisine-profiles.md) <br>
- [Expert Cabinet](references/expert-cabinet.md) <br>
- [Memory System](references/memory-system.md) <br>
- [Output Schema](references/output-schema.md) <br>
- [Heuristics](references/heuristics.md) <br>
- [Dishes Reference](assets/dishes-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Configuration] <br>
**Output Format:** [Markdown meal recommendations with structured lists, tables, brief rationale, and optional reusable preference profile text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce deterministic menu plans, dish lists, sequencing guidance for home cooking, and concise preference summaries based on user-provided dining constraints.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
