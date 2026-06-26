## Description: <br>
Fetches RSS feeds from 90 top Hacker News blogs, scores and filters articles with AI, and generates a Markdown daily digest with translated titles, categories, trend highlights, Mermaid charts, and a tag cloud. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[royxiao08](https://clawhub.ai/user/royxiao08) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and technical readers use this skill to collect recent articles from curated technical RSS feeds, rank them with an AI provider, and produce a daily digest in Chinese or English. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores a Gemini API key in a predictable plaintext local config file. <br>
Mitigation: Use a restricted or low-billing-limit key, avoid shared machines, and delete ~/.hn-daily-digest/config.json when the saved key is no longer needed. <br>
Risk: RSS article titles, descriptions, and URLs are sent to Gemini or a configured OpenAI-compatible provider for scoring and summarization. <br>
Mitigation: Run only with providers and endpoints you trust, and do not set OPENAI_API_BASE to an untrusted endpoint. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/royxiao08/ai-daily-digest) <br>
- [Hacker News Popularity Contest 2025](https://refactoringenglish.com/tools/hn-popularity/) <br>
- [Andrej Karpathy source note](https://x.com/karpathy) <br>
- [Google AI Studio API keys](https://aistudio.google.com/apikey) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report plus concise terminal status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a digest Markdown file containing article summaries, ranking rationale, category statistics, Mermaid charts, ASCII charts, and tag cloud output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
