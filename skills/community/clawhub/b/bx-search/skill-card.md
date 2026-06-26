## Description: <br>
Web search using the Brave Search CLI (`bx`) for current information, documentation lookup, troubleshooting research, RAG grounding, news, media, local places, and AI-synthesized answers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brave-skills](https://clawhub.ai/user/brave-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to route web-search and research tasks through the Brave Search CLI for grounded current information, documentation lookup, troubleshooting, and synthesized answers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries may disclose secrets, confidential text, or sensitive context to the Brave Search API. <br>
Mitigation: Use a dedicated Brave Search API key and avoid sending secrets or confidential text in search queries. <br>
Risk: Precise local-place or location searches may reveal sensitive location context. <br>
Mitigation: Use coarse location terms when possible and review queries before submitting precise latitude, longitude, city, or address data. <br>
Risk: Remote installers and downloaded binaries can introduce supply-chain risk. <br>
Mitigation: Inspect or verify the installer and binary source before installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brave-skills/bx-search) <br>
- [Brave Search API](https://brave.com/search/api/) <br>
- [Skill repository metadata](https://github.com/brave/brave-search-skills/tree/main/clawhub/bx-search) <br>
- [Issue tracker](https://github.com/brave/brave-search-skills/issues) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires `bx` and `BRAVE_SEARCH_API_KEY`; search tasks may return JSON search results, token-budgeted context, or streaming answer chunks.] <br>

## Skill Version(s): <br>
1.4.0 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
