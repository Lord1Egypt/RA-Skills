## Description:

Use when a user asks an agent to do web research, source discovery, citation-backed reporting, page extraction, crawling, or browser-rendered research using the BuiltByEcho Research npm package.

This skill is ready for commercial/non-commercial use.

## Publisher:

[builtbyecho](https://clawhub.ai/user/builtbyecho)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run local-first web research workflows, discover and extract sources, render JavaScript-heavy pages, crawl sites, and produce citation-backed reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to run npm-based research tooling with network and browser access.

Mitigation: Prefer pinning @builtbyecho/research to the reviewed version and run it with limited filesystem and environment access.

Risk: The skill includes a durable upload workflow for reports or trace bundles.

Mitigation: Require explicit review and redaction before uploading research artifacts to Vaultline or any external storage.

Risk: Research output may contain incorrect or misleading citations or source summaries.

Mitigation: Review generated reports and verify citations before using the output for high-stakes decisions.

## Reference(s):

- [BuiltByEcho Research homepage](https://github.com/BuiltByEcho/research)
- [ClawHub skill page](https://clawhub.ai/builtbyecho/skills/builtbyecho-research)
- [BuiltByEcho publisher profile](https://clawhub.ai/user/builtbyecho)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include traceable research reports, extracted fields, crawl output, and source citations.]

## Skill Version(s):

0.5.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
