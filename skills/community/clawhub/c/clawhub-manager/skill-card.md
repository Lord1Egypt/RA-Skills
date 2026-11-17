## Description:

Clawhub Manager helps agents manage ClawHub skills by searching, inspecting, listing, publishing, and deleting skills through the ClawHub CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[franklu0819-lang](https://clawhub.ai/user/franklu0819-lang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to manage ClawHub skill releases, inspect published skill metadata, search the ClawHub catalog, and list local installed skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scripts can publish or delete ClawHub skills using the current clawhub login.

Mitigation: Run publish and delete commands only from the intended account and workspace, and review the target slug and version before execution.

Risk: The bundled test script can unintentionally publish test content to ClawHub.

Mitigation: Run scripts/test-security-scan.sh only with a mocked publish command, a dry-run or scan-only change, or an account where publishing test content is acceptable.

Risk: The built-in security scan is a convenience check and may not catch every secret or unsafe credential-like example.

Mitigation: Run independent secret scanning before publishing and rotate any example key if it was ever real.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/franklu0819-lang/skills/clawhub-manager)
- [README](README.md)
- [Security guide](SECURITY.md)
- [Usage examples](EXAMPLES.md)
- [Changelog](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown guidance with bash command examples and optional JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the clawhub CLI; JSON inspection output also requires jq.]

## Skill Version(s):

1.2.0 (source: server release metadata, SKILL.md frontmatter, artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
