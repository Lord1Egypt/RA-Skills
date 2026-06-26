## Description: <br>
Searches Douyin works in real time through Redfox by keyword, with sorting, publish-time filters, pagination, and optional daily subscription prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuanyi-github](https://clawhub.ai/user/yuanyi-github) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content operators, strategy researchers, creators, and brand teams use this skill to retrieve current Douyin works for keywords, compare engagement signals, and monitor recurring topics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search keywords are shared with Redfox and the REDFOX_API_KEY must be stored locally. <br>
Mitigation: Use a scoped, revocable API key where available, avoid sensitive search terms, and keep the key out of prompts, logs, code, and shared output. <br>
Risk: The subscription flow may create recurring daily searches without enough cancellation and control detail. <br>
Mitigation: Before enabling subscriptions, confirm the exact scheduled task, runtime location, notification target, and cancellation process. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuanyi-github/douyin-realtime-search-redfox) <br>
- [RedFoxHub API key settings](https://redfox.hk/settings/api-keys?source=clawhub) <br>
- [RedFoxHub](https://redfox.hk) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown tables and short guidance; the bundled search script returns JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a locally configured REDFOX_API_KEY and user-provided search keyword.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
