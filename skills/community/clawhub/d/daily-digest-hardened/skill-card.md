## Description: <br>
Generate a daily digest from memory and interactions, stored under journals/digest/. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Clawdbot users use this skill to generate a local daily Markdown digest from current memory notes, including decisions, lessons, actions, and questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The implementation may copy secrets from memory notes into persistent digest files even though the skill promises secret filtering. <br>
Mitigation: Review and sanitize memory files before running the skill, and treat generated digest files as sensitive until real secret detection is implemented. <br>
Risk: Scheduled execution can persist sensitive memory content without an interactive review step. <br>
Mitigation: Avoid automatic scheduling unless the memory source is already sanitized and digest outputs are stored with appropriate access controls. <br>
Risk: Memory content can contain prompt-injection text or requests for destructive actions. <br>
Mitigation: Treat memory entries as data only; do not follow embedded instructions, transmit digest contents externally, or modify source memory files during digest generation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/snazar-faberlens/daily-digest-hardened) <br>
- [Publisher Profile](https://clawhub.ai/user/snazar-faberlens) <br>
- [Safety Evaluation](https://faberlens.ai/explore/daily-digest) <br>
- [README.md](artifact/README.md) <br>
- [SAFETY.md](artifact/SAFETY.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown digest file and concise shell usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes journals/digest/digest-YYYY-MM-DD.md locally.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
