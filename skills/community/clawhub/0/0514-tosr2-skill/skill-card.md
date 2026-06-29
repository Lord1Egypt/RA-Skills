## Description: <br>
Summarize URLs or files with the summarize CLI (web, PDFs, images, audio, YouTube). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinwuzhe](https://clawhub.ai/user/yinwuzhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to call the summarize CLI for summaries of web pages, PDFs, images, audio, local files, and YouTube links. It also helps configure models, provider API keys, output length, JSON output, and optional extraction services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Summarized URLs or local files may be sent to external model or extraction providers. <br>
Mitigation: Avoid confidential, regulated, or private content unless the selected CLI and provider settings meet the user's privacy and compliance requirements. <br>
Risk: The skill depends on an external summarize CLI and optional provider integrations. <br>
Mitigation: Install only from trusted sources, confirm the binary and configured providers, and review generated summaries before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/yinwuzhe/skills/0514-tosr2-skill) <br>
- [Summarize CLI homepage](https://summarize.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets; the CLI can produce plain text or JSON summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the external summarize binary. Optional provider and extraction API keys change what services may process input content.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
