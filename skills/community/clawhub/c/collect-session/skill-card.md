## Description: <br>
Installs and configures an OpenClaw hook that captures session telemetry, model usage, cost data, and Markdown summaries when /new or /reset is issued. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[virtualpaul](https://clawhub.ai/user/virtualpaul) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install and troubleshoot local session collection for searchable work history, telemetry review, and cost tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Session contents and tool-use metadata are intentionally stored as local memory and may include secrets, credentials, customer data, or sensitive personal material. <br>
Mitigation: Use a controlled output directory, restrict file access, define deletion and retention practices, and avoid collecting sensitive sessions unless redaction and retention controls are in place. <br>
Risk: LLM enrichment can send sampled session text to the configured LiteLLM provider for naming and summarization. <br>
Mitigation: Confirm the provider and data-handling policy before enabling enrichment, or run with --no-llm or without LITELLM_API_KEY for sensitive sessions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/virtualpaul/collect-session) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, configuration, shell commands, code, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The installed collector writes session Markdown files, SESSION-INDEX.md, and session-log.jsonl records.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
