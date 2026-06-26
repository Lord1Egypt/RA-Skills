## Description: <br>
Runs local-only, fail-closed checks to detect and report data leaks, secrets, egress risks, and prompt injection risks before publishing or committing code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edmonddantesj](https://clawhub.ai/user/edmonddantesj) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to run local repository checks before commits, publishing, or reviewing inbound text for secret, egress, allowlist, and prompt injection risks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scanning broad or sensitive workspaces can expose local file paths or report metadata. <br>
Mitigation: Run it only on projects intended for scanning, narrow scope with --paths and --exclude, and keep generated reports private. <br>
Risk: Allowlist and exclude patterns from untrusted repositories can hide files from review or cause slow scans. <br>
Mitigation: Review allowlist and exclude patterns before use, especially for release checks or sensitive workspaces. <br>
Risk: Detection-only checks can produce false positives or miss risks outside the bundled patterns. <br>
Mitigation: Treat PASS, WARN, and BLOCK results as review inputs and update the rule files when project-specific risks are known. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/edmonddantesj/aoi-openclaw-security-toolkit-core) <br>
- [Security Policy (Core)](docs/SECURITY_POLICY.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [CLI text or JSON output with optional Markdown report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses PASS, WARN, and BLOCK grades with exit codes 0, 1, and 2; generated reports omit excerpts to reduce secret leakage.] <br>

## Skill Version(s): <br>
0.1.6 (source: package.json, _meta.json, skill.js, integrity_manifest.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
