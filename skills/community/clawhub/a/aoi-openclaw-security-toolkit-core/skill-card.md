## Description:

Run local-only fail-closed security checks to detect and report data leaks, secrets, egress risks, and prompt injections before publishing or committing code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edmonddantesj](https://clawhub.ai/user/edmonddantesj)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill before commits, releases, or ClawHub publishing to scan local repositories, staged diffs, scripts, skills, and inbound text for accidental leakage, exposed credentials, unexpected egress patterns, and prompt-injection cues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local repositories and paths selected for scanning, and JSON output may include redacted snippets or suspicious URLs from local files.

Mitigation: Run it only against repositories or paths intended for review, and use explicit --paths and --exclude settings for sensitive workspaces.

Risk: Pattern-based secret, egress, and prompt-injection scans can produce false positives or miss risks outside the configured rules.

Mitigation: Review PASS/WARN/BLOCK findings manually and tune the rule files for the target repository before relying on the result for release decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/edmonddantesj/skills/aoi-openclaw-security-toolkit-core)
- [Security Policy (Core)](docs/SECURITY_POLICY.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [CLI PASS/WARN/BLOCK status, optional Markdown report, and optional JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are capped and secret excerpts are redacted or omitted from reports.]

## Skill Version(s):

0.1.6 (source: server release evidence, package.json, _meta.json, integrity_manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
