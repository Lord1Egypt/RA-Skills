## Description: <br>
AI食品营养管理助手 helps users record meals in natural language, look up food nutrition, and generate daily or weekly HTML nutrition reports with diet suggestions based on Chinese dietary guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and nutrition-focused assistants use this skill to record meals, estimate nutrient intake, compare foods, maintain local diary/profile data, and produce daily or weekly HTML reports. It is suited for personal nutrition tracking and general diet guidance, not professional medical diagnosis or treatment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meal history, nutrition estimates, reports, and profile data are stored locally and may contain sensitive health-adjacent personal information. <br>
Mitigation: Use the skill only in trusted workspaces, review generated user_data and report files before sharing, and remove local records when they are no longer needed. <br>
Risk: Optional TianAPI lookup requires an API key and may send food lookup terms to that service. <br>
Mitigation: Treat the API key as sensitive, keep it in local configuration only, rotate it if exposed, and avoid external lookup for private meal details. <br>
Risk: Nutrition values and dietary recommendations are estimates. <br>
Mitigation: Use outputs as general guidance and consult a qualified professional for medical, clinical, or condition-specific nutrition decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bettermen/food-nutrition) <br>
- [TianAPI](https://www.tianapi.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Conversational text and Markdown, with local JSON diary/configuration files and generated HTML reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores profile data, meal diary entries, cached food lookups, and generated reports locally; optional TianAPI lookups require an API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
