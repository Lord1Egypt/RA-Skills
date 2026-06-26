## Description: <br>
Searches arXiv for papers on a user-specified topic, analyzes titles and abstracts, summarizes research hotspots and trends, and can set optional recurring monitoring after user confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[songxf1024](https://clawhub.ai/user/songxf1024) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and technical teams use this skill to find recent arXiv papers for a topic, review title-and-abstract based summaries, identify hotspots, and optionally monitor the same query on a recurring schedule. <br>

### Deployment Geography for Use: <br>
Global; default scheduling timezone is Asia/Shanghai. <br>

## Known Risks and Mitigations: <br>
Risk: Recurring monitoring jobs and saved search settings can persist until edited, disabled, or removed. <br>
Mitigation: Confirm the schedule, timezone, and session target with the user before enabling monitoring, and provide clear update or cancellation guidance. <br>
Risk: Default scheduling uses Asia/Shanghai, which may not match users outside China. <br>
Mitigation: Ask users to confirm timezone-sensitive schedules when their locale or requested delivery time is ambiguous. <br>
Risk: The search script depends on the Python arxiv package. <br>
Mitigation: Install the arxiv dependency from a trusted package source before running the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/songxf1024/arxiv-paper-searcher) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON search or scheduling payloads, and shell command snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Paper analysis is based on arXiv title and abstract metadata; optional monitoring records local configuration and OpenClaw cron job binding details.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
