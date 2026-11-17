## Description:

Run a self-contained Chinese and international AI news workflow inside the current workspace. Use when the user wants either high-frequency RSS capture only or scheduled report delivery only, with cumulative Excel outputs and a merged Word brief, without relying on an external local repository path.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nighmat1220](https://clawhub.ai/user/nighmat1220)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to collect Chinese and international AI news from RSS or Atom sources, deduplicate items, generate AI-assisted summaries and impact scores, and produce cumulative Excel reports plus a merged Word brief.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Article content and ARK_API_KEY can be sent to a configurable model endpoint.

Mitigation: Use only a trusted HTTPS ARK_API_BASE, keep ARK_API_BASE unset unless an override is required, and use --disable-ai for private or licensed content.

Risk: Feed configuration can include arbitrary URLs, custom headers, basic authentication, and disabled TLS verification.

Mitigation: Inspect config/sources.json and config/international_sources.json before running, require trusted feed URLs, and do not set verify_ssl=false outside a controlled test environment.

Risk: The workflow writes collected article content and generated reports into the selected workspace.

Mitigation: Run it in a trusted workspace with appropriate access controls and retention expectations for data, reports, snapshots, and state files.

## Reference(s):

- [Commands](references/commands.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Markdown guidance with bash commands; generated JSONL, Excel, and Word files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates workspace-scoped data, reports, snapshots, and state files; AI generation can be disabled with --disable-ai.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
