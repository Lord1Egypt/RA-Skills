## Description:

AiPPT-skill helps agents use the AiPPT.cn Open Platform API to collaboratively generate, edit, template, export, and download presentation files from topics, documents, existing PPT files, URLs, or single-slide requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huiyuan1234](https://clawhub.ai/user/huiyuan1234)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide an agent through PPT generation workflows, including outline review, template selection, file or URL import, and export to PPTX, PDF, Word, or PNG. It is suited for presentation drafting where the user can review generated outlines and exported files before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Presentation topics, URLs, and selected local documents may be sent to AiPPT.cn during generation workflows.

Mitigation: Use the skill only with content approved for AiPPT.cn processing, and review generated outlines and exports before sharing them.

Risk: Credentials and cached tokens can be exposed if stored in local files or shared writable directories.

Mitigation: Use platform-managed secrets where available, avoid shared writable install locations, and clear or protect the token cache after use.

Risk: The broad activation scope may run on many presentation-related prompts.

Mitigation: Confirm the intended generation path before sending files, URLs, or sensitive prompt content to the service.

## Reference(s):

- [AiPPT Open Platform Documentation](https://open.aippt.cn/docs/zh/)
- [ClawHub Skill Page](https://clawhub.ai/huiyuan1234/skills/aipptskill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Markdown guidance with shell command examples and generated file paths for exported presentation assets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can export PPTX, PDF, Word, and PNG files after AiPPT task creation, outline handling, template selection, and download.]

## Skill Version(s):

4.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
