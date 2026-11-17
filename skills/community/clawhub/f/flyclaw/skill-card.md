## Description:

Multi-source flight aggregation for flight status, prices, schedules, route search, round-trip search, cabin selection, and nonstop filtering without requiring a login or API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai4mse](https://clawhub.ai/user/ai4mse)

### License/Terms of Use:

Apache-2.0

## Use Case:

External users and developers use this skill to query flight numbers or search routes across multiple flight data sources, including prices, schedules, live status, round trips, cabin class, and stop filters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Travel searches contact third-party flight services and may expose query details outside the user's environment.

Mitigation: Review the enabled data sources before installation and disable providers that do not match the user's travel-query privacy requirements.

Risk: The default Fliggy source can persist a device ID and send host metadata externally.

Mitigation: Disable `fliggy_mcp` or use the skill only after the publisher documents and minimizes that data flow.

Risk: Airport data updates can fetch content from user-supplied URLs.

Mitigation: Run `update-airports` only with trusted URLs and review downloaded data before relying on it.

## Reference(s):

- [FlyClaw ClawHub listing](https://clawhub.ai/ai4mse/skills/flyclaw)
- [README_EN.md](README_EN.md)
- [SKILL_EN.md](SKILL_EN.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration]

**Output Format:** [JSON on stdout by default, optional human-readable table output, with errors and logs on stderr]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Flight search records may include prices, currency, flight numbers, route segments, layover details, schedules, status, aircraft details, and source labels.]

## Skill Version(s):

0.4.4 (source: frontmatter and pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
