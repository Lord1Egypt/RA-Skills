## Description:

Find cheapest flights and create interactive flight route maps with real-time flight search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rudy2steiner](https://clawhub.ai/user/rudy2steiner)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use Flightmapify to generate interactive HTML flight maps for origin, destination, and travel-date queries, including route visualization and flight-search links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill starts local HTTP services and manages ports while generating the flight-map experience.

Mitigation: Run it in a constrained workspace, choose ports that are not used by important services, and avoid exposing sensitive workspace files while the local server is active.

Risk: The artifact includes process-management behavior that can terminate a process on a selected port.

Mitigation: Review the process-handling code before installation and prefer a version that removes automatic kill -9 behavior.

Risk: Flight search subprocesses may receive environment variables containing FlyAI credentials.

Mitigation: Pass only the required FlyAI credential to subprocesses and avoid running the skill with elevated privileges.

Risk: The skill depends on external FlyAI tooling and map services for live search and visualization.

Mitigation: Pin and review external dependencies, use a personal FlyAI API key where appropriate, and expect rate limits or service availability issues.

## Reference(s):

- [Flightmapify ClawHub page](https://clawhub.ai/rudy2steiner/skills/flightmapify)
- [rudy2steiner ClawHub publisher profile](https://clawhub.ai/user/rudy2steiner)
- [FlyAI API key console](https://flyai.open.fliggy.com/console)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration, Guidance]

**Output Format:** [HTML files and terminal text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a local interactive flight-map HTML file and localhost access URL; flight search may use FlyAI and Amap credentials from environment variables.]

## Skill Version(s):

1.4.6 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
