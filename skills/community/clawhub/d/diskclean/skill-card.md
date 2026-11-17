## Description:

AI-assisted disk space scanner and cleaner that finds reclaimable space from local development artifacts, caches, downloads, Docker, Xcode, logs, and related files, then helps preview and clean approved items.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xj7r](https://clawhub.ai/user/0xj7r)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use diskclean to scan macOS or Linux home directories for reclaimable local development artifacts and present cleanup recommendations before running approved cleanup commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confirmed cleanup can delete more than a user expects because cleanup guardrails are weaker than advertised.

Mitigation: Review every dry-run item carefully before confirmation, confirm paths are under the user's home directory and clearly understood, and avoid confirmed cleanup until path validation and age checks are fixed.

Risk: Safe-tier labels may overstate safety for logs or aged cache paths.

Mitigation: Treat safe-tier output as a review queue rather than automatic approval, and manually limit deletion to clearly regenerable artifacts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/0xj7r/skills/diskclean)
- [Publisher profile](https://clawhub.ai/user/0xj7r)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with shell commands and JSON scan or report output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3; intended for macOS and Linux; cleanup should be preceded by dry-run review.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
