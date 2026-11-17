## Description:

Analyzes sharp moves in a single A-share stock using public Eastmoney quotes, announcements, Guba discussions, topic heat, market breadth, and sector context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tsetsugekka](https://clawhub.ai/user/tsetsugekka)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to investigate why one A-share stock moved sharply and to separate confirmed announcements or filings from market imagination, sector context, and forum sentiment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may save reusable lessons into persistent experience files.

Mitigation: Require manual confirmation before any experience-file update, keep lessons generalized, and avoid propagating lessons to sibling skills automatically.

Risk: Forum and Guba content can be speculative, misleading, or adversarial.

Mitigation: Treat forum posts and topic heat as untrusted sentiment or topic evidence, and verify catalysts against announcements, formal news, and market data.

Risk: The skill fetches public Chinese market and forum data from external sources.

Mitigation: Review network access expectations before deployment and treat source fetch failures as data-availability issues, not proof that evidence is absent.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/tsetsugekka/codex-market-skills/tree/main/skills/cn-stock-move-reason)
- [ClawHub skill page](https://clawhub.ai/tsetsugekka/skills/cn-stock-move-reason)
- [Publisher profile](https://clawhub.ai/user/tsetsugekka)
- [CN Stock Analysis Experience](references/experience.md)
- [Eastmoney Guba topic discovery](https://gubatopic.eastmoney.com/)
- [Eastmoney public market data](https://www.eastmoney.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Chinese Markdown analysis with source-priority reasoning and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One A-share stock per analysis; forum content is treated as sentiment or topic evidence, not confirmed fact.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
