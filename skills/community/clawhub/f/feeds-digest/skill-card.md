## Description: <br>
Aggregates RSS and Atom updates from YouTube, Microsoft blogs, GitHub releases, and generic feeds, then filters them by date and topic with optional LLM summarization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jcbuer](https://clawhub.ai/user/jcbuer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical teams use this skill to collect product, release, and community updates into a filtered digest for review, reporting, or scheduled automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured feeds are fetched from external network sources and digest history is written to local cache files. <br>
Mitigation: Review configured feed URLs before use and protect or clear the feeds-digest cache if feed history is sensitive. <br>
Risk: Using --llm can send digest content to the configured Perplexity or OpenAI provider. <br>
Mitigation: Use Ollama for local-only summarization or avoid --llm for private or sensitive feeds. <br>
Risk: Python dependencies are version-ranged rather than pinned. <br>
Mitigation: Use a lockfile or pinned dependency set in controlled environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jcbuer/feeds-digest) <br>
- [Data sources 2026](references/data-sources-2026.md) <br>
- [YouTube channel discovery](references/youtube-channel-discovery.md) <br>
- [Microsoft Tech Community categories](references/ms-tc-categories.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON digest text, optionally written to a file, with setup commands and configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optional LLM summaries use the configured Perplexity, OpenAI, or Ollama provider; date windows, topics, feed sources, and maximum items per source are configurable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
