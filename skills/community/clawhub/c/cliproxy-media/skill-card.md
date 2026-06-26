## Description: <br>
CLIProxy Media helps agents analyze images and PDFs through a configured CLIProxy-compatible Anthropic Messages endpoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bencoremans](https://clawhub.ai/user/bencoremans) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect local images, image URLs, and PDF files, ask questions about their contents, and receive text analysis through a CLIProxy-compatible endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images, PDFs, URLs, and prompts are sent to the configured proxy or API endpoint. <br>
Mitigation: Use only CLIProxy-compatible endpoints you control or trust, and avoid sensitive, regulated, proprietary, or private documents unless the endpoint's access, logging, retention, and billing terms are acceptable. <br>
Risk: Untrusted callers could route requests to an unexpected endpoint by changing CLIPROXY_URL or using --url. <br>
Mitigation: Do not allow untrusted users to set CLIPROXY_URL or --url; pin the endpoint in trusted execution environments. <br>


## Reference(s): <br>
- [CLIProxy Media ClawHub release](https://clawhub.ai/bencoremans/cliproxy-media) <br>
- [Publisher profile](https://clawhub.ai/user/bencoremans) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Text or streamed text responses, with Markdown examples and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports images, image URLs, PDFs, optional system prompts, model overrides, endpoint overrides, streaming, and max-token controls.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
