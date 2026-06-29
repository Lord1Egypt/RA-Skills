## Description: <br>
Searches Bilibili videos by keyword through the RedFox API, with sorting, time-range filters, pagination, and optional daily keyword subscription guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redfox-data](https://clawhub.ai/user/redfox-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users such as Bilibili creators, operations teams, data analysts, brands, and MCNs use this skill to search recent Bilibili videos, compare keyword performance, adjust filters, and review results in a Markdown table. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a RedFox API key and sends Bilibili search keywords to redfox.hk. <br>
Mitigation: Install only when that credential and keyword-sharing posture is acceptable; keep the key in an environment variable and avoid exposing it in prompts, logs, or files. <br>
Risk: Daily keyword subscriptions can continue running after initial setup if the user forgets how they were scheduled. <br>
Mitigation: Use a visible scheduler and record how to disable or update the subscription before enabling recurring searches. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/bilibili-keywords-search) <br>
- [RedFoxHub API key settings](https://redfox.hk/settings/api-keys?source=clawhub) <br>
- [RedFoxHub](https://redfox.hk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown tables and guidance generated from JSON search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY and sends user-provided Bilibili search keywords to redfox.hk.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
