## Description: <br>
AI 智能家庭厨助 helps users choose recipes from available ingredients, generate cooking steps, find ingredient substitutions, plan menus, answer cooking questions, surface kitchen safety guidance, and create interactive HTML recipe reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill for household cooking support: recipe recommendations, step-by-step preparation guidance, substitutions, multi-day meal planning, cooking tips, safety prompts, and local HTML report generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive health, allergy, household, or dietary details could be included in prompts or optional web searches. <br>
Mitigation: Avoid entering sensitive details unless needed, and review prompts before allowing search-based fallback. <br>
Risk: Generated HTML reports may persist recipe, meal-planning, or dietary details on disk. <br>
Mitigation: Review generated files and remove or store them according to the user's local data handling expectations. <br>
Risk: Cooking and kitchen safety guidance may be incomplete for emergencies or specialized dietary needs. <br>
Mitigation: Treat generated guidance as a cooking reference and consult appropriate professionals or emergency services for urgent or specialized cases. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bettermen/chef-cooking) <br>
- [Project homepage](https://github.com/bettermen/chef-cooking) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance, command examples, optional JSON from helper scripts, and local HTML report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a bundled recipe database and may use web search when local recipe data is insufficient.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
