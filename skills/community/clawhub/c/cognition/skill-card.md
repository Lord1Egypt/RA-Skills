## Description: <br>
Cognition gives OpenClaw agents a practical memory architecture for commitments, prior context, repeat-mistake prevention, staged durable-memory updates, reusable procedures, and memory hygiene. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zurbrick](https://clawhub.ai/user/zurbrick) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Cognition to add local persistent memory practices to OpenClaw agents, including session logs, durable knowledge, commitments, reusable procedures, and staged consolidation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory files may capture secrets or sensitive personal data if users store them there. <br>
Mitigation: Do not store secrets or sensitive personal data in memory files, and periodically review durable memory and FUTURE_INTENTS entries. <br>
Risk: Scheduled consolidation or reflection can create ongoing local reports that may include incorrect or stale proposals. <br>
Mitigation: Keep consolidation staged and append-only, require review before durable memory changes, and tag uncertain entries for review. <br>


## Reference(s): <br>
- [Cognition Architecture Notes](references/architecture.md) <br>
- [Cognition Protocol Blocks for AGENTS.md](references/protocols.md) <br>
- [Nightly Consolidation - Safe Staging Prompt](references/consolidation-prompt.md) <br>
- [Weekly Reflection - Memory Hygiene Prompt](references/weekly-reflection-prompt.md) <br>
- [Cognition - Tier 2 Retrieval Configuration](references/config.md) <br>
- [Cognitive Science Appendix](references/cognitive-science.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with bash commands, JSON and YAML templates, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local workspace memory files; staged consolidation and reflection reports are append-only unless a reviewed workflow applies changes.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
