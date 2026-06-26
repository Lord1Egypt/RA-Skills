## Description: <br>
Searches Douyin in real time through the RedFox API, returning recent works for a keyword with sort, time-window, pagination, and optional daily subscription support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redfox-data](https://clawhub.ai/user/redfox-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content operators, strategy researchers, creators, influencers, and brand teams use this skill to monitor current Douyin content, compare engagement signals, explore recent posts by keyword, and subscribe to daily keyword updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Douyin search keywords and filters are sent to RedFox with the user's API key. <br>
Mitigation: Avoid sensitive keywords, use a revocable RedFox API key, and confirm the key source, scope, expiration, and reset process before use. <br>
Risk: The required REDFOX_API_KEY could be exposed if it is copied into prompts, code, logs, or output files. <br>
Mitigation: Store REDFOX_API_KEY only in environment or secret configuration and do not hardcode or print it. <br>
Risk: The optional daily subscription can create recurring scheduled searches. <br>
Mitigation: Only confirm subscription when recurring monitoring is intended, and remove the platform schedule or crontab entry when it is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/redfox-data/douyin-realtime-search) <br>
- [RedFoxHub API key settings](https://redfox.hk/settings/api-keys?source=clawhub) <br>
- [RedFoxHub](https://redfox.hk?source=github) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON from the search script and Markdown tables or guidance in agent responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY; accepts keyword, sort order, publish-time window, and page; can create an opt-in daily subscription at 10:00.] <br>

## Skill Version(s): <br>
1.0.4 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
