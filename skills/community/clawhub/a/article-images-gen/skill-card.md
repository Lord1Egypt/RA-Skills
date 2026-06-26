## Description: <br>
Generates hand-drawn, minimalist illustrations for Markdown articles or direct prompts using opencli Gemini with Grok fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redisread](https://clawhub.ai/user/redisread) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze Markdown articles, create illustration outlines and prompt files, generate 16:9 hand-drawn images, and insert image references into the source article. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted article or prompt text can become local shell command execution through opencli command strings. <br>
Mitigation: Install only for trusted article and prompt files until opencli calls use argument-array execution. <br>
Risk: The article workflow rewrites source Markdown files in place. <br>
Mitigation: Keep articles under version control or backed up, and review generated edits before publishing. <br>


## Reference(s): <br>
- [article-images-gen homepage](https://github.com/victor-skills/tree/main/skills/article-images-gen) <br>
- [ClawHub skill page](https://clawhub.ai/redisread/article-images-gen) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands] <br>
**Output Format:** [PNG image files, Markdown outline and prompt files, and updated Markdown article content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes generated assets under /tmp/imageGen by default, uses 16:9 landscape images, and creates an article backup before rewriting the article.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter states 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
