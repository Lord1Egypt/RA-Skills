## Description: <br>
Crawl and validate A-share information sources from five named sites with browser-first and fallback fetch workflows that handle access limits and normalize market-news outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[afengzi](https://clawhub.ai/user/afengzi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and market-data workflow operators use this skill to check crawlability, choose browser or fetch collection modes, and produce summary-ready A-share records from public sources while separating confirmed facts, sentiment, and unverified clues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Logged-in browser or cookie-based access can expose sensitive session material. <br>
Mitigation: Prefer anonymous or public access first, avoid raw cookies and main browser profiles, and use authenticated access only when explicitly needed. <br>
Risk: Anti-bot pages, login walls, disclaimers, or shell-only pages may be mistaken for usable market content. <br>
Mitigation: Classify these results as restricted or not usable, switch to verified entrypoints or browser checks, and disclose missing access instead of implying coverage. <br>
Risk: Community discussion from Xueqiu or Jiuyangongshe can be presented as confirmed fact. <br>
Mitigation: Keep community-only claims in sentiment or unverified-clue sections unless independently confirmed by official disclosures or reliable public reporting. <br>
Risk: Recurring summaries can hide failed priority sites and create overconfident coverage. <br>
Mitigation: Include missing-site reporting, note fallback sources, and keep crawl scope and retention limits explicit for recurring jobs. <br>
Risk: A-share summaries may drift into investment advice. <br>
Mitigation: Do not output buy or sell recommendations; structure outputs around facts, sentiment, source tiers, and verification status. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/afengzi/a-share-site-crawl) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Site notes](artifact/references/sites.md) <br>
- [Five-site workflow](artifact/references/workflow.md) <br>
- [Entrypoints](artifact/references/entrypoints.md) <br>
- [Normalized fields](artifact/references/fields.md) <br>
- [Risks](artifact/references/risks.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration, text] <br>
**Output Format:** [Markdown guidance with crawlability verdicts, normalized record schemas, source-tier notes, and Chinese market-summary sections when used for formal rounds.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Formal round outputs separate confirmed facts, market sentiment, unverified clues, missing sites, and source-tier explanations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
