## Description:

Deals Hunter finds recent shopping deals from SMZDM RSS, enriches selected items with Tavily price-history search, and produces Chinese Markdown recommendations with purchase links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunnyhot](https://clawhub.ai/user/sunnyhot)

### License/Terms of Use:

MIT-0

## Use Case:

External users and shopping-focused agents use this skill to compile scheduled Chinese deal digests with current prices, price-history context, and buy-or-wait guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send shopping reports to an external Discord destination.

Mitigation: Confirm the destination before execution and restrict posting permissions to the intended channel.

Risk: Generated purchase links may come from an HTTP feed and are not allowlisted.

Mitigation: Treat every purchase link as untrusted and verify the final domain and product details before buying.

Risk: The skill writes local deal history, price cache, and report files.

Mitigation: Run it in a least-privileged or sandboxed environment and review the configured file paths before scheduling.

Risk: The skill uses Tavily search APIs and requires a Tavily key.

Mitigation: Provide only the Tavily key intended for this workflow and monitor quota usage.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sunnyhot/skills/deals-hunter)
- [Publisher profile](https://clawhub.ai/user/sunnyhot)
- [SMZDM RSS feed](http://feed.smzdm.com)
- [SMZDM RSS endpoint](https://www.smzdm.com/rss)
- [Manmanbuy price search](https://cu.manmanbuy.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown deal reports with purchase links, price-history notes, and setup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language recommendations; may write local deal history, price cache, and report files during execution.]

## Skill Version(s):

6.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
