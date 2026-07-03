## Description: <br>
Jekyll blog authoring UI - manage posts, drafts, tags, and publishing workflow for static sites. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amrree](https://clawhub.ai/user/amrree) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, site maintainers, and technical writers use this skill to manage Jekyll or static-site blog posts, drafts, tags, previews, and publishing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local post files can be created, edited, deleted, and published through the skill. <br>
Mitigation: Run only against a trusted Jekyll working copy, keep backups or version control available, and review changes before publishing. <br>
Risk: Publishing workflows can run git commands and push changes to GitHub Pages. <br>
Mitigation: Use a least-privilege git credential, review commit contents, and avoid running publish actions from an untrusted workspace. <br>
Risk: The web server and generation features may expose local operations or call external research and AI services. <br>
Mitigation: Keep the server bound to a trusted local environment, do not expose it to a network, and review any generated content or external-service use before saving. <br>
Risk: The artifact may look for a MiniMax API key at a hard-coded local path. <br>
Mitigation: Store credentials securely, verify the expected key path before use, and rotate credentials if the runtime environment is not fully trusted. <br>


## Reference(s): <br>
- [Blog Composer on ClawHub](https://clawhub.ai/amrree/skills/blog-composer) <br>
- [TheSolAI blog](https://thesolai.github.io) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown content, Jekyll post files, configuration guidance, and local run/publish commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and write local Jekyll blog files, run git publishing commands, and call external research or AI services when used.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
