## Description: <br>
Mines personalized hotwords and ambiguous terms from OpenClaw conversation history and exports vocabulary tables for ASR prompt use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[octoclaws](https://clawhub.ai/user/octoclaws) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to extract per-agent conversation snippets, submit them to an ASR hotword-mining service, and maintain hotword tables that improve transcription of domain-specific terms and proper nouns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private OpenClaw conversation history is uploaded to the configured ASR correction service. <br>
Mitigation: Use only a trusted local or self-hosted HTTPS endpoint and review extracted chat data before submission. <br>
Risk: The skill sends raw LLM provider configuration, including an API key, in the remote task payload. <br>
Mitigation: Remove api_key from the remote payload or use a scoped credential before running the mining workflow. <br>
Risk: The default configuration points to a hard-coded external HTTP endpoint. <br>
Mitigation: Replace the endpoint with a trusted HTTPS service before installation or execution. <br>
Risk: Scheduled runs and optional Telegram or Feishu summaries may share conversation-derived results automatically. <br>
Mitigation: Keep execution manual by default and enable external notifications only after confirming the intended recipients and data handling. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/octoclaws/asr-personal-hotwords) <br>
- [Publisher Profile](https://clawhub.ai/user/octoclaws) <br>
- [asr-corrector Service](https://github.com/asr-corrector) <br>
- [README](artifact/README.md) <br>
- [Skill Instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, csv, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown hotword table by default, with optional JSON, CSV, or plain text exports and a JSON run summary.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads OpenClaw session history and LLM provider configuration, calls a configured ASR correction service, stores dated vocabulary archives, and updates hotwords.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
