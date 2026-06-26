## Description: <br>
AiPPT-skill helps agents collaborate with users to generate presentation decks through the AiPPT.cn Open Platform API, including outline editing, template selection, file or URL import, and export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huiyuan1234](https://clawhub.ai/user/huiyuan1234) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create, refine, and export presentation decks from a topic, document, existing PPT, URL, or single-slide request while keeping outline and template decisions visible before final generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, uploaded files, and URLs may be sent to AiPPT's external service. <br>
Mitigation: Use only with material your organization permits sending to AiPPT, and avoid confidential, regulated, or internal-only inputs unless approved. <br>
Risk: The skill requires sensitive AiPPT credentials and may use a paid service. <br>
Mitigation: Configure credentials only through the platform's secure skill settings, avoid pasting keys into chat, and verify account access and billing before use. <br>
Risk: Generated presentations may contain errors or unsuitable content. <br>
Mitigation: Review generated files before sharing or publishing them. <br>


## Reference(s): <br>
- [AiPPT Open Platform documentation](https://open.aippt.cn/docs/zh/) <br>
- [ClawHub AiPPT-skill page](https://clawhub.ai/huiyuan1234/aipptskill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands, progress messages, and generated presentation file paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce PPTX output and optional PDF, Word, or PNG exports through AiPPT; requires configured AiPPT credentials.] <br>

## Skill Version(s): <br>
4.0.2 (source: server release metadata; artifact skill.json and script still identify 4.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
