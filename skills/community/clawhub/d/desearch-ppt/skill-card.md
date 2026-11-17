## Description:

v2.0 Pro版：端到端自动化研究报告与PPT生成器。结合ZeeLin深度研究、.gov域名数据验证、原创概念生成、Gemini 3.1图像生成与OCR错别字核验。输入任意主题，即可自动生成一份包含原创思想、数据来源可追溯的深度研究报告，并将其转化为一份视觉惊艳、内容严谨、无错别字的专业级PPT/PDF。

This skill is ready for commercial/non-commercial use.

## Publisher:

[kelcey2023](https://clawhub.ai/user/kelcey2023)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content teams use this skill to turn a user-supplied research topic into a sourced research report, structured slide outline, image-generation prompts, and assembled presentation outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can invoke privileged package installation paths.

Mitigation: Review before installing, use an isolated environment, and do not run the sudo pip or runtime sudo apt-get paths from the skill unless they have been approved.

Risk: The workflow requires research and image-generation API keys.

Mitigation: Provide DESEARCH_API_KEY and GEMINI_API_KEY only in trusted environments and limit the credentials to the intended workflow.

Risk: Generated decks may include fixed team branding or contact text.

Mitigation: Remove or configure the fixed team branding/contact text when faithful report-derived output is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kelcey2023/skills/desearch-ppt)
- [PPT structure and outline guide](references/slide_structure.md)
- [ZeeLin DeSearch API activity page](https://desearch.zeelin.cn/skill-activity)
- [Tesseract OCR Windows installer wiki](https://github.com/UB-Mannheim/tesseract/wiki)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown research reports, JSON slide outlines and prompts, and generated PPTX/PDF presentation files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DESEARCH_API_KEY and GEMINI_API_KEY for the documented research and image-generation workflow.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
