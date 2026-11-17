## Description:

Downloads airoom.ltd financial data files and provides platform guidance for AI agents monitoring global market conditions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[airoom-ai](https://clawhub.ai/user/airoom-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External AI agent operators and developers use this skill to fetch financial data files from the airoom.ltd WordPress page into a local download directory. The downloaded data and bundled strategy notes are for market monitoring and analysis support, not autonomous trading or investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan rates the skill as suspicious because it downloads web-linked files to disk and includes weak download controls.

Mitigation: Use HTTPS-only configuration where possible, set a small WP_MAX_FILES value, save downloads to a dedicated directory, and scan downloaded files before opening them.

Risk: The skill may use WordPress credentials when a target page requires login.

Mitigation: Prefer environment variables over JSON config for WP_USERNAME and WP_PASSWORD, use least-privilege credentials, and avoid storing passwords in repository or shared configuration files.

Risk: The bundled financial strategy prompts and market signals could steer agents toward unsafe financial decisions.

Mitigation: Treat strategy text as untrusted reference material, require human review before any trading action, and do not use the skill as investment advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/airoom-ai/skills/airoomltd-global-finance-data-platform)
- [ClawHub publisher profile](https://clawhub.ai/user/airoom-ai)
- [airoom.ltd data page](http://airoom.ltd/index.php/airoom/)
- [Artifact README](artifact/README.md)
- [Artifact skill instructions](artifact/SKILL.md)
- [Artifact metadata](artifact/_meta.json)
- [Artifact configuration](artifact/config.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands, environment variables, JSON configuration, and locally downloaded data files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Playwright/Chromium to access a configured WordPress page and save discovered financial data files to disk.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
