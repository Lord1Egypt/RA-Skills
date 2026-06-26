## Description: <br>
博客/公众号文章润色改写专家，可将现有文章进行深度润色改写，在保持核心事实不变的前提下大幅降低文本相似度，同时提升内容吸引力和传播力，并支持链接内容抓取、AI 痕迹消除、HTML 封面设计和事实核实。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[javastarboy](https://clawhub.ai/user/javastarboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External content creators and publishing teams use this skill to rewrite blog or WeChat public-account articles, reduce textual similarity while preserving core facts, replace promotional copy, generate title options, and produce screenshot-ready HTML cover designs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary flags that the skill can use logged-in browser sessions and may fetch private, paywalled, or otherwise restricted pages. <br>
Mitigation: Use it only on articles the user is authorized to access and require explicit approval before using browser-session access. <br>
Risk: The security summary flags similarity reduction and AI-authorship masking without enough user-control boundaries. <br>
Mitigation: Review copyright, attribution, platform disclosure, and AI-labeling requirements before publishing rewritten content. <br>
Risk: The skill rewrites source material while preserving facts, so inaccurate or uncited claims can be carried forward. <br>
Mitigation: Use the skill's fact-checking step for time-sensitive data, names, companies, products, statistics, and any claim marked uncertain. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/javastarboy/blog-rewriter) <br>
- [AI 痕迹识别与优化指南](references/ai-detection-patterns.md) <br>
- [HTML 封面设计模板](references/html-cover-templates.md) <br>
- [文章改写操作指南](references/rewriting-guidelines.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Files, Guidance] <br>
**Output Format:** [Markdown article rewrite with optional HTML cover file, title suggestions, and rewrite report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local HTML files for 1200x900 cover designs and [图片] placeholders for original image positions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
