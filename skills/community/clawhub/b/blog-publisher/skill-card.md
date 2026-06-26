## Description: <br>
Publishes Obsidian notes or text to a dev blog by converting Markdown to .mdoc, assisting with image prompts and processing, and guiding preview review before production deployment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sonim1](https://clawhub.ai/user/sonim1) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and blog publishers use this skill to turn Obsidian drafts or supplied text into bilingual .mdoc blog posts, prepare frontmatter and images, review a preview deployment, and publish approved changes to the production blog. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill grants an agent broad publishing authority over the specified dev-blog repository and production site. <br>
Mitigation: Before any push, require git status and git diff review, stage only intended files, publish to the preview branch first, and merge to main only after explicit approval. <br>
Risk: Drafts, prompts, and images may be sent through external browser, image-generation, Google, OpenRouter, OpenAI, or Telegram services. <br>
Mitigation: Explicitly choose the image provider and avoid sending sensitive drafts or images to external services unless those data flows are approved. <br>
Risk: Force-pushing the preview branch can overwrite remote preview history. <br>
Mitigation: Treat force-pushes as separately approved actions and confirm the target branch before pushing. <br>


## Reference(s): <br>
- [Blog Format Reference](references/blog-format.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/sonim1/blog-publisher) <br>
- [Publisher Profile](https://clawhub.ai/user/sonim1) <br>
- [Production Blog](https://sonim1.com) <br>
- [Preview Deployment](https://it-blog-git-preview-bumfoo-s-team.vercel.app) <br>
- [Google Generative Language API Endpoint](https://generativelanguage.googleapis.com/v1beta/models) <br>
- [OpenRouter Chat Completions API Endpoint](https://openrouter.ai/api/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with YAML frontmatter, .mdoc content, image prompts, file paths, and shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or modify blog content files and image assets, and may propose git operations for preview and production publishing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
