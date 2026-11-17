## Description:

AI演示文稿全流程制作：内容结构化→设计选型→AI插画/HTML构建→PPTX导出。17种实战验证的视觉风格（漫画/极简/数据叙事/国风），可编辑HTML与全AI视觉两条路径自由选择。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lifenglei](https://clawhub.ai/user/lifenglei)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to turn presentation requests or source material into Chinese slide outlines, visual direction, generated imagery or editable HTML, and final PPTX decks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Slide prompts, source content, or personal images may be sent to Google Gemini during image generation.

Mitigation: Use only non-sensitive materials unless external processing is approved, and get explicit consent before sending personal images or confidential deck content.

Risk: The skill text suggests reading GEMINI_API_KEY from a local Claude secrets file.

Mitigation: Provide GEMINI_API_KEY through the normal environment or a secrets manager, and do not allow agents to inspect ~/.claude/.env.

Risk: The bundled HTML-to-PPTX path converts local HTML with browser automation.

Mitigation: Convert only trusted HTML or run conversion in a restricted environment with JavaScript and network access controlled.

Risk: AI-generated slide visuals or embedded text can be inaccurate, malformed, or hard to edit in the full-image path.

Mitigation: Preview representative slides before delivery and regenerate or use the editable HTML path when textual accuracy and post-editing matter.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lifenglei/skills/duan-skill)
- [Design Movements Reference](references/design-movements.md)
- [Presentation Design Principles](references/design-principles.md)
- [Presentation Prompt Templates](references/prompt-templates.md)
- [Proven Styles Gallery](references/proven-styles-gallery.md)
- [Snoopy Style Guide](references/proven-styles-snoopy.md)
- [Ten Simple Rules for Effective Presentation Slides](https://pmc.ncbi.nlm.nih.gov/articles/PMC8638955/)
- [Assertion-Evidence Research](https://writing.engr.psu.edu/ae_comprehension.pdf)
- [Google Gemini Image Prompting](https://developers.googleblog.com/en/how-to-prompt-gemini-2-5-flash-image-generation-for-the-best-results/)
- [Google NotebookLM Slide Decks](https://blog.google/technology/google-labs/8-ways-to-make-the-most-out-of-slide-decks-in-notebooklm/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands, plus generated HTML, images, and PPTX files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require GEMINI_API_KEY for image generation and local Node.js or Python tooling for PPTX assembly.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
