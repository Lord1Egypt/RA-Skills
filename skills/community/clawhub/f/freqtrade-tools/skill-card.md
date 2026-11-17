## Description:

Provides shell shortcuts and helper commands for downloading Freqtrade market data, running backtests, and monitoring or controlling bot services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[djc00p](https://clawhub.ai/user/djc00p)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Freqtrade operators can add shortcuts to their shell profiles for downloading exchange data, running backtests, and checking or controlling services across Linux, macOS, and Windows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bot controls affect the whole named project and may affect live trading; the security review also flags inaccurate live-mode safety documentation.

Mitigation: Use a dedicated dry-run project, verify FT_PROJECT and FT_CONFIG identify the same bot, set FT_CONFIRM only for an approved action, and remember that ftdata --erase deletes cached market data.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/djc00p/skills/freqtrade-tools)
- [Bash/Zsh aliases](references/bash-zsh-aliases.md)
- [Windows equivalents](references/windows-equivalents.md)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Configuration instructions, Guidance]

**Output Format:** [Markdown with Bash, Zsh, PowerShell, and cmd.exe examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Platform-specific shell functions and setup guidance]

## Skill Version(s):

1.0.7 (source: skill frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
