## Description:

Système de mémoire adaptative hebbienne pour Claude.md qui transforme les logs de sessions en patterns pondérés afin de renforcer ou d'atrophier les règles de travail selon l'usage réel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[romainsantoli-web](https://clawhub.ai/user/romainsantoli-web)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to design or operate an adaptive Claude.md memory workflow that ingests session logs, analyzes recurring work patterns, updates Hebbian weights, and keeps human review in the loop before durable rule changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can continuously ingest future agent session logs into persistent local memory.

Mitigation: Review the hook before enabling it, limit allowed session paths, keep ingestion manual or tightly scheduled, and document how to disable scheduled ingestion and remove stored local data.

Risk: Session logs may contain sensitive data that regex-based stripping or runtime checks do not fully catch.

Mitigation: Use stronger secret scanning for sensitive environments, review rejected-session alerts, and avoid ingesting logs from paths that may contain secrets or private credentials.

Risk: Automatically weighted memory patterns could introduce stale or misleading rules into future agent behavior.

Mitigation: Keep weight updates in dry-run mode by default, require human review for durable changes, and use drift checks and reversible Git commits for applied updates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/romainsantoli-web/skills/firm-hebbian-memory)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline code, shell command, and JSON configuration blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes tool names, default Hebbian parameters, audit checks, hook examples, and security guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
