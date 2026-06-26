## Description: <br>
Auto-capture hourly session highlights and update daily memory files to keep long-term memory continuous. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raydez](https://clawhub.ai/user/raydez) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and operators use this skill to summarize recent OpenClaw session activity into daily memory entries, either on an hourly schedule or from manual prompts such as "remember this" and "log today". <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recent session activity may be saved automatically into persistent local memory files without sufficient consent, retention, or sensitive-data controls. <br>
Mitigation: Prefer manual triggering or explicit confirmation; add secret and PII redaction, retention limits, and controls to inspect, disable, and delete ~/.openclaw/workspace/memory entries before enabling cron mode. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/raydez/auto-memory-keeper) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown daily memory entries with supporting command snippets and JSON configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates persistent local daily memory files under ~/.openclaw/workspace/memory and deduplicates similar entries using a configurable threshold.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
