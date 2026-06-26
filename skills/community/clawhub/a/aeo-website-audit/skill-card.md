## Description: <br>
Run a live 100-point AEO (Answer Engine Optimization) audit on any website, scoring schema markup, meta signals, content structure, technical setup, and AI visibility with grades, component breakdowns, and prioritized recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[piiiico](https://clawhub.ai/user/piiiico) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, marketers, SEO consultants, and website owners use this skill to audit public websites for answer-engine visibility and receive scored component breakdowns with prioritized fixes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-provided URLs to a disclosed external audit service. <br>
Mitigation: Use it for public website audits and avoid private staging sites, internal hostnames, or sensitive URLs unless sharing them with the hosted audit provider is acceptable. <br>
Risk: Audit calls depend on an external service with documented rate limits and timeouts. <br>
Mitigation: Handle failed or delayed requests gracefully and avoid high-volume repeated calls beyond the published limit. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/piiiico/aeo-website-audit) <br>
- [Publisher profile](https://clawhub.ai/user/piiiico) <br>
- [Synlig Digital homepage](https://synligdigital.no) <br>
- [AEO audit REST endpoint](https://aeo-mcp-server.amdal-dev.workers.dev/audit?url={URL}) <br>
- [AEO audit MCP endpoint](https://aeo-mcp-server.amdal-dev.workers.dev/mcp) <br>
- [A2A agent card endpoint](https://aeo-mcp-server.amdal-dev.workers.dev/.well-known/agent-card.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and structured audit results from JSON API responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a public website URL; calls an external hosted audit service with no credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
