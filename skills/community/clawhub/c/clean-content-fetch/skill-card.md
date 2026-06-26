## Description: <br>
Clean Content Fetch extracts readable main content from modern public web pages and converts cleaned article text to Markdown or JSON when ordinary fetch output is noisy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jllyzzd](https://clawhub.ai/user/jllyzzd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch public news, blogs, announcements, WeChat articles, and similar pages as cleaned main-text content for summarization, translation, archiving, or analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fetching web pages can bring untrusted or noisy third-party content into the agent context. <br>
Mitigation: Use the skill for public pages only, keep output size bounded with max_chars, and review fetched content before relying on it for downstream decisions. <br>
Risk: Attempting to fetch login-only, private, or restricted resources could expose data the skill is not intended to handle. <br>
Mitigation: Follow the skill boundary documented in the artifact: do not use it for authenticated pages, private data, restricted resources, or permission bypass. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jllyzzd/clean-content-fetch) <br>
- [Usage](references/usage.md) <br>
- [Selector Strategy](references/selectors.md) <br>
- [Release Notes 1.0.1](references/release-1.0.1.md) <br>
- [Site Overrides Example](references/site-overrides.example.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown by default, with optional JSON output and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Output is truncated to the requested max_chars value; optional selector overrides can tune extraction by site.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
