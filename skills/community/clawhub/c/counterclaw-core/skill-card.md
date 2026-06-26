## Description: <br>
Defensive interceptor for prompt injection and basic PII masking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nickconstantinou](https://clawhub.ai/user/nickconstantinou) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use Counterclaw Core to screen agent inputs for common prompt injection patterns and check outputs for basic PII before messages or email content are sent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The protected email path can send through Gmail and depends on local credentials and gog CLI configuration. <br>
Mitigation: Verify CounterClaw imports correctly, test the helper with dry-run first, and use a dedicated or least-privilege Gmail account before allowing sends. <br>
Risk: Violations are logged persistently into OpenClaw memory. <br>
Mitigation: Install only when local logging to ~/.openclaw/memory/ is acceptable, and review stored logs according to the user's data handling policy. <br>
Risk: PII checks are basic and should not be treated as complete automatic redaction. <br>
Mitigation: Review outbound content before sending and do not rely on the scanner as the sole control for sensitive text. <br>


## Reference(s): <br>
- [Counterclaw Core on ClawHub](https://clawhub.ai/nickconstantinou/counterclaw-core) <br>
- [CounterClaw Core repository](https://github.com/nickconstantinou/counterclaw-core) <br>
- [counterclaw-core on PyPI](https://pypi.org/project/counterclaw-core/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Python dictionaries, CLI text, Markdown instructions, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Core scanning is offline; optional email helper behavior depends on local gog CLI configuration.] <br>

## Skill Version(s): <br>
1.1.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
