## Description: <br>
AIScan v1.4.0 audits websites for AI-agent readiness, MCP discoverability, LLM access, framework signals, and fix-ready remediation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[asif2bd](https://clawhub.ai/user/asif2bd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, site owners, and agents use AIScan to audit public websites for AI-agent readiness, inspect crawler, MCP, LLM, framework, and discovery signals, and produce platform-aware remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Website URLs submitted for scanning are disclosed to the hosted aiscan.site service. <br>
Mitigation: Scan only public URLs or URLs the user is comfortable sending to aiscan.site; avoid confidential, internal, localhost, and staging URLs unless disclosure is intentional. <br>
Risk: AI-readiness fixes may alter public machine-readable files or discovery metadata. <br>
Mitigation: Review proposed robots.txt, llms.txt, sitemap, .well-known, OAuth, MCP, and agent-skill changes before an agent writes them to a site. <br>
Risk: Remediation guidance could claim unsupported API, MCP, OAuth, or agent-skill capabilities if applied without validation. <br>
Mitigation: Publish discovery files only for real capabilities and validate proposed changes against the site's actual platform and repository structure. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/asif2bd/skills/aiscan-ai-readiness-scanner) <br>
- [Live Scanner](https://aiscan.site) <br>
- [REST API Docs](https://aiscan.site/api/public/scan) <br>
- [MCP Endpoint](https://aiscan.site/api/mcp) <br>
- [Agent Skill JSON](https://aiscan.site/aiscan-skill.json) <br>
- [Changelog](https://aiscan.site/changelog) <br>
- [MissionDeck.ai Cloud](https://missiondeck.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or text reports with optional JSON API results, code snippets, shell commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include AIScan scores, grades, dimension summaries, failed or partial checks, remediation steps, and a re-scan plan.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata, SKILL.md frontmatter, CHANGELOG.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
