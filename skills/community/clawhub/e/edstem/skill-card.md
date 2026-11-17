## Description:

Fetch, sync, and organize EdStem discussion threads for any course or institution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[axel5o5](https://clawhub.ai/user/axel5o5)

### License/Terms of Use:

MIT

## Use Case:

External users, educators, course staff, and developers use this skill to fetch, archive, review, and analyze EdStem course discussion threads across institutions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill ships and documents hardcoded EdStem bearer tokens for private course data.

Mitigation: Treat any included token as exposed, revoke it, and replace hardcoded tokens with a secure runtime secret before use.

Risk: Exported EdStem discussions may contain student or staff content that should not be shared broadly.

Mitigation: Confirm authorization to export course discussions, store generated files in an appropriate private location, and review LLM or cron workflows for disclosure risk.

Risk: The security verdict requires review before installation.

Mitigation: Review and scan the skill before deployment, and do not install it as-is in shared or published environments.

## Reference(s):

- [EdStem Skill on ClawHub](https://clawhub.ai/axel5o5/skills/edstem)
- [EdStem API endpoint](https://us.edstem.org/api)
- [README](artifact/README.md)
- [Changelog](artifact/CHANGELOG.md)
- [Migration notes](artifact/MIGRATION_NOTES.md)

## Skill Output:

**Output Type(s):** [markdown, JSON, text, shell commands, configuration guidance]

**Output Format:** [Markdown thread files, JSON thread metadata, terminal status text, and usage commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a user-selected output directory and writes EdStem thread exports for the requested course.]

## Skill Version(s):

1.1.0 (source: server release metadata, README, CHANGELOG, PUBLISHING.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
