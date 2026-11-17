## Description:

Embodied Ai Weekly helps agents compile and publish weekly embodied AI reports by gathering recent arXiv papers and GitHub project activity, generating Markdown and HTML summaries with charts and figures, and preparing GitHub Pages updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jessy-huang](https://clawhub.ai/user/jessy-huang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, and research teams use this skill to produce a weekly embodied AI briefing across seven research directions, recent arXiv papers, GitHub repository activity, visual summaries, and GitHub Pages publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The publishing workflow can push broad local repository changes to GitHub Pages.

Mitigation: Require a dry run, inspect generated files and staged diffs, and stage only the expected report, archive, and latest paths before pushing.

Risk: The skill can publish generated reports to a public GitHub Pages site.

Mitigation: Use narrowly scoped GitHub credentials and require explicit confirmation before any public push.

Risk: The generated HTML may depend on the Chart.js CDN.

Mitigation: Pin the CDN dependency to an approved version or remove the external dependency before release.

## Reference(s):

- [ArXiv search guide](references/arxiv_search_guide.md)
- [GitHub search guide](references/github_search_guide.md)
- [HTML report style guide](references/html_template_guide.md)
- [ClawHub skill page](https://clawhub.ai/jessy-huang/skills/embodied-ai-weekly)
- [arXiv recent robotics papers](https://arxiv.org/list/cs.RO/recent)
- [arXiv recent computer vision papers](https://arxiv.org/list/cs.CV/recent)
- [GitHub repository search API](https://api.github.com/search/repositories)
- [Chart.js CDN dependency](https://cdn.jsdelivr.net/npm/chart.js)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and HTML reports with inline shell commands and GitHub Pages file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates weekly report artifacts and may prepare public GitHub Pages updates; review generated files and diffs before publishing.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
