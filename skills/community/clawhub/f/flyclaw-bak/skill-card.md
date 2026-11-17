## Description:

Flyclaw Bak helps agents query and aggregate flight status, schedules, prices, routes, cabin options, nonstop filters, and real-time position data from multiple public flight sources without requiring a user account or API key for core use.

This skill is for research and development only.

## Publisher:

[qizha](https://clawhub.ai/user/qizha)

### License/Terms of Use:

Apache-2.0

## Use Case:

External users and developers use this skill to ask an agent for flight-number lookups, route searches, city-to-city flight options, round trips, cabin filters, direct or connecting flights, and price comparisons. The skill is most appropriate for exploratory travel search where public-provider availability and price variance are acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Normal searches contact external flight providers, which may expose travel-query details or be unsuitable for agents running on sensitive internal networks.

Mitigation: Review before installing in privacy-sensitive environments and restrict execution to contexts where outbound public flight-provider requests are acceptable.

Risk: The airport-cache update feature can retrieve remote cache data.

Mitigation: Use the cache update path only with trusted HTTPS URLs and review updated cache files before relying on them.

Risk: The artifact includes an embedded Fliggy key described by the security evidence as a shared public client credential.

Mitigation: Treat the value as non-secret shared client material, do not reuse it as a private credential, and rotate or replace it if deploying in a managed environment.

Risk: Optional SerpAPI, MCP, or browser-related modes add extra dependency and network paths beyond the core zero-key workflow.

Mitigation: Keep optional modes disabled unless their dependencies, credentials, and outbound network behavior have been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qizha/skills/flyclaw-bak)
- [ClawHub publisher profile](https://clawhub.ai/user/qizha)
- [Skill documentation](artifact/SKILL_EN.md)
- [README](artifact/README_EN.md)
- [FlightRadar24 API endpoint](https://api.flightradar24.com/common/v1)
- [Airplanes.live API endpoint](https://api.airplanes.live/v2)
- [ADSB.lol API endpoint](https://api.adsb.lol/v2)
- [Skiplagged MCP endpoint](https://mcp.skiplagged.com/mcp)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Text, Configuration guidance]

**Output Format:** [Markdown guidance with shell commands; CLI results are JSON by default or a human-readable table when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prices default to CNY with optional USD conversion; stderr is used for errors and logs so JSON stdout remains parseable.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter and pyproject.toml report source version 0.4.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
