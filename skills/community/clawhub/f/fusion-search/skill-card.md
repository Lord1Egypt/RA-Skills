## Description: <br>
Fusion Search routes multilingual web search queries across 16 search engines with Playwright-based browsing, result deduplication, quality scoring, and optional full-content extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lvjingxuan-ai](https://clawhub.ai/user/lvjingxuan-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and research agents use this skill to perform multilingual web research from the command line or Python API, combining results from Chinese and international search engines and optionally fetching page text for deeper review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated web scraping through a stealth Playwright browser may have privacy, reliability, or policy implications. <br>
Mitigation: Use the skill only in environments where this behavior is acceptable, avoid sensitive searches, and review results before relying on them. <br>
Risk: The browser launch weakens several Chromium protections. <br>
Mitigation: Run the skill in a contained environment and avoid using it with trusted sessions or sensitive local data. <br>
Risk: Automatic engine routing and full-content fetching can contact multiple search engines and result pages. <br>
Mitigation: Specify an engine when privacy matters and keep full-content fetching disabled unless the task requires it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lvjingxuan-ai/fusion-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, code, shell commands, guidance] <br>
**Output Format:** [JSON search results or human-readable CLI text with titles, URLs, snippets, optional extracted content, engine names, and scores] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search output is ranked and deduplicated; optional full-content extraction is capped by the skill parameters.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
