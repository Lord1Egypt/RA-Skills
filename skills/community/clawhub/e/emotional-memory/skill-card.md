## Description: <br>
Gives AI agents emotional continuity across sessions by tagging meaningful moments, consolidating memories on a schedule, and generating a self-model from accumulated experience. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[artemis-lgtm](https://clawhub.ai/user/artemis-lgtm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw agent operators use this skill to record emotionally significant session moments, schedule memory consolidation, and maintain a self-model that can be loaded for continuity across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local memory files can contain privacy-sensitive session details if sensitive information is logged. <br>
Mitigation: Avoid recording secrets, private user details, medical information, or financial information, and periodically review or delete emotional-index.jsonl, continuity.jsonl, self-model.md, and consolidation reports. <br>
Risk: Scheduled consolidation and self-model jobs continue updating memory state over time. <br>
Mitigation: Enable cron jobs only when ongoing memory updates are intended, and configure the memory directory deliberately. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/artemis-lgtm/emotional-memory) <br>
- [Publisher profile](https://clawhub.ai/user/artemis-lgtm) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; runtime scripts write JSONL and Markdown memory files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local emotional memory state under EMOTIONAL_MEMORY_DIR, OPENCLAW_WORKSPACE/memory, or ./memory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
