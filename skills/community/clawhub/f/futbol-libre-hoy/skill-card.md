## Description:

List today's football fixtures and live scores using the futbol-libre-hoy CLI/package.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nazzal5448](https://clawhub.ai/user/nazzal5448)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to fetch today's football fixtures, live scores, date-specific match lists, and match URLs for deeper review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to run unpinned third-party npm or Python packages.

Mitigation: Use pinned, reviewed package versions with hashes or a locked dependency workflow before running the commands.

Risk: The package runs with the user's normal local permissions.

Mitigation: Run it only in an environment without sensitive files or credentials until package provenance is verified.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nazzal5448/skills/futbol-libre-hoy)
- [Futbol Libre Hoy homepage](https://verfutbollibre.net)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and match URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live-score results, date-specific fixtures, JSON command usage, and links to match detail pages.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
