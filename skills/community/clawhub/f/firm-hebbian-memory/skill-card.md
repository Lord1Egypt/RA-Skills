## Description: <br>
Système de mémoire adaptative hebbienne pour Claude.md qui transforme les logs de sessions en patterns pondérés afin de renforcer ou d'atrophier les règles de travail selon l'usage réel. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[romainsantoli-web](https://clawhub.ai/user/romainsantoli-web) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to connect Claude.md guidance with an adaptive memory workflow that harvests session logs, analyzes recurring patterns, and proposes Hebbian weight updates. It is intended for teams that want reviewable consolidation of recurring work patterns into agent instructions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can collect local session logs into persistent adaptive memory through an external MCP extension and optional cron job. <br>
Mitigation: Enable harvesting only after trusting the external MCP extension, choosing exact allowed log paths, and defining retention and deletion rules. <br>
Risk: Session logs may contain personal data or secrets, and regex-based stripping may miss some credentials such as connection URLs or environment variables in stack traces. <br>
Mitigation: Keep path whitelisting enabled, reject sessions with detected secrets, and add a dedicated secret scanner before use in sensitive environments. <br>
Risk: Adaptive weight updates could change agent memory or instructions based on accumulated logs. <br>
Mitigation: Keep weight updates in dry-run or review-only mode unless an authorized human explicitly approves the change. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/romainsantoli-web/firm-hebbian-memory) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell and JSON configuration blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Describes OpenClaw MCP tools, local hooks, cron automation, audit commands, and human review checkpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
