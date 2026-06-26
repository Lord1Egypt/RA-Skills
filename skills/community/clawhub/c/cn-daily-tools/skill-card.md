## Description: <br>
A Chinese daily utilities skill for weather forecasts, exchange-rate lookups, news summaries, and package tracking without API-key setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[27555402-spec](https://clawhub.ai/user/27555402-spec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Chinese-speaking users use this skill to ask an agent for everyday weather, currency conversion, news-summary, and package-tracking assistance in Chinese. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live web lookups for weather, exchange rates, news, or delivery status may return stale, unavailable, or source-dependent information. <br>
Mitigation: Have the agent identify the lookup source and timestamp when reporting current information, and ask users to verify important decisions against authoritative services. <br>
Risk: Package tracking requests may include personal delivery details. <br>
Mitigation: Avoid sharing sensitive tracking numbers or personal delivery information unless the user accepts the lookup source and privacy tradeoff. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/27555402-spec/cn-daily-tools) <br>
- [Publisher profile](https://clawhub.ai/user/27555402-spec) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Chinese Markdown responses with concise summaries, recommendations, and source links when news is summarized.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No scripts, install hooks, credentials, persistence, or hidden behavior were found in the inspected artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
