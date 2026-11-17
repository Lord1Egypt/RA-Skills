## Description:

Prompt injection and malware detection filter for external content. Scans text, files, or URLs for 20+ attack patterns including instruction overrides, credential exfiltration, persona hijacking, encoded payloads, fake system messages, and invisible character injection. Returns JSON with risk level and sanitized text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bryantegomoh](https://clawhub.ai/user/bryantegomoh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill before processing external text, files, URLs, user pastes, articles, or API responses to detect prompt-injection and malicious-content patterns and decide whether to block, review, or continue.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: URL mode can read local files or private network resources and return their contents.

Mitigation: Review before installing or using in automated workflows; only pass trusted, intended URLs and prefer a sandbox that blocks file:// URLs, localhost, private networks, link-local metadata addresses, and redirects to those destinations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bryantegomoh/skills/content-security-filter)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [JSON report with safe status, risk level, findings, sanitized text, and scanned character count.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exit code 0 indicates safe content; exit code 1 indicates a detected threat.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
