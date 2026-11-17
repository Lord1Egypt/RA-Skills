## Description:

AI News Briefing monitors ten public AI news sources, extracts AI-related content with OpenClaw browser-execution, and generates Chinese AI industry briefings with summarization support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sharkwind](https://clawhub.ai/user/sharkwind)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and analysts use this skill to generate time-filtered AI news briefings, monitor public AI industry updates, and summarize key developments from multiple public sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow browses ten public AI news sources and sends extracted public article text through the summarization/model workflow.

Mitigation: Use it only in environments where outbound browsing and model-based summarization of public article text are allowed.

Risk: Briefing quality depends on public website availability, source filtering, and model summarization accuracy.

Mitigation: Verify important claims against the linked source publications before making business or operational decisions.

Risk: The documented output is optimized for Chinese-language briefings.

Mitigation: Ask for a different output language when Chinese briefings are not desired.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sharkwind/skills/ai-news-briefing)
- [Publisher profile](https://clawhub.ai/user/sharkwind)
- [TechCrunch AI](https://techcrunch.com/tag/artificial-intelligence/)
- [MIT Technology Review AI](https://www.technologyreview.com/topic/artificial-intelligence/)
- [VentureBeat AI](https://venturebeat.com/category/ai/)
- [The Verge AI](https://www.theverge.com/ai-artificial-intelligence/)
- [Forbes AI](https://www.forbes.com/ai/)
- [Reuters AI](https://www.reuters.com/technology/artificial-intelligence/)
- [MarkTechPost](https://www.marktechpost.com/)
- [OpenAI Blog](https://openai.com/blog)
- [DeepMind Blog](https://deepmind.google/discover/blog/)
- [The Rundown AI](https://www.therundown.ai/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Chinese Markdown/text news briefing with shell-command workflow snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Browses public AI news sources, filters AI-related text, and summarizes findings into source-by-source briefing sections.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
