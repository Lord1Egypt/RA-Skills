## Description: <br>
Agent-first AEO operating platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arberx](https://clawhub.ai/user/arberx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and AEO analysts use this skill to measure brand mentions and domain citations across AI answer engines, diagnose visibility and indexing gaps, and operate Canonry CLI workflows for content, analytics, server traffic, Google Business Profile, and WordPress integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Canonry can connect to sensitive business systems, including analytics, logs, CMS, Google Business Profile, and local credential files. <br>
Mitigation: Use read-only or least-privilege accounts where possible, secure ~/.canonry/config.yaml, pass explicit account IDs, and review connected services before enabling automation. <br>
Risk: Some workflows can perform destructive or production-affecting actions, including project deletion, backfills, account switching, and WordPress changes. <br>
Mitigation: Use dry-run or preview commands when available, work in staging for WordPress, and require explicit approval before touching live systems. <br>
Risk: Agent, webhook, schedule, and API-key features may expose a write-capable automation surface. <br>
Mitigation: Prefer read-only agent scope and read-only API keys for analysis, review schedules and webhooks before enabling them, and grant write scopes only for approved operations. <br>
Risk: Incorrect interpretation of mention, citation, or probe data can produce misleading AEO recommendations. <br>
Mitigation: Treat mention and citation as independent signals, keep probe runs out of production metrics, and avoid fabricating or coercing missing measurements. <br>


## Reference(s): <br>
- [Canonry CLI Reference](references/canonry-cli.md) <br>
- [AEO Analysis](references/aeo-analysis.md) <br>
- [Indexing Workflows](references/indexing.md) <br>
- [WordPress Integration](references/wordpress-integration.md) <br>
- [Server-side Traffic](references/server-side-traffic.md) <br>
- [Google Business Profile Integration](references/google-business-profile.md) <br>
- [Canonry website](https://canonry.ai) <br>
- [AINYC organization](https://ainyc.ai) <br>
- [AINYC Canonry repository](https://github.com/AINYC/canonry) <br>
- [AINYC AEO Methodology](https://ainyc.ai/aeo-methodology) <br>
- [ClawHub skill page](https://clawhub.ai/arberx/skills/canonry) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON or configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include CLI commands, report interpretation, configuration snippets, and risk-aware operating guidance.] <br>

## Skill Version(s): <br>
4.97.0+007bc7e (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
