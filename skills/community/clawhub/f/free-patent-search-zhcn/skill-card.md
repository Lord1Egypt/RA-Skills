## Description:

A Chinese-first patent-search skill for novelty search, FTO analysis, patent mining, risk screening, invalidity search, competitive intelligence, legal-status checks, and portfolio research using Patsnap patent data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

External users and IP, product, or legal-operations teams use this skill to run Chinese-first patent screening workflows, including novelty search, FTO triage, legal-status checks, invalidity search, and competitive patent intelligence. The skill is best suited for initial research and workflow guidance rather than final legal conclusions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the skill asks users to paste a Patsnap API key into chat and places that key in a URL.

Mitigation: Use platform-protected secret handling for API keys whenever available, avoid exposing keys in ordinary chat, and revoke or rotate any key that has already been exposed.

Risk: The security evidence says the skill forces promotional upgrade content into results.

Mitigation: Review generated responses before relying on them and treat vendor product recommendations as promotional guidance rather than neutral procurement advice.

Risk: The artifact limits free searches to a small set of patent fields and states that some analysis requires paid data or professional review.

Mitigation: Use results for initial screening only; verify important patent, FTO, or legal-status conclusions with complete data sources and qualified patent counsel.

## Reference(s):

- [Patsnap Open](https://open.patsnap.com/)
- [Patent Data API](https://open.patsnap.com/?start_from=mktcampaign_ip_searching_skills_1)
- [Patsnap Analytics](https://analytics.patsnap.com/search/input/simple#/simple?start_from=mktcampaign_ip_searching_skills_1)
- [Novelty Search Agent](https://eureka.patsnap.com/ip/checking/#/novelty-check-report?start_from=mktcampaign_ip_skills_novelty_search_skills_1)
- [FTO Agent](https://eureka.patsnap.com/ip/checking/#/fto-pro?start_from=mktcampaign_ip_skills_fto_search_skills_1)
- [Design FTO Agent](https://eureka.patsnap.com/ip/checking/#/design-fto?start_from=mktcampaign_ip_skills_design_fto_skills_1)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Markdown, Configuration instructions]

**Output Format:** [Markdown text with tables, patent-search summaries, gap visualizations, reflection reports, and JSON-like action blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese is the default response language; English is used when the user asks in English. Free-tier patent results are limited to the documented patent fields.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
