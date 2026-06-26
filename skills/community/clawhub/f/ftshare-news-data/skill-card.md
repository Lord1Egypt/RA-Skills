## Description: <br>
Searches market.ft.tech news semantically by query and returns related recent news results with source sites and article links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shawn92](https://clawhub.ai/user/shawn92) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to search A-share and market news by semantic query or keyword and present recent results with source and link information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: News search terms and optional time filters are sent to market.ft.tech. <br>
Mitigation: Use the skill only for prompts that explicitly require FT or market.ft.tech news search, and avoid sending sensitive query text. <br>
Risk: The upstream data range is limited to current-year news and roughly the most recent half month. <br>
Mitigation: Tell users about the time-range limit when presenting results and avoid using this skill for historical news research. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shawn92/ftshare-news-data) <br>
- [Publisher profile](https://clawhub.ai/user/shawn92) <br>
- [market.ft.tech news search endpoint](https://market.ft.tech/data/api/v1/market/data/semantic-search-news) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [JSON from the handler, typically summarized for users in Markdown with source and article links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results are limited by the upstream service to current-year news and roughly the most recent half month; optional time filters are normalized to UTC+8.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
