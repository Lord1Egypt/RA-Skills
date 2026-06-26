## Description: <br>
Enterprise-grade browser automation for OpenClaw with automatic tab cleanup, retries, smart waiting, concurrency locking, and configurable browser settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BodaFu](https://clawhub.ai/user/BodaFu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to automate OpenClaw browser workflows such as web search, page fetching, multi-page processing, screenshots, PDFs, and form filling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports that user-supplied URLs, search text, form values, and profile names are used in shell command strings, creating a local command-execution risk. <br>
Mitigation: Use the skill only with trusted inputs in a dedicated low-privilege browser profile until the scripts use safe argument passing. <br>
Risk: Form automation may log or pass sensitive form values through command execution and console output. <br>
Mitigation: Avoid passwords, tokens, and sensitive personal data until form-value logging is redacted and input handling is hardened. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/BodaFu/browser-automation-v2) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance and command-line output with generated screenshot and PDF file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scripts depend on OpenClaw browser profile settings and environment variables for timeout, retries, profile, and debug logging.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and artifact/SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
