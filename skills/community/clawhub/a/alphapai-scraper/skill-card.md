## Description:

Logs in to AlphaPai to scrape recent market comments, archive raw and structured records, build local search indexes, query historical comments, generate mobile-friendly summaries, and optionally send summaries to Feishu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawdbotrr](https://clawhub.ai/user/clawdbotrr)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect recent AlphaPai comments, store them locally, query the indexed archive by topic and time window, and produce concise Chinese summaries for market research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires AlphaPai credentials, tokens, cookies, or saved browser sessions, and the supplied security evidence warns that these authenticated session files need tight local protection.

Mitigation: Use a scoped AlphaPai token or dedicated browser profile, keep credential and session files out of published packages, restrict local file permissions, and delete saved session artifacts when no longer needed.

Risk: The security guidance flags broad browser-session access and Chrome-profile fallback as review concerns.

Mitigation: Prefer storage state, token, or cookies for a dedicated AlphaPai session, and disable Chrome-profile fallback unless the operator has reviewed and accepted that access.

Risk: The security guidance calls out ignore_https_errors behavior before authenticated login.

Mitigation: Remove or disable ignore_https_errors before entering credentials or using authenticated sessions.

Risk: Optional Feishu webhook delivery can send generated summaries outside the local machine.

Mitigation: Leave Feishu disabled unless the exact webhook endpoint is trusted and intended for the scraped or summarized content.

Risk: Artifact documentation notes that hybrid retrieval lacks stronger reranking and negation filtering, so query summaries may include irrelevant or misleading matches.

Mitigation: Review source snippets and treat generated summaries as aids for research triage rather than final market conclusions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clawdbotrr/skills/alphapai-scraper)
- [AlphaPai web application](https://alphapai-web.rabyte.cn)
- [AlphaPai comments page](https://alphapai-web.rabyte.cn/reading/home/comment)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, code, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries, raw text or Markdown captures, structured JSON records, SQLite and vector indexes, runtime metadata, configuration guidance, and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are written locally under the configured AlphaPai data directory; Feishu delivery is optional and disabled unless a trusted webhook is configured.]

## Skill Version(s):

0.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
