## Description: <br>
Calorie1 Detective v3 uses Kimi/Moonshot vision to identify foods in selected photos and produce estimated calories and macronutrients from a local nutrition database. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaa2531349](https://clawhub.ai/user/aaa2531349) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to analyze food photos or descriptions, estimate calorie and macronutrient totals, and generate a concise nutrition report for diet tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected food photos are sent to Kimi/Moonshot for visual recognition. <br>
Mitigation: Use only images appropriate for third-party processing and avoid photos containing faces, documents, location clues, or private background details. <br>
Risk: The skill uses API keys for Kimi/Moonshot and optional nutrition services. <br>
Mitigation: Keep API keys in environment variables or private local configuration, and install dependencies in an isolated environment with patched package versions. <br>
Risk: Nutrition values are estimates and may be inaccurate for portion size, ingredients, or cooking method. <br>
Mitigation: Treat output as informational diet-tracking guidance rather than medical or professional nutrition advice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aaa2531349/calorie1) <br>
- [Moonshot chat completions API](https://api.moonshot.cn/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Chinese Markdown-style nutrition report printed to stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include identified foods, estimated calories, protein, carbohydrates, fat, and a short caution that nutrition values are AI estimates.] <br>

## Skill Version(s): <br>
3.0.2 (source: server release metadata; artifact metadata and changelog reference v3.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
