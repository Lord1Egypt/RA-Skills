## Description:

Dual-value learning system that selects books, extracts reusable mental models, writes persistent Markdown knowledge entries, and returns F.A.C.E.T. analysis for user learning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kedoupi](https://clawhub.ai/user/kedoupi)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and teams use this skill to turn selected books into reusable mental models, maintain a local decision-framework library, and produce personalized learning briefings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads USER.md and HEARTBEAT-reading.md, which may contain private work, company, client, or project details.

Mitigation: Review those files before use and prefer local-only runs when they contain sensitive context.

Risk: Generated mental-model entries are persisted for future agent use and may influence later answers.

Mitigation: Review generated knowledge entries before auto-loading them into future sessions and treat them as untrusted reference material until approved.

Risk: Optional Feishu or Notion sync can send personalized analysis to external services.

Mitigation: Keep tokens in environment variables, approve external sync per run, and disable sync unless the destination is intended.

## Reference(s):

- [Cognitive Forge ClawHub page](https://clawhub.ai/kedoupi/skills/cognitive-forge)
- [Book Selection Logic](references/book-selection.md)
- [Knowledge Classification Guide](references/knowledge-classification.md)
- [Example Output Format](references/example-output.md)
- [book-scout dependency](https://clawhub.ai/kedoupi/book-scout)
- [mental-model-forge dependency](https://clawhub.ai/kedoupi/mental-model-forge)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance]

**Output Format:** [Markdown briefings plus Markdown and JSON knowledge-base files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports full, brief, status, review, and depth-mode outputs; optional Feishu or Notion sync when credentials are provided.]

## Skill Version(s):

1.0.4 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
