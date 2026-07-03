## Description: <br>
上传花卉或植物照片后，这个技能使用 DashScope 多模态模型识别品种、生成浇水、光照、温度、土壤、施肥和病虫害六维养护建议，并输出摘要和交互式 HTML 报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and gardening enthusiasts use this skill to identify plants from photos, receive practical care guidance, and generate a shareable HTML care report. It can also answer plant-care questions from its bundled offline knowledge base when no image is supplied. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use broad credentials by falling back to OPENAI_API_KEY when DASHSCOPE_API_KEY is absent. <br>
Mitigation: Use a dedicated DashScope key and avoid running the skill in environments where unrelated API keys are set. <br>
Risk: Uploaded plant photos are sent to DashScope and copied into the generated HTML report. <br>
Mitigation: Use non-sensitive images, review generated reports before sharing, and store reports only in appropriate locations. <br>
Risk: The HTML report is generated from AI output and may contain unsafe or misleading content. <br>
Mitigation: Review the generated report before opening, sharing, or relying on its recommendations. <br>
Risk: Pest-control recommendations may include chemical treatment advice. <br>
Mitigation: Treat chemical guidance as informational and follow product labels, local rules, and professional advice where needed. <br>


## Reference(s): <br>
- [Project homepage](https://github.com/bettermen/flower-care) <br>
- [Plant care database](references/plant_care_db.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown summary with optional shell commands and a generated interactive HTML report file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a plant image path for API-based identification or a plant name for offline knowledge-base guidance; generated HTML may embed the uploaded image and model output.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
