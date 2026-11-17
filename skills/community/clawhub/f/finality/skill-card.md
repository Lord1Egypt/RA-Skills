## Description:

Finality is advertised as a blockchain finality analysis skill, but the reviewed artifact implements a local command-line data manager with status, add, list, search, remove, export, stats, and config commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents can use this skill to run simple local entry-management commands and inspect or export the stored records. Do not rely on it for blockchain finality analysis or protocol security decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact is advertised as blockchain finality analysis, but security evidence says it is not a real finality-analysis skill.

Mitigation: Treat it only as a local data-management utility unless a trusted reviewer confirms the intended blockchain-analysis behavior.

Risk: The artifact can persist, remove, and export local data.

Mitigation: Run it only in an isolated workspace with reviewed FINALITY_DIR settings and avoid storing sensitive information in its data files.

Risk: The config command is reported to have a command-injection flaw.

Mitigation: Do not pass untrusted input to config keys or values; review and patch the script before using that command in automation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ckchzh/skills/finality)
- [Publisher profile](https://clawhub.ai/user/ckchzh)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, files]

**Output Format:** [Markdown with inline bash code blocks and plain-text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command execution may create, modify, remove, or export local JSONL/config files under FINALITY_DIR or the current working directory.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
