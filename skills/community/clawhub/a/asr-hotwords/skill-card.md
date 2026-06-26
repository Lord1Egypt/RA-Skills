## Description: <br>
Mines OpenClaw conversation histories for ASR hotwords and ambiguous terms, then exports a unified hotword table for speech recognition prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lovejing0306](https://clawhub.ai/user/lovejing0306) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and agents use this skill to extract frequently used Chinese terms, proper nouns, and ambiguous phrases from prior conversations so ASR prompts can better preserve domain-specific vocabulary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill scans private OpenClaw conversation histories and uses the configured LLM provider credentials. <br>
Mitigation: Limit config.yaml to the intended agents and dates, use scoped provider credentials, and run only in environments where processing those conversations is approved. <br>
Risk: The generated hotwords can be injected into downstream DMWork voice correction context without clear per-run user approval. <br>
Mitigation: Review hotwords.md before injection and avoid the background install test or automated update path unless that behavior is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lovejing0306/asr-hotwords) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, CSV, Text, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown hotword prompt file with optional JSON, CSV, or plain-text exports and JSON run summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exports hotwords.md by default, can filter by date range and minimum frequency, and may update downstream voice correction context.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
