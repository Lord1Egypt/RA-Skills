## Description: <br>
Standalone CMS for GitHub Pages Jekyll blogs - browse, edit, create posts, and deploy with one click. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amrree](https://clawhub.ai/user/amrree) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site operators use BlogStudio to manage GitHub Pages Jekyll content through a local CMS interface that can browse, edit, preview, create, publish, and sync posts, guides, and pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: GitHub credentials can be exposed to browser-facing application code. <br>
Mitigation: Use only a narrowly scoped token for the intended repository, and avoid broad personal GitHub credentials until token handling is moved server-side. <br>
Risk: The CMS can publish or delete content directly in the live repository. <br>
Mitigation: Review changes before publishing, confirm the target repository and branch, and run it only where direct main-branch updates are acceptable. <br>


## Reference(s): <br>
- [BlogStudio ClawHub Skill Page](https://clawhub.ai/amrree/skills/blog-studio) <br>
- [Publisher Profile](https://clawhub.ai/user/amrree) <br>
- [Target GitHub Pages Site](https://thesolai.github.io) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and file-oriented guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include operational steps for running a local CMS and managing GitHub-backed Jekyll content.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, release metadata, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
