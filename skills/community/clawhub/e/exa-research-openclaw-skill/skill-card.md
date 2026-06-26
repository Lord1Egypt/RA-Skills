## Description: <br>
Use the local `exa` CLI to search the live web, ask grounded questions with citations, fetch page contents, find similar links, retrieve Exa code context, or manage Exa research tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[WKenya](https://clawhub.ai/user/WKenya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and researchers use this skill to route current web research, cited answer synthesis, page extraction, similar-link discovery, code context retrieval, and Exa research workflows through the local Exa CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs the local Exa CLI selected by EXA_BIN or PATH. <br>
Mitigation: Install Exa from a trusted source and verify EXA_BIN or PATH before using the wrapper. <br>
Risk: The skill requires an Exa API key. <br>
Mitigation: Keep the key in OpenClaw secrets or a locked-down file and avoid committing credentials. <br>
Risk: Web research, raw API calls, private URLs, or proprietary content may be sent to the Exa service. <br>
Mitigation: Prefer scoped Exa commands, avoid raw calls unless needed, and only send sensitive content when Exa processing is acceptable. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/WKenya/exa-research-openclaw-skill) <br>
- [Exa CLI upstream project](https://github.com/jdegoes/exa) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and CLI output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the local exa CLI and EXA_API_KEY; results may include live web links, citations, page content, highlights, summaries, code context, and research task data.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
