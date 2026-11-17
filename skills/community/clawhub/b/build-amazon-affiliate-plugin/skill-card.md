## Description:

Create a production-ready WordPress plugin that displays Amazon product ads when users insert Amazon affiliate links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imjohnathanblog-spec](https://clawhub.ai/user/imjohnathanblog-spec)

### License/Terms of Use:

GPL v2 or later

## Use Case:

Developers and site operators use this skill to generate an Amazon Associates WordPress plugin that detects Amazon links, extracts ASINs, renders ad units, configures affiliate and PA-API settings, and supports Gutenberg blocks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated plugin code handles affiliate ad insertion in WordPress content and stores Amazon PA-API credentials.

Mitigation: Review generated code before use, store PA-API keys only in a properly secured WordPress admin environment, and verify sanitization, escaping, nonces, and capability checks before deployment.

Risk: The artifact includes Gutenberg build dependencies that may become outdated.

Mitigation: Update and audit the WordPress block npm dependencies before building or deploying generated block assets.

Risk: The source skill directs output to a hard-coded local workspace path.

Mitigation: Change the generated output directory to the target project workspace before running file-generation steps.

## Reference(s):

- [Amazon PA-API Integration Guide](references/AMAZON_API.md)
- [Ad Symbiont Plugin Specification](references/PLUGIN_SPEC.md)
- [ClawHub Skill Page](https://clawhub.ai/imjohnathanblog-spec/skills/build-amazon-affiliate-plugin)

## Skill Output:

**Output Type(s):** [Code, Files, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with generated WordPress plugin files and setup instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces PHP plugin code, CSS and JavaScript assets, installation guidance, and expansion options.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
