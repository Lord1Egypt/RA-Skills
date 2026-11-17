## Description:

Publish AI-generated content, including HTML pages, Markdown reports, multi-file sites, dashboards, and visualizations, to a shareable URL using Artidrop.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wenguo17](https://clawhub.ai/user/wenguo17)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Artidrop to publish generated HTML, Markdown, reports, dashboards, and multi-file sites as shareable web pages. It is intended for explicit publish, share, or host requests, not raw chat responses or generic file storage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and uses an unpinned third-party npm CLI that handles generated content and optional credentials.

Mitigation: Review and pin the Artidrop CLI version before broad use, and install only when the target environment accepts third-party CLI handling of content.

Risk: Publishing sends user-selected content to Artidrop and may make it accessible through a shareable URL.

Mitigation: Avoid publishing secrets, personal data, internal documents, or proprietary material unless the user explicitly intends to share it; use private visibility for sensitive content when authenticated access is available.

## Reference(s):

- [Artidrop website](https://artidrop.ai)
- [Artidrop CLI npm package](https://www.npmjs.com/package/artidrop)
- [Artidrop skill on ClawHub](https://clawhub.ai/wenguo17/skills/artidrop)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and returned shareable URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include published Artidrop URLs and optional JSON metadata when the Artidrop CLI is run with --json.]

## Skill Version(s):

1.3.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
