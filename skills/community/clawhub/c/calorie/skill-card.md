## Description: <br>
Calorie Detective analyzes food photos with AI vision to estimate calories, protein, carbohydrates, fat, and dietary suggestions using Kimi vision and a local food nutrition database. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaa2531349](https://clawhub.ai/user/aaa2531349) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to submit food images and receive an estimated nutrition report for everyday diet tracking, fitness planning, and calorie awareness. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API-key/provider handling is under-scoped and could expose or misuse credentials if broad keys are configured. <br>
Mitigation: Use a dedicated low-scope API key, set only the intended provider key, and avoid storing secrets in configuration files. <br>
Risk: Food photos may contain sensitive details such as faces, documents, location clues, or private surroundings. <br>
Mitigation: Avoid uploading images with sensitive content and disclose that photos are sent to the configured vision provider for analysis. <br>
Risk: Nutrition results are AI estimates and may be inaccurate for portion size, ingredients, and cooking method. <br>
Mitigation: Treat reports as general diet-tracking guidance and consult qualified nutrition or medical professionals for health-critical decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/aaa2531349/calorie) <br>
- [Moonshot Platform Documentation](https://platform.moonshot.cn/docs) <br>
- [Moonshot Chat Completions API](https://api.moonshot.cn/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, shell commands, guidance] <br>
**Output Format:** [Markdown nutrition report with calorie, macronutrient, itemized food, and recommendation sections; deployment guidance uses YAML and shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts JPEG, PNG, and WebP food images in the Kimi Claw configuration; generated estimates are advisory and may vary by ingredients, portion size, and cooking method.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
