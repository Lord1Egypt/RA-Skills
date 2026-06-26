## Description: <br>
Free multi-engine web search via ddgs CLI (DuckDuckGo, Google, Bing, Brave, Yandex, Yahoo, Wikipedia) and arXiv API search with no API keys required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[camopel](https://clawhub.ai/user/camopel) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, researchers, and agent builders use this skill to run web searches across multiple engines, discover arXiv papers, and provide a JSON search backend for OpenClaw-compatible workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to external search providers and arXiv. <br>
Mitigation: Avoid confidential or sensitive queries unless the user is comfortable with those third-party services receiving the query text. <br>
Risk: Installation may install the ddgs Python package and add a local command wrapper under ~/.local/bin. <br>
Mitigation: Review installation changes before running the installer and confirm the local PATH impact in managed environments. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/camopel/ddgs-search) <br>
- [OpenClaw project](https://github.com/camopel/openclaw) <br>
- [arXiv API endpoint](https://export.arxiv.org/api/query) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON search results plus Markdown command and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Web search results include title, URL, snippet, and date fields; arXiv results can include authors, categories, abstracts, and publication dates.] <br>

## Skill Version(s): <br>
1.2.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
