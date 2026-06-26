## Description: <br>
Real-time web search, autosuggest, spellcheck, and AI-powered answers using the official Brave Search API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[broedkrummen](https://clawhub.ai/user/broedkrummen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve current web results, search suggestions, spell corrections, and cited Brave Answers responses for documentation lookup, fact finding, current events, and research workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries, answer prompts, and optional location context are sent to Brave using the configured API keys. <br>
Mitigation: Avoid secrets, regulated data, and sensitive personal data in queries; review Brave account settings, usage, and data handling expectations before deployment. <br>
Risk: The security evidence notes user input in shell-like command templates. <br>
Mitigation: Run the skill in an agent runtime that passes arguments with argv-style escaping and review generated commands before execution. <br>
Risk: The release requires sensitive Brave API credentials. <br>
Mitigation: Store keys in environment variables or a local secret manager, do not paste keys into prompts or committed files, and rotate keys if exposed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/broedkrummen/brave-api-search) <br>
- [Brave Search API](https://brave.com/search/api/) <br>
- [Brave API Dashboard](https://api-dashboard.search.brave.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown and plain text command output with result URLs, citations, suggestions, corrections, entity summaries, usage details, and setup guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on Brave API responses and configured API keys; cited answers and entity extraction require streaming mode.] <br>

## Skill Version(s): <br>
4.2.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
