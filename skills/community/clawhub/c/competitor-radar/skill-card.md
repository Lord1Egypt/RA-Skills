## Description: <br>
Competitor Radar monitors competitor RSS feeds, GitHub releases, and Hacker News mentions, then uses AI scoring to generate a structured competitor intelligence report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaohuaishu](https://clawhub.ai/user/xiaohuaishu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, product teams, and competitive intelligence analysts use this skill to monitor named competitors across public release channels and produce a concise Markdown report of notable updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence reports an embedded API key and AI-scoring prompts sent to a local LLM gateway. <br>
Mitigation: Review or edit the LLM configuration before installing, remove and rotate the embedded key, and prefer running with --no-ai unless the local service is trusted. <br>
Risk: The security evidence advises avoiding the undocumented _write_radar.py helper. <br>
Mitigation: Use radar.py directly for normal operation and inspect helper scripts before executing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaohuaishu/competitor-radar) <br>
- [Publisher profile](https://clawhub.ai/user/xiaohuaishu) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report, optionally written to a file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses configurable competitor entries and can run without AI scoring via --no-ai.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
