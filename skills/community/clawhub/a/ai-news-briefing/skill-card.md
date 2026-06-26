## Description: <br>
AI News Briefing monitors public AI news sources, extracts AI-related items, and helps an agent generate Chinese briefing summaries with source attribution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sharkwind](https://clawhub.ai/user/Sharkwind) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, developers, and AI-industry analysts use this skill to check recent AI news and produce structured Chinese briefings from public news sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill visits listed public news sites and may send extracted snippets through configured summarization or model tools. <br>
Mitigation: Review or limit the source list and run the skill only where those network and data-handling controls are acceptable. <br>
Risk: Briefings can reflect incomplete, stale, or unavailable source pages. <br>
Mitigation: Review generated summaries and source attribution before relying on them for decisions. <br>


## Reference(s): <br>
- [AI News Briefing on ClawHub](https://clawhub.ai/Sharkwind/ai-news-briefing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-style Chinese news briefing text with source-by-source summaries and attribution.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public web pages and configured summarization/model tools; source access may fail or change.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata; package.json reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
