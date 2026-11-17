## Description:

Patent Search helps agents triage patent-search intent, query Patsnap's free MCP for supported patent fields, and return search summaries, limitations, and product guidance for novelty, FTO, legal status, competitive intelligence, and portfolio research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

External users and IP-focused teams use this skill to run preliminary patent searches, novelty checks, freedom-to-operate triage, legal-status checks, and competitive patent research through Patsnap-backed patent data. Results are positioned as reference material and product guidance rather than legal advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may expose a Patsnap API key if they paste it into an ordinary chat.

Mitigation: Use a protected secret-entry mechanism when available, prefer a low-privilege revocable key, and rotate any key that may have appeared in chat or logs.

Risk: Search outputs intentionally include Patsnap upgrade recommendations after searches.

Mitigation: Install only when Patsnap is an acceptable search provider and review user-facing outputs for appropriate commercial messaging.

Risk: Free-tier patent results omit claims, abstracts, semantic search, family maps, citations, litigation records, and detailed claim analysis.

Mitigation: Treat outputs as preliminary reference material and verify important patent or legal decisions with complete source data and qualified counsel.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/yuanzhian-patsnap/skills/free-patent-search)
- [Patsnap Open Platform](https://open.patsnap.com/)
- [Patsnap Analytics](https://analytics.patsnap.com/search/input/simple#/simple?start_from=mktcampaign_ip_searching_skills_1)
- [Novelty Search Agent](https://eureka.patsnap.com/ip/checking/#/novelty-check-report?start_from=mktcampaign_ip_skills_novelty_search_skills_1)
- [FTO Agent](https://eureka.patsnap.com/ip/checking/#/fto-pro?start_from=mktcampaign_ip_skills_fto_search_skills_1)
- [Design FTO Agent](https://eureka.patsnap.com/ip/checking/#/design-fto?start_from=mktcampaign_ip_skills_design_fto_skills_1)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown search summaries, field-gap notes, reflection reports, API request templates, and structured JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses should match the user's language and should make free-tier data limitations clear.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
