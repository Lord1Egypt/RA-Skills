## Description:

Configures China-region package mirrors for Python pip, npm, yarn, pnpm, cargo, Go modules, NuGet, RubyGems, Conda, Homebrew, Gradle, Maven, and Composer when dependency downloads are slow or regional mirror setup is requested.

This skill is ready for commercial/non-commercial use.

## Publisher:

[normdist-ai](https://clawhub.ai/user/normdist-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure selected package managers to use China-region mirrors, especially when dependency downloads are slow or projects need local package-source acceleration. The skill guides confirmation, environment checks, configuration commands, and post-change verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent global package-manager or shell configuration changes may affect future builds.

Mitigation: Prefer project-level settings when possible, show exact changes before execution, and back up existing configuration files first.

Risk: Mirror and source rewrites, including pip trusted-host settings and NuGet, Maven, Cargo, RubyGems, or shell profile edits, can change dependency trust and resolution behavior.

Mitigation: Use the skill only when China-region mirrors are intentional, confirm each selected mirror, and review the resulting configuration before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/normdist-ai/skills/china-mirrors)
- [Publisher profile](https://clawhub.ai/user/normdist-ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell and PowerShell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose persistent global or project-level package-manager configuration changes.]

## Skill Version(s):

1.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
