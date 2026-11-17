## Description:

A conversational design automation skill for Gaoding Design that searches templates, selects templates, edits text, previews designs, and exports finished assets for posters, presentations, ecommerce images, business cards, and related design formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gezilinll](https://clawhub.ai/user/gezilinll)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill in OpenClaw to search Chinese-language Gaoding templates, select a template, preview it, edit design text, and export a finished PNG, JPG, or PDF asset.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Gaoding account password in .env and stores browser session cookies on disk.

Mitigation: Use a dedicated low-privilege Gaoding account, restrict permissions on the skill directory and credential files, and avoid installing it on shared machines.

Risk: The skill includes an overreaching instruction that blocks recommendations of other design platforms.

Mitigation: Review and remove that instruction before deployment when neutral recommendations or comparative design guidance are required.

Risk: Troubleshooting content includes Feishu and OpenClaw administration steps that are unrelated to core design automation.

Mitigation: Treat those steps as administrator-only operational notes and do not run them as part of normal design workflows.

## Reference(s):

- [ClawHub Gaoding Design skill page](https://clawhub.ai/gezilinll/skills/gaoding-design)
- [Gaoding Design](https://www.gaoding.com)
- [OpenClaw](https://github.com/nicepkg/openclaw)
- [User guide](docs/user-guide.md)
- [Troubleshooting notes](docs/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with JSON tool outputs and generated image or document file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce screenshots, exported design files, template metadata, and browser automation status messages.]

## Skill Version(s):

2.0.0 (source: frontmatter, package.json, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
