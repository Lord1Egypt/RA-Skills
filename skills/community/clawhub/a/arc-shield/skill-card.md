## Description: <br>
Output sanitization for agent responses - prevents accidental secret leaks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arc-claw-bot](https://clawhub.ai/user/arc-claw-bot) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use Arc Shield to scan outbound agent messages for accidentally exposed secrets, tokens, keys, passwords, and PII before sending to external channels. It supports strict blocking, redaction, and reporting workflows for command-line and OpenClaw-style integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server security review reports that an advertised strict blocking path can still print the sensitive message it claims to block. <br>
Mitigation: Do not rely on strict mode alone as a blocking sanitizer in outbound pipelines; use redaction or discard and verify stdout before connecting the tool to external senders. <br>
Risk: Secret detection is pattern-based and may miss new or context-dependent secret formats. <br>
Mitigation: Keep patterns current, test custom patterns before deployment, and pair the filter with agent instructions that avoid including secrets in responses. <br>


## Reference(s): <br>
- [Arc Shield ClawHub listing](https://clawhub.ai/arc-claw-bot/arc-shield) <br>
- [README](artifact/README.md) <br>
- [Quick Reference](artifact/QUICKREF.md) <br>
- [Installation Guide](artifact/INSTALLATION.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text, Markdown guidance, shell snippets, sanitized text, and optional JSON reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local command-line filters can pass through, block, redact, or report on scanned outbound content.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
