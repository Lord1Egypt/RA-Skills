## Description: <br>
Summarize URLs or files with the summarize CLI for web pages, PDFs, images, audio, and YouTube links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinwuzhe](https://clawhub.ai/user/yinwuzhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to generate concise summaries from URLs, local files, PDFs, images, audio, and YouTube links through the summarize CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Summarized content may be sent to external AI providers or optional extraction services. <br>
Mitigation: Avoid confidential files, private URLs, regulated data, and secrets unless the configured provider and any Firecrawl or Apify fallback service are trusted for that data. <br>
Risk: The skill depends on an upstream CLI and Homebrew formula. <br>
Mitigation: Review the upstream summarize CLI or Homebrew formula before installation when strong supply-chain assurance is required. <br>
Risk: The skill requires sensitive provider credentials for selected models and optional services. <br>
Mitigation: Use scoped credentials where available and configure only the provider keys needed for the intended workflow. <br>


## Reference(s): <br>
- [Summarize homepage](https://summarize.sh) <br>
- [ClawHub skill page](https://clawhub.ai/yinwuzhe/apply-8138) <br>
- [Publisher profile](https://clawhub.ai/user/yinwuzhe) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples; the summarize CLI may also produce JSON when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports length controls, maximum output token controls, extract-only mode, provider model selection, and optional external extraction services.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
