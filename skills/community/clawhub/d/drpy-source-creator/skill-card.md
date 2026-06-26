## Description: <br>
Helps developers create, modify, and debug JavaScript-based drpy sources for TVBox, Haikuo, ZYPlayer, and similar players. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuluoxci](https://clawhub.ai/user/yuluoxci) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and advanced media-tool users use this skill to create, validate, minify, and troubleshoot drpy source definitions for video, audio-book, comic, and novel sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local helper scripts may be unsafe on untrusted or oddly named files. <br>
Mitigation: Review helper scripts before execution and run the minifier only on trusted, well-named files until the shell invocation is fixed. <br>
Risk: Examples and debugging workflows can expose cookies, headers, URLs, or other sensitive request data. <br>
Mitigation: Avoid putting personal browser cookies into shared configs and redact headers, cookies, and URLs before sharing logs. <br>
Risk: Example sources and parser URLs may depend on third-party sites or services. <br>
Mitigation: Verify each third-party parser URL and target site before using an example source. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yuluoxci/drpy-source-creator) <br>
- [Attributes Reference](references/attributes.md) <br>
- [Template Inheritance Reference](references/templates.md) <br>
- [Parsing Reference](references/parsing.md) <br>
- [Troubleshooting Reference](references/troubleshooting.md) <br>
- [Formatting Reference](references/formatting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with JavaScript, Python, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated drpy rule examples, validation steps, minification commands, and debugging notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
