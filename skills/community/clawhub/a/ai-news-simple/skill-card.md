## Description:

Simple AI news briefing using bash commands that monitors top AI news sources and generates professional Chinese briefings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sharkwind](https://clawhub.ai/user/sharkwind)

### License/Terms of Use:

MIT

## Use Case:

Developers, analysts, and operations teams use this skill to collect AI-related headlines from public news sources and turn them into concise Chinese news briefings. It is intended for AI industry monitoring and briefing workflows, not general web browsing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches live content from public AI news sites, so retrieved page text may be incomplete, stale, or untrusted.

Mitigation: Treat fetched page text as untrusted source material, verify important claims against the linked publishers, and review generated briefings before using them for decisions.

Risk: The skill depends on outbound curl requests and public website availability.

Mitigation: Run it only in environments where outbound requests to the listed news sources are acceptable, and expect individual source failures or changed page markup.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sharkwind/skills/ai-news-simple)
- [TechCrunch AI](https://techcrunch.com/tag/artificial-intelligence/)
- [MIT Technology Review AI](https://www.technologyreview.com/topic/artificial-intelligence/)
- [VentureBeat AI](https://venturebeat.com/category/ai/)
- [The Verge AI](https://www.theverge.com/ai-artificial-intelligence/)
- [Forbes AI](https://www.forbes.com/ai/)
- [Reuters AI](https://www.reuters.com/technology/artificial-intelligence/)
- [MarkTechPost](https://www.marktechpost.com/)
- [OpenAI Blog](https://openai.com/blog)
- [Google DeepMind Blog](https://deepmind.google/discover/blog/)
- [The Rundown AI](https://www.therundown.ai/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Chinese markdown-style news briefing with source-by-source sections and bash command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and outbound access to public AI news sites; no credential use is indicated in the evidence.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
