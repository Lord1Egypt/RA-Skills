## Description:

Article To Html turns articles or notes into mobile-readable, visually styled HTML infographics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[partigle](https://clawhub.ai/user/partigle)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creators use this skill to condense articles, posts, or notes into self-contained mobile-first HTML infographics for browser preview and screenshot delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The screenshot workflow can expose a local directory or leave a local HTTP server running.

Mitigation: Serve only a dedicated temporary output directory on 127.0.0.1, stop the server after screenshots, and clean up generated files.

Risk: Some templates contact Google Fonts despite the skill describing self-contained HTML output.

Mitigation: Remove or replace remote font imports when offline, private, or no-third-party-network rendering is required.

Risk: Sample output may include an unrelated install command that is not part of this skill's normal workflow.

Mitigation: Treat sample outputs as examples only and review commands before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/partigle/skills/article-to-html)
- [Publisher Profile](https://clawhub.ai/user/partigle)
- [README](artifact/README.md)
- [Quick Start](artifact/docs/01-快速开始.md)
- [Design Specification](artifact/docs/02-设计规范.md)
- [Technical Constraints](artifact/rules/01-技术底线.md)
- [Screenshot Workflow](artifact/rules/02-截图流程.md)
- [Style Inspiration](artifact/rules/03-风格灵感.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Self-contained HTML files with embedded CSS, plus workflow guidance and optional PNG screenshot output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Mobile-first 1080px-wide infographic layout with post-processing for CSS, sizing, and screenshot readiness.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
