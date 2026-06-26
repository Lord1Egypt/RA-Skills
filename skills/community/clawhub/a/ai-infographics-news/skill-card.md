## Description: <br>
Searches recent AI product, tool, funding, model, and OpenClaw/MaxClaw news, then generates a high-resolution AI news infographic with a short highlight summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LeahLiang](https://clawhub.ai/user/LeahLiang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and creators use this skill to turn recent AI news research into shareable infographic assets. It is suited for AI news recaps that need concise highlights, visual styling, and a saved image file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recent AI news selected from web results may be incomplete, outdated, or misleading. <br>
Mitigation: Review the selected news highlights and dates for accuracy before publishing or sharing the infographic. <br>
Risk: Generated infographic text or layout may contain rendering errors that change meaning or reduce readability. <br>
Mitigation: Inspect the generated image and regenerate or revise the prompt when important text is unclear or inaccurate. <br>
Risk: Optional CDN upload can share the generated image outside the local workspace. <br>
Mitigation: Use CDN upload only when external sharing is intended and the image contents have been reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/LeahLiang/ai-infographics-news) <br>
- [Infographic style reference](references/infographic-styles.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, image, guidance] <br>
**Output Format:** [Markdown summary plus a generated PNG image path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates a 2K infographic in 9:16 or 16:9 format, saves it under /workspace, and may upload to CDN only when sharing is intentionally requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
