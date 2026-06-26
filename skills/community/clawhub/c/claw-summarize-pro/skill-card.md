## Description: <br>
Summarize URLs or files with the summarize CLI, including web pages, PDFs, images, audio, and YouTube links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[williamwang-wh](https://clawhub.ai/user/williamwang-wh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and other agent users use this skill to call the summarize CLI for concise summaries of URLs, local files, and media sources, with optional model and extraction settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local files, private URLs, or media may be sent to configured model or extraction providers. <br>
Mitigation: Do not use the skill with confidential documents, secrets, private URLs, regulated data, or sensitive media unless external processing is acceptable. <br>
Risk: The skill depends on a third-party Homebrew tap and the summarize CLI. <br>
Mitigation: Install only when the publisher, tap, and CLI are trusted for the intended environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/williamwang-wh/claw-summarize-pro) <br>
- [Summarize CLI Homepage](https://summarize.sh) <br>
- [Publisher Profile](https://clawhub.ai/user/williamwang-wh) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON output from the CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports summary length, output token limits, extraction-only mode, JSON output, and optional provider configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
