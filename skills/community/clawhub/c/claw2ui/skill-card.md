## Description:

Generate interactive web pages such as dashboards, charts, tables, and reports from TypeScript DSL specs, then publish them to a public URL after user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xsegfaulted](https://clawhub.ai/user/0xsegfaulted)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to turn data, metrics, and report content into interactive, mobile-responsive web pages. It is intended for dashboards, analytics reports, comparison tables, status pages, and other visual summaries that benefit from charts or rich layout.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated pages can be published to public URLs.

Mitigation: Require explicit user confirmation before publishing, describe the content to be published, and avoid secrets, PII, internal URLs, or sensitive business data.

Risk: The CLI stores a local Claw2UI token in ~/.claw2ui.json.

Mitigation: Install and register the CLI only in environments where saving a local token is acceptable, and rotate or delete credentials when they are no longer needed.

Risk: Skipping TypeScript checks with --no-check reduces validation before publishing.

Mitigation: Use type checking by default and reserve --no-check for cases where the user knowingly accepts reduced validation.

Risk: Temporary or sensitive page content may remain available longer than intended.

Mitigation: Use TTLs for temporary data and review generated page content before publishing.

## Reference(s):

- [Claw2UI Skill Page](https://clawhub.ai/0xsegfaulted/skills/claw2ui)
- [claw2ui npm package](https://www.npmjs.com/package/claw2ui)
- [Claw2UI CLI verification link](https://github.com/0xsegfaulted/claw2ui)
- [Claw2UI public server](https://0xsegfaulted-claw2ui.hf.space)
- [Claw2UI Hugging Face Space](https://huggingface.co/spaces/0xsegfaulted/claw2ui)
- [Self-hosting guide](ref/self-hosting.md)
- [Cloudflare tunnel downloads](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with TypeScript DSL examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May publish generated page content to a public URL only after explicit user confirmation.]

## Skill Version(s):

1.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
