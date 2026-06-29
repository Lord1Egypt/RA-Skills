## Description: <br>
Amazon 产品全链路深度研究助手，可从一句产品名、ASIN, or description run product search, review collection, AI tagging, keyword expansion, VOC clustering, competitor analysis, opportunity analysis, and produce an interactive HTML report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, product researchers, and ecommerce operators use this skill to research Amazon product categories, compare competitors, analyze customer reviews, identify VOC pain points, expand keywords, and generate product opportunity reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Real runs can send queries, product and review text, and generated analysis to selected API providers. <br>
Mitigation: Use mock mode for demonstrations or confidential research, and only provide API keys when sharing that data with the selected providers is acceptable. <br>
Risk: Generated HTML reports may load remote scripts or images when opened. <br>
Mitigation: Treat reports as local files, review them before sharing, and open them in an environment appropriate for remote resource loading. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bettermen/amazon-product-research) <br>
- [Publisher profile](https://clawhub.ai/user/bettermen) <br>
- [RapidAPI Amazon hub](https://rapidapi.com/hub/amazon) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands, Python script outputs, structured analysis data, and interactive HTML reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Report output defaults to a local product_research timestamped HTML file; mock mode can run without API keys.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
