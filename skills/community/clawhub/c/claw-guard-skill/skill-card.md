## Description: <br>
Safety Guard URLs or files with the safety-guard CLI (web, PDFs, images, audio, YouTube). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[John-niu-07](https://clawhub.ai/user/John-niu-07) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to summarize or inspect URLs, local files, PDFs, images, audio, and YouTube links through the safety-guard CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided URLs, files, and YouTube content may be sent to the selected AI provider or optional fallback extraction services. <br>
Mitigation: Use only approved providers and avoid confidential or regulated material unless those services are approved for that data. <br>
Risk: The skill depends on the safety-guard CLI and its Homebrew source. <br>
Mitigation: Install only when the CLI and Homebrew tap are trusted in the target environment. <br>


## Reference(s): <br>
- [Safety Guard homepage](https://safety-guard.sh) <br>
- [ClawHub skill page](https://clawhub.ai/John-niu-07/claw-guard-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports length controls, maximum output token limits, extract-only mode, and optional provider-backed fallbacks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
