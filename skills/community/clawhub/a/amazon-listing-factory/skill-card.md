## Description: <br>
Generate complete Amazon listing drafts with title, bullets, image plan, prompts, and video script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lenger666](https://clawhub.ai/user/lenger666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, marketers, and ecommerce operators use this skill to draft Amazon listing content from product inputs, including titles, bullet points, image plans, image prompts, and video scripts. When configured, it can call external services to generate images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports API-backed listing and image generation with under-disclosed external image generation. <br>
Mitigation: Use dedicated low-privilege API keys, review LISTING_BASE_URL and COZE_API_URL before running, and avoid sensitive product data unless third-party processing is acceptable. <br>
Risk: The security review reports Feishu routing and tmux recipient detection. <br>
Mitigation: Audit or disable Feishu sending and tmux recipient detection before use, especially in shared or multi-user runtime environments. <br>
Risk: The security review reports debug route output and local runtime.log retention. <br>
Mitigation: Review debug output before enabling it and restrict, rotate, or delete retained runtime logs after runs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lenger666/amazon-listing-factory) <br>
- [Feishu usage tutorial](https://my.feishu.cn/docx/DzpHdBjJdosX6Nx7CAMc9OY5nZf) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [JSON object containing a Markdown answer with listing copy tables and optional image result links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated image URLs when image environment variables are configured; otherwise includes image prompts and an image plan.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
