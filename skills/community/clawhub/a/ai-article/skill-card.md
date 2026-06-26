## Description: <br>
Generates Chinese article drafts with platform-aware structure, suggested actions, and accompanying images or cover assets from a topic, audience, keywords, and brand requirements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[allinherog-star](https://clawhub.ai/user/allinherog-star) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, operators, copywriters, and technical content teams use this skill to turn a topic or campaign brief into a publishable Chinese article package. It is intended for content planning and drafting across platforms such as Xiaohongshu, WeChat, blogs, and Zhihu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send prompts, drafts, audience details, keywords, brand requirements, and profile context to the AI Skills API using the caller's API key. <br>
Mitigation: Use only with approved content for that provider, avoid confidential drafts, customer data, regulated personal data, secrets, or proprietary brand material, and confirm before execution when sensitive context may be included. <br>
Risk: Broad implicit invocation can cause the skill to run when a user asks for article or seeded-content generation. <br>
Mitigation: Prefer explicit confirmation before running the skill or disable implicit invocation in environments that handle sensitive planning or brand material. <br>
Risk: Generated articles and images may need editorial, factual, brand, and platform-policy review before publication. <br>
Mitigation: Review title, opening, structure, claims, images, watermark settings, and platform fit before publishing or handing off deliverables. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/allinherog-star/ai-article) <br>
- [AI Skills quick start](https://github.com/allinherog-star/ai-skills/tree/main#%E5%BF%AB%E9%80%9F%E5%BC%80%E5%A7%8B) <br>
- [AI Skills website](https://ai-skills.ai) <br>
- [Form schema](references/form-schema.json) <br>
- [Skill definition](references/skill.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [JSON response envelope containing Markdown article artifacts, generated image files, and download links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run asynchronously and return article Markdown, WebP image artifacts, cover assets, and an archive URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
