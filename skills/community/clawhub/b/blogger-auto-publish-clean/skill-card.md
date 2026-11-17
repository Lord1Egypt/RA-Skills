## Description:

Automatically publish Markdown articles to Google Blogger with batch publishing, draft management, and automatic HTML conversion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rainco2008](https://clawhub.ai/user/rainco2008)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to configure Blogger OAuth access and publish Markdown posts as drafts or live Blogger articles. It is suited for blog automation workflows that need repeatable publishing commands, post metadata, and Markdown-to-HTML conversion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish any local file path it is given.

Mitigation: Use a dedicated Markdown post directory and review file paths before running publish commands, especially when prompts or generated commands suggest paths.

Risk: OAuth credentials and tokens are sensitive and may be weakly protected.

Mitigation: Keep credentials.json and token.json private with restrictive filesystem permissions, and avoid copying tokens through shared or temporary locations.

Risk: An unauthenticated webhook-style example could expose publishing capability if deployed as-is.

Mitigation: Do not use webhook examples without authentication and access controls.

Risk: Unpinned dependencies can change behavior across installations.

Mitigation: Pin and review dependencies before production use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rainco2008/skills/blogger-auto-publish-clean)
- [Publisher Profile](https://clawhub.ai/user/rainco2008)
- [API Reference](references/REFERENCES.md)
- [Examples](references/EXAMPLES.md)
- [Setup Guide](SETUP.md)
- [Google Cloud Console](https://console.cloud.google.com/)
- [Blogger](https://www.blogger.com/)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide OAuth setup and Blogger publishing operations that create, list, or manage posts when the user runs the generated commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
