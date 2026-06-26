## Description: <br>
Generate BNBOT lobster-bot mascot images in a consistent style using reference images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackleeio](https://clawhub.ai/user/jackleeio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, marketers, and brand operators use this skill to generate BNBOT mascot illustrations, social posts, stickers, and transparent PNG assets from approved reference poses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mascot prompts and reference images are sent to Google Gemini during image generation. <br>
Mitigation: Install only when that data flow is acceptable, and avoid submitting sensitive prompts or private reference images. <br>
Risk: The skill uses local credentials and includes a hard-coded developer .env fallback path. <br>
Mitigation: Provide GOOGLE_AI_API_KEY through the intended environment and prefer a revised release that removes the developer-specific fallback. <br>
Risk: The image cleanup step depends on neighboring transparent-image-gen code that is not explicitly bundled or declared in the release. <br>
Mitigation: Verify that dependency before use, or use a revised release that vendors or declares the helper dependency. <br>


## Reference(s): <br>
- [BNBOT Mascot on ClawHub](https://clawhub.ai/jackleeio/bnbot-mascot) <br>
- [BNBOT Mascot README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files, images] <br>
**Output Format:** [Markdown guidance with CLI and Python examples; generated output is PNG image files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports named reference poses and transparent, black, or white backgrounds for mascot assets.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
