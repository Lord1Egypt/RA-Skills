## Description: <br>
Publishes Markdown content into a Hugo blog as posts, daily reports, or weekly reports, with template-based front matter, optional cover image handling, and content-aware category, tag, and library suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redisread](https://clawhub.ai/user/redisread) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content authors use this skill to move finished Markdown drafts into configured Hugo content directories, generate or replace front matter, copy cover images, and prepare posts, daily reports, or weekly reports for publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Publishing to the wrong Hugo directory or template path can modify an unintended repository. <br>
Mitigation: Confirm HUGO_BLOG_DIR, content directory, and template settings with the configuration check before publishing. <br>
Risk: A same-named destination article may be overwritten and existing Markdown front matter may be replaced. <br>
Mitigation: Use git status, backups, or a draft copy before running the publishing workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/redisread/blog-push) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files with Hugo front matter, plus concise terminal guidance and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May copy cover image files and update destination Markdown files in the configured Hugo project.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
