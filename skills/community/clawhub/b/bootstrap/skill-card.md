## Description: <br>
Generate a personalized SOUL.md through a warm, adaptive onboarding conversation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huanz](https://clawhub.ai/user/huanz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to create or update a personalized AI partner profile through a short onboarding conversation, then save the confirmed result as a local SOUL.md file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated SOUL.md can preserve personal details such as role, pain points, preferences, boundaries, and long-term goals. <br>
Mitigation: Review the generated profile before confirming it, and remove any personal details that should not be saved locally. <br>
Risk: Updating an existing SOUL.md could replace or merge prior profile content in ways the user did not intend. <br>
Mitigation: Warn when a SOUL.md already exists and require the user to choose overwrite or merge before writing changes. <br>
Risk: Autonomy and ongoing-learning preferences may affect how future agent interactions behave. <br>
Mitigation: Confirm language, autonomy, pushback, and ongoing-learning wording before saving the final profile. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/huanz/bootstrap) <br>
- [Conversation Guide](references/conversation-guide.md) <br>
- [SOUL.md Template](templates/SOUL.template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown conversation with a generated SOUL.md profile and local save confirmation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The generated SOUL.md is intended to stay under 300 words and is saved only after user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
