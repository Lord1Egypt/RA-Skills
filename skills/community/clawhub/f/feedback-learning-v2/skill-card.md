## Description: <br>
Zero-LLM feedback learning system for OpenClaw agents that detects feedback, logs events, tracks positive and negative patterns, promotes structured rules, and generates weekly reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Surdeddd](https://clawhub.ai/user/Surdeddd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add local feedback capture, pattern analysis, rule promotion, and weekly learning reports to OpenClaw-style agent workflows. It is intended for teams that want a shell and Python based feedback memory without LLM calls or API keys. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist local feedback, command-failure details, generated rules, and reports on disk. <br>
Mitigation: Restrict permissions on the learning directory, avoid automatic error-hook capture during secret-heavy work, and periodically delete or archive logs and reports that are no longer needed. <br>
Risk: Promoted rules may encode incorrect or stale behavior if repeated feedback patterns are misunderstood. <br>
Mitigation: Review generated genes before relying on them, mark stale or resolved rules explicitly, and use reports to monitor recurring unresolved patterns. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Surdeddd/feedback-learning-v2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell and Python command examples; runtime scripts produce JSON, JSONL, and Markdown files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No API keys are required; outputs are stored locally under the configured feedback learning directory.] <br>

## Skill Version(s): <br>
2.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
