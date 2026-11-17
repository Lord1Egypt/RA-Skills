## Description:

Intelligent search for agents. Multi-source retrieval across web, scholar, Tavily, and Perplexity Sonar models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bowen-dotcom](https://clawhub.ai/user/bowen-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run web, scholar, Tavily, and Perplexity Sonar searches through AIsa APIs and return structured results, citation-rich answers, or research reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries, prompts, and supplied URLs are sent to AIsa-backed APIs using AISA_API_KEY.

Mitigation: Avoid submitting secrets, private documents, internal-only URLs, or proprietary research topics unless external processing is approved.

Risk: Generated search answers and research reports may include incomplete, stale, or misleading information.

Mitigation: Review cited sources and scan outputs before relying on results for decisions or downstream skill changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bowen-dotcom/skills/aisa-search-skill)
- [OpenClaw](https://openclaw.ai)
- [AIsa Documentation](https://docs.aisa.one)
- [AIsa API Reference](https://docs.aisa.one/reference/)
- [Perplexity Sonar API](https://docs.aisa.one/reference/post_perplexity-sonar)
- [Perplexity Sonar Pro API](https://docs.aisa.one/reference/post_perplexity-sonar-pro)
- [Perplexity Sonar Reasoning Pro API](https://docs.aisa.one/reference/post_perplexity-sonar-reasoning-pro)
- [Perplexity Sonar Deep Research API](https://docs.aisa.one/reference/post_perplexity-sonar-deep-research)
- [AIsa Verity](https://github.com/AIsa-team/verity)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY and sends user-directed queries, prompts, and supplied URLs to AIsa-backed APIs.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
