## Description:

Creates and publishes styled GitHub Pages blog posts by generating HTML posts, updating the blog index, and committing and pushing changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[t3mr0i](https://clawhub.ai/user/t3mr0i)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, publishing agents, and blog maintainers use this skill to draft styled HTML posts, add index entries, and publish updates to a GitHub Pages blog with git.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish generated content to a hardcoded GitHub Pages repository on broad blog-post prompts.

Mitigation: Before execution, require review of the exact changed files, destination repository, branch, commit, and public URL; prefer a review branch or pull request instead of direct pushes to master.

Risk: The default repository, branch, domain, branding, and locale may not match the user's intended blog.

Mitigation: Install or run the skill only for the Clankr0i/clank-blog setup, or first customize the repository, branch, domain, branding, and locale values.

## Reference(s):

- [Clank Blog Post on ClawHub](https://clawhub.ai/t3mr0i/skills/clank-blog-post)
- [Clank Blog GitHub Pages URL template](https://clankr0i.github.io/clank-blog/{slug}.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTML, CSS, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires git; defaults to the Clankr0i/clank-blog repository, master branch, GitHub Pages deployment, and German-localized blog templates unless customized.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
