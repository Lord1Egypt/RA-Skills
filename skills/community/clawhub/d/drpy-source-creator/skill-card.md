## Description:

Helps agents create, modify, validate, and debug drpy JavaScript source rules for TVBox, Haikuo Vision, ZYPlayer, and similar media players.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuluoxci](https://clawhub.ai/user/yuluoxci)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and advanced media-player users use this skill to build and troubleshoot drpy source configurations, including selectors, template inheritance, parsing behavior, local proxy settings, and source validation for video, audiobook, comic, and novel content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Helper scripts may be risky when used with untrusted filenames or inputs.

Mitigation: Review helper scripts before execution and avoid running minify_drpy.js with untrusted filenames.

Risk: Examples and debugging workflows can expose playback URLs, cookies, headers, or request details.

Mitigation: Do not hardcode personal cookies or share logs that contain sensitive playback URLs, headers, cookies, or request details.

Risk: Site analysis and parser-service workflows can contact public websites or transmit playback URLs and headers to parser services.

Mitigation: Restrict analyze_site.py to public sites you intend to contact, and use parser services only when you are comfortable sending playback URLs and related headers to them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuluoxci/skills/drpy-source-creator)
- [Attributes reference](references/attributes.md)
- [Template inheritance reference](references/templates.md)
- [Parsing reference](references/parsing.md)
- [Troubleshooting reference](references/troubleshooting.md)
- [Formatting reference](references/formatting.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript snippets, configuration examples, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce drpy rule examples, validation steps, minification commands, and site-analysis guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
