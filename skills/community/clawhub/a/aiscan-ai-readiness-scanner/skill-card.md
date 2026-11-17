## Description:

AIScan v3.1 audits websites for AI-agent readiness through its stable REST API, MCP server, CLI/CI tooling, evidence-backed scoring, and fix-ready remediation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asif2bd](https://clawhub.ai/user/asif2bd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site owners, and agent operators use AIScan to audit whether public websites are ready for AI agents, LLM crawlers, MCP-aware tools, and answer engines. The skill helps agents call AIScan surfaces, interpret scores and failing checks, produce reports, and apply user-approved remediation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Website URLs and scan requests are sent to AIScan as a third-party hosted scanner.

Mitigation: Use the skill only for sites the user is authorized to scan, and avoid private or staging URLs unless the user confirms scanning is allowed.

Risk: The documented curl-to-node CLI fallback can run mutable remote code.

Mitigation: Prefer the REST API or MCP tools; if CLI use is needed, pin a CLI version and avoid the curl-to-node fallback.

Risk: AIScan remediation can lead agents to edit user repositories based on remote fix guidance.

Mitigation: Review every proposed change, apply only the smallest user-approved fixes, and re-scan once to confirm the result.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/asif2bd/skills/aiscan-ai-readiness-scanner)
- [Live Scanner](https://aiscan.site)
- [Developer and REST API Docs](https://aiscan.site/developers)
- [OpenAPI 3.1](https://aiscan.site/openapi.json)
- [API Catalog](https://aiscan.site/.well-known/api-catalog)
- [MCP Endpoint](https://aiscan.site/api/mcp)
- [Agent Skill JSON](https://aiscan.site/aiscan-skill.json)
- [Changelog](https://aiscan.site/changelog)
- [MissionDeck.ai Cloud](https://missiondeck.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or text with JSON scan results, shell commands, and code or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [REST API and MCP calls return scores, grades, checks, platform evidence, and remediation; reports may be generated as Markdown.]

## Skill Version(s):

2.0.0 (source: release metadata, SKILL.md frontmatter, CHANGELOG released 2026-08-25)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
