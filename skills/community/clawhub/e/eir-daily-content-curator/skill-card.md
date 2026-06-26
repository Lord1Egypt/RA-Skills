## Description: <br>
Daily AI news curation that learns interests from a user profile, searches the web, and produces structured summaries and daily briefs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[heyeir](https://clawhub.ai/user/heyeir) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to set up recurring content curation, search and crawl source material, generate structured summaries, and compile daily news briefs. It supports local standalone output and an opt-in Eir mode for publishing generated summaries with source metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends search queries and crawls source URLs through configured web services. <br>
Mitigation: Use trusted search and crawl providers, review configured topics, and avoid sensitive queries when external providers are enabled. <br>
Risk: Eir mode can post generated summaries, interest topic slugs, source URLs, and source metadata to Eir. <br>
Mitigation: Enable Eir mode only when that data sharing is intended, and review generated content before publishing when accuracy or confidentiality matters. <br>
Risk: Search and Eir credentials are stored in local configuration files or environment variables. <br>
Mitigation: Protect config/eir.json and config/settings.json, keep them out of source control, and rotate tokens if they are exposed. <br>
Risk: Optional personalization can use local audience context in prompts. <br>
Mitigation: Keep personalization disabled unless desired, and omit optional personalized fields when generic output is required. <br>


## Reference(s): <br>
- [Eir Mode Setup Guide](artifact/references/eir-setup.md) <br>
- [Eir API Reference](artifact/references/eir-api.md) <br>
- [Eir Content Specification](artifact/references/content-spec.md) <br>
- [Candidates JSON Format Specification](artifact/references/candidates-spec.md) <br>
- [Eir Interest Rules](artifact/references/eir-interest-rules.md) <br>
- [Interest Extraction Prompt](artifact/references/interest-extraction-prompt.md) <br>
- [Eir Writer Prompt](artifact/references/writer-prompt-eir.md) <br>
- [Standalone Writer Prompt](artifact/references/writer-prompt-standalone.md) <br>
- [Eir](https://www.heyeir.com) <br>
- [Brave Search API](https://brave.com/search/api/) <br>
- [Tavily](https://tavily.com/) <br>
- [SearXNG](https://docs.searxng.org/) <br>
- [Crawl4AI](https://github.com/unclecode/crawl4ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown briefs, JSON content items, task files, and inline shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Standalone mode saves generated content locally; Eir mode can post generated summaries and source metadata to Eir.] <br>

## Skill Version(s): <br>
3.119.0 (source: evidence.release.version and artifact/CHANGELOG.md, released 2026-04-25) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
