## Description: <br>
AI News Simple generates Chinese AI news briefings by fetching and filtering public AI news sources with bash and curl. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sharkwind](https://clawhub.ai/user/Sharkwind) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to generate AI industry news briefings, monitor AI news sources, and summarize recent AI-related developments in Chinese. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts public news websites while generating briefings. <br>
Mitigation: Review outbound network policy before use in corporate or privacy-sensitive environments. <br>
Risk: Fetched webpage content is untrusted and may contain incomplete, stale, or misleading material. <br>
Mitigation: Treat fetched content as source material for review and verify important claims against authoritative sources before acting on them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Sharkwind/ai-news-simple) <br>
- [Publisher Profile](https://clawhub.ai/user/Sharkwind) <br>
- [TechCrunch AI](https://techcrunch.com/tag/artificial-intelligence/) <br>
- [MIT Technology Review AI](https://www.technologyreview.com/topic/artificial-intelligence/) <br>
- [VentureBeat AI](https://venturebeat.com/category/ai/) <br>
- [Reuters Artificial Intelligence](https://www.reuters.com/technology/artificial-intelligence/) <br>
- [OpenAI Blog](https://openai.com/blog) <br>
- [Google DeepMind Blog](https://deepmind.google/discover/blog/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown-style Chinese briefing with bash command output and source attribution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses curl to fetch public webpages; no credential inputs were detected.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
