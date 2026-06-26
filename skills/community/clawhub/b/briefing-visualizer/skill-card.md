## Description: <br>
将结构化文字简报转化为适合手机阅读和社交分发的长图，支持自定义标题、资讯内容、数据摘要、亮点洞察和底部通栏广告图。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xieliuzhu888](https://clawhub.ai/user/xieliuzhu888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, marketers, and business operators use this skill to turn structured industry, market, company, or招商 briefings into mobile-friendly long images for WeChat, Moments, Xiaohongshu, and similar channels. The agent prepares the briefing layout as HTML and can provide the shell command to render the final image with the bundled Python script. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a local Python script that launches headless Chrome. <br>
Mitigation: Install and run it only in an environment where local script execution and Chrome automation are acceptable. <br>
Risk: Generated HTML may include external links, scripts, or third-party assets supplied through briefing content. <br>
Mitigation: Review the generated HTML before rendering, especially when the briefing includes untrusted sources or embedded assets. <br>
Risk: Briefing content and banner images may contain confidential, unauthorized, or rights-restricted material. <br>
Mitigation: Use trusted content and only include material the user is permitted to process and distribute. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xieliuzhu888/briefing-visualizer) <br>
- [HTML Template Reference](references/html_template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with HTML/CSS code, shell command examples, and local image file output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a 390px-wide mobile briefing image locally; output file name and optional banner image are user-provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
