## Description:

Create, edit, enhance, convert, and manage images, design resources, and visual assets with Codia Design Skills and the Codia Open API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codia-ai](https://clawhub.ai/user/codia-ai)

### License/Terms of Use:

MIT

## Use Case:

Developers and AI-agent users use this skill pack to route design, image, PDF, SVG, account, and usage requests to the Codia Design CLI and Codia Open API. It supports asset generation and editing, background removal, image inspection, editable design extraction, PDF-to-PPT conversion, and account credit management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on installing and running the Codia Design CLI and authenticating it with a Codia API key.

Mitigation: Install only from trusted Codia sources, prefer pinned or reviewed releases, and avoid exposing API keys in chat, shell history, logs, or the local auth config file.

Risk: Billable API operations and auto-recharge settings can affect account credits or spending.

Mitigation: Check credit estimates and balances before paid operations, and require explicit user approval before enabling or changing auto-recharge.

Risk: Design, image, PDF, and URL inputs may be sent to the Codia Open API through the local CLI.

Mitigation: Use only user-provided or authorized files and URLs, keep outputs in requested directories, and report API or download validation failures directly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/codia-ai/skills/codia-design-skills)
- [Codia API reference](https://codia.ai/api-reference#description/introduction)
- [README](artifact/README.md)
- [Security and data handling](artifact/SECURITY.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown, JSON, files]

**Output Format:** [Markdown guidance with inline shell commands, local file paths, downloaded asset paths, returned URLs, task IDs, and compact JSON summaries when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local image, SVG, PPTX, or JSON files through the Codia Design CLI; does not expose API keys or raw local auth configuration.]

## Skill Version(s):

0.1.4 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
