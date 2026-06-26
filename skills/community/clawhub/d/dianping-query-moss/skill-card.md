## Description: <br>
Queries Dianping restaurant information, including restaurant ratings, average spend, addresses, cuisine or area search results, and nearby food recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MemoryF](https://clawhub.ai/user/MemoryF) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to search Dianping for Hangzhou-focused restaurant recommendations or details such as ratings, prices, locations, dishes, and review summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review flags that the skill asks the agent to use a named Dianping account and may involve phone or SMS login. <br>
Mitigation: Complete any login directly in Dianping's own UI, do not paste SMS codes or credentials into chat, and confirm the active account before browsing. <br>
Risk: The security review flags a Hangzhou location workaround that can conflict with the account's Beijing location context. <br>
Mitigation: Confirm the city context before relying on results and use the Hangzhou URL or city-scoped search terms when Hangzhou results are required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MemoryF/dianping-query-moss) <br>
- [Dianping Hangzhou page](https://www.dianping.com/hangzhou) <br>
- [Dianping AI search URL pattern](https://www.dianping.com/ai-search?keyword=...) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or concise text summaries of Dianping restaurant search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include restaurant names, ratings, average spend, addresses, cuisine notes, recommended dishes, review summaries, and city-scoped search guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
