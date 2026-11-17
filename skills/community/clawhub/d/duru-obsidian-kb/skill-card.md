## Description:

Build and maintain a personal Obsidian-based knowledge base from articles, papers, repositories, datasets, spreadsheets, and local files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durugy](https://clawhub.ai/user/durugy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and knowledge workers use this skill to collect source material into a local markdown knowledge base, compile Obsidian-friendly wiki pages, search or ask questions over the KB, generate markdown outputs, and run health checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary flags unsafe review-worthy behavior around command execution from configuration.

Mitigation: Review configuration and .env values before use, run only trusted local scripts, and execute the skill in a dedicated workspace.

Risk: The security summary flags broad network fetching and repository ingestion.

Mitigation: Avoid attacker-supplied URLs or repositories and prefer trusted sources until URL validation and size limits are fixed.

Risk: The security summary flags file writes outside intended paths and risky file-back targets.

Mitigation: Use a dedicated KB directory and review output paths and target concepts before enabling file-back behavior.

## Reference(s):

- [Duru Obsidian KB on ClawHub](https://clawhub.ai/durugy/skills/duru-obsidian-kb)
- [Layout Reference](references/layout.md)
- [Phase Plan](references/phase-plan.md)
- [Daily Ops](references/daily-ops.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown files, JSON manifests, shell command guidance, and local knowledge-base artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces deterministic local files under a selected knowledge-base root when scripts are run.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
