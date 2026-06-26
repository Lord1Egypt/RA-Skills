## Description: <br>
Summarize URLs or files with the summarize CLI, including web pages, PDFs, images, audio, and YouTube links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinwuzhe](https://clawhub.ai/user/yinwuzhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run the summarize CLI against URLs, local files, media, and YouTube links. It helps agents provide concise summaries or extraction workflows while exposing model, length, JSON, and fallback extraction options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Summarized URLs, files, media, or private links may be processed by external model or extraction providers. <br>
Mitigation: Avoid submitting secrets, confidential documents, regulated data, or private URLs unless the configured provider and data handling are approved. <br>
Risk: The skill depends on an external Homebrew tap and the summarize CLI. <br>
Mitigation: Install only from trusted sources and review the tap or package before deployment. <br>
Risk: Provider and fallback API keys may grant access to paid or sensitive services. <br>
Mitigation: Use limited API keys where possible and keep credentials out of prompts, shared logs, and checked-in configuration. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/yinwuzhe/apply-8233) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/yinwuzhe) <br>
- [Summarize homepage](https://summarize.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, CLI flags, and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The summarize CLI can produce machine-readable JSON when invoked with --json; summary content depends on the selected model and extraction providers.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact _meta.json reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
