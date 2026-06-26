## Description: <br>
Summarize URLs or files with the summarize CLI, including web pages, PDFs, images, audio, and YouTube links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinwuzhe](https://clawhub.ai/user/yinwuzhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and other agent users use this skill to invoke the summarize CLI for concise summaries of URLs, local files, media, and YouTube links, with optional provider and extraction-service configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Summarized files, private URLs, media, or YouTube content may be processed by the selected AI provider and optional extraction services. <br>
Mitigation: Avoid submitting confidential or sensitive content unless the selected provider and optional Firecrawl or Apify services are approved for that data. <br>
Risk: The skill relies on the external summarize Homebrew tap and installed CLI binary. <br>
Mitigation: Install only when the tap and binary source are trusted, and review updates before use in managed environments. <br>
Risk: Provider and extraction-service API keys are required for some workflows. <br>
Mitigation: Configure only the credentials needed for the chosen workflow and keep keys out of shared logs, prompts, and committed config files. <br>


## Reference(s): <br>
- [Summarize homepage](https://summarize.sh) <br>
- [ClawHub skill page](https://clawhub.ai/yinwuzhe/0512-03-tos2-skill) <br>
- [Publisher profile](https://clawhub.ai/user/yinwuzhe) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce machine-readable JSON when the summarize CLI is run with --json; output length can be controlled with CLI flags.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
