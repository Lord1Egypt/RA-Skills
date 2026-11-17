## Description:

Crawl and validate A-share information sources with browser-first and fallback fetch workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[afengzi](https://clawhub.ai/user/afengzi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and market-research agents use this skill to collect public A-share market information, classify site access quality, and normalize facts, sentiment, and unverified clues into summary-ready records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Providing logged-in browser access, cookies, or profile access for restricted sites can expose account context beyond normal public crawling.

Mitigation: Use stronger access only when the task explicitly requires it, prefer public entrypoints and approved fallback sources, and mark restricted sites as missing instead of implying full coverage.

Risk: Community-source content from sites such as Xueqiu or Jiuyangongshe can be mistaken for confirmed market facts.

Mitigation: Treat community items as sentiment or clues, assign lower source tiers and opinion-risk labels, and move unconfirmed claims to market-sentiment or pending-verification sections.

Risk: Anti-bot pages, login walls, shell pages, or PDF viewer output can be misread as usable extracted content.

Mitigation: Classify each probe as usable, partial, shell-only, or blocked; use body-coverage fields; keep PDF-only disclosure results at metadata level unless readable text is actually recovered.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/afengzi/skills/a-share-site-crawl)
- [Entrypoints](references/entrypoints.md)
- [Fields](references/fields.md)
- [Risks](references/risks.md)
- [Site Notes](references/sites.md)
- [Five-Site Workflow](references/workflow.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Chinese Markdown summaries and JSON-like normalized records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Separates confirmed facts, market sentiment, unverified clues, missing sites, and source-tier notes; does not provide buy or sell recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
