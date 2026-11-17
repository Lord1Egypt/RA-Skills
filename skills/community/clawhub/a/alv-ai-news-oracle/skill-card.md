## Description:

Fetches real-time AI news briefings from Hacker News, TechCrunch, and The Verge using SkillBoss API Hub search and chat capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvisdunlop](https://clawhub.ai/user/alvisdunlop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to fetch current AI news briefings and source-linked summaries through SkillBoss API Hub.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends news-search and summarization requests to a third-party API service.

Mitigation: Confirm the SkillBoss API service is trusted before installation and review what data the agent sends through the API.

Risk: The skill requires a SkillBoss API key for authentication.

Mitigation: Use a scoped API key, store it as SKILLBOSS_API_KEY, and avoid embedding credentials in prompts, code, or shared logs.

Risk: Installing from a moving repository branch can change behavior after review.

Mitigation: Prefer a reviewed commit or release when installing the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alvisdunlop/skills/alv-ai-news-oracle)
- [SkillBoss API Hub pilot endpoint](https://api.heybossai.com/v1/pilot)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Structured JSON briefing with concise bullet-point text and source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and calls the SkillBoss API Hub.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
