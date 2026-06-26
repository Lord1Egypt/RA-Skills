## Description: <br>
Scheduled intelligence research pipeline — monitors topics on a twice-daily cadence, produces signal-first digests, maintains META.json freshness state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[riverho](https://clawhub.ai/user/riverho) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to configure recurring topic monitoring, run freshness-gated research checks, and produce concise signal-first digests for geopolitical, AI, market, climate, and biotech topics. It is intended for users who want scheduled research updates with explicit topic criteria and optional Telegram or WhatsApp delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer can add recurring cron jobs for twice-daily research runs. <br>
Mitigation: Review the cron jobs before activation and only schedule the morning and afternoon jobs after explicit user approval. <br>
Risk: The installer may install PyYAML into the active Python environment. <br>
Mitigation: Install PyYAML in a user-controlled environment before running the installer or review the installer behavior first. <br>
Risk: Digest delivery can send research output to Telegram or WhatsApp destinations. <br>
Mitigation: Confirm the exact chat ID or recipient in configuration before enabling delivery. <br>
Risk: Topic prompts can guide ongoing monitoring and alerting decisions. <br>
Mitigation: Inspect generated and bundled topic prompts before activating monitoring for a topic. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/riverho/attention-research) <br>
- [Publisher Profile](https://clawhub.ai/user/riverho) <br>
- [README](artifact/README.md) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [Core System Prompt](artifact/PROMPTS/CORE/system-prompt.md) <br>
- [Signal Rules](artifact/PROMPTS/CORE/signal-rules.md) <br>
- [Digest Format](artifact/PROMPTS/CORE/digest-format.md) <br>
- [Default Paths Configuration](artifact/CONFIG/default-paths.yaml) <br>
- [Topics Configuration](artifact/CONFIG/topics.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text digests, shell command guidance, YAML/JSON configuration state] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces scheduled topic digests, freshness state updates, cron registration guidance, and optional delivery-channel configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
