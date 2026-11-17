## Description:

Review daily AI advancements and domestic banking fintech progress from tier-1 curated sources with full text inspection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lube845](https://clawhub.ai/user/lube845)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to generate a daily AI and fintech brief from curated AI, banking, and domestic financial technology sources. The skill retrieves or reuses recent article data, summarizes concrete technical and business details, and saves a Markdown report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The crawler can follow untrusted links from source pages and bring fetched article content into the agent and local storage.

Mitigation: Review before installing, block outbound requests to private or internal services, or harden crawling with strict HTTPS host allowlists and redirect validation.

Risk: Fetched article text, raw JSON, and cached reports may contain untrusted or misleading content.

Mitigation: Treat fetched content and cached reports as untrusted inputs and review generated briefs before relying on or redistributing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lube845/skills/daily-fintech-brief)
- [The Batch RSS](https://www.deeplearning.ai/the-batch/rss/)
- [Ben's Bites RSS](https://www.bensbites.co/rss)
- [Banking Dive RSS](https://www.bankingdive.com/feeds/news/)
- [China Financial Computer technology news](https://www.fcc.com.cn/art/kjzx/)
- [China Electronic Banking digital banking](https://www.cebnet.com.cn/szyh/)
- [China Electronic Banking financial AI](https://www.cebnet.com.cn/financialai/)
- [MPayPass](https://www.mpaypass.com.cn/)
- [MPayPass fintech column](https://www.mpaypass.com.cn/authordefault.asp?id=80115)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files]

**Output Format:** [Markdown daily brief with supporting JSON article payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Raw article JSON is cached for 7 days; generated Markdown reports are retained under the skill workspace.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
