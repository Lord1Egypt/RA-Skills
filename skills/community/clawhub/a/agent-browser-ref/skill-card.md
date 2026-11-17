## Description:

Headless browser automation CLI guidance for AI agents using accessibility tree snapshots and ref-based element selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agent operators use this skill to automate browser workflows with agent-browser, including navigation, element interaction, data extraction, screenshots, PDFs, network control, and isolated browser sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved browser state can expose cookies, localStorage, and website login sessions.

Mitigation: Keep saved state outside projects, restrict file permissions, avoid committing or sharing it, delete it when no longer needed, and use separate low-privilege sessions for sensitive sites.

Risk: The skill relies on a global agent-browser installation that may be unpinned or sourced from an untrusted package origin.

Mitigation: Install only from a trusted package source, pin or review the package version before deployment, and re-review updates before use in sensitive workflows.

Risk: Browser automation can perform actions in authenticated web sessions and may affect real accounts or data.

Mitigation: Use isolated sessions with least-privilege test accounts where possible and review planned commands before executing workflows on sensitive sites.

## Reference(s):

- [Agent Browser skill reference](references/SKILL.md)
- [agent-browser CLI homepage](https://github.com/vercel-labs/agent-browser)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes command examples for browser navigation, ref-based interactions, state persistence, screenshots, PDFs, network controls, cookies, storage, tabs, and frames.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
