## Description: <br>
EFT - Emotional Framework Translator detects, measures, and explains emotional patterns in AI model responses with 10 emotion labels, per-sentence analysis, narrative arc detection, and local dashboard/API access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marceloadryao](https://clawhub.ai/user/marceloadryao) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, AI safety reviewers, and researchers use this skill to monitor emotional patterns in AI agent responses, inspect sentence-level emotion classifications, and review recent analysis history through local dashboard and JSON endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill records analyzed agent responses and keeps local history. <br>
Mitigation: Use it only in sessions without secrets, personal data, regulated data, or proprietary work unless a protected log path and log purge process are configured. <br>
Risk: Recent history is exposed through unauthenticated local HTTP APIs. <br>
Mitigation: Restrict gateway access to trusted local clients and add authentication or remove wildcard CORS before use in sensitive environments. <br>
Risk: The skill runs a configurable local Python/Rust analysis engine on captured text. <br>
Mitigation: Verify the engine source and dependencies before installation and configure paths only to trusted local files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/marceloadryao/enginemind-eft) <br>
- [Publisher profile](https://clawhub.ai/user/marceloadryao) <br>
- [EFT Documentation](artifact/EFT_DOCUMENTATION.md) <br>
- [EFT Scientific Evidence](artifact/EFT_SCIENTIFIC_EVIDENCE.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, JSON, Files, Configuration instructions] <br>
**Output Format:** [JSON analysis records, JSONL local history, and dashboard views] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python according to ClawHub metadata; analyzes captured agent responses and retains recent history locally.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
