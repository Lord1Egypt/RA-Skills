## Description: <br>
Generate a daily AI news newsletter for a Chinese audience from fresh web sources and return the newsletter body and article summaries in Simplified Chinese. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[j3ffyang](https://clawhub.ai/user/j3ffyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content teams, analysts, and AI practitioners use this skill to gather, verify, rank, and summarize recent AI news into a Simplified Chinese newsletter with source metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires API credentials for web search and fetching. <br>
Mitigation: Provide only the required BRAVE_API_KEY and FIRECRAWL_API_KEY values in the intended runtime environment and avoid exposing them in generated newsletter output. <br>
Risk: Web-sourced news can be stale, inconsistent, malformed, or off topic. <br>
Mitigation: Use the skill's verification, duplicate removal, fallback search, and warning records; review source links before redistribution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/j3ffyang/ai-newsletter-chn-for-hermes) <br>
- [Publisher profile](https://clawhub.ai/user/j3ffyang) <br>
- [Author profile](https://github.com/j3ffyang) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON] <br>
**Output Format:** [Simplified Chinese Markdown newsletter plus JSON newsletter data, article summaries, source metadata, and warnings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preserves article title, URL, domain, published date, relevance score, and source query metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
