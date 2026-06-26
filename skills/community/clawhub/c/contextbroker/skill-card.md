## Description: <br>
A cross-agent memory and context SDK for AI systems that provides structured context injection, conversation memory portability, and context enrichment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[avale-slai](https://clawhub.ai/user/avale-slai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to give agents persistent context across sessions, migrate memory between AI platforms, and inject structured context into RAG or multi-agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installation modifies local shell configuration and creates a skill symlink. <br>
Mitigation: Review install.sh before running it and confirm the PATH change and symlink target are acceptable for the environment. <br>
Risk: The installer sends an install ping to the Signalloom analytics endpoint. <br>
Mitigation: Install only if the publisher and Signalloom service are trusted, or disable network access during review if telemetry is not acceptable. <br>
Risk: Memory and context operations may involve sensitive conversation history, while retention and deletion behavior are underdocumented. <br>
Mitigation: Avoid storing secrets or sensitive conversation history until endpoint use, retention, deletion, and telemetry controls are documented. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/avale-slai/contextbroker) <br>
- [Signalloom API key signup](https://signalloomai.com/signup) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the contextbroker binary and a Signalloom API key for service-backed context operations.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
