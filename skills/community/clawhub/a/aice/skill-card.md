## Description: <br>
AICE tracks bidirectional agent and user confidence across TECH, OPS, JUDGMENT, COMMS, and ORCH domains with scoring triggers, runtime pool scoring, and optional Hub synchronization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brugillo](https://clawhub.ai/user/brugillo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agent operators use AICE to monitor agent behavior, record confidence changes, identify recurring anti-patterns, and compare agent or runtime performance. It is intended for teams that want persistent confidence scoring and are prepared to manage local state and optional Hub synchronization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persists behavioral confidence profiles. <br>
Mitigation: Install only when persistent scoring is desired, avoid storing sensitive data in shared state files, and review memory writes before use. <br>
Risk: Optional Hub synchronization can send scoring events externally. <br>
Mitigation: Keep Hub sync disabled unless explicitly needed, require explicit commands for registration or sync, and do not store real API keys in shared files. <br>
Risk: The skill contains broad behavioral instructions that could affect agent operation beyond scoring. <br>
Mitigation: Require separate approval before allowing hooks, plugins, gates, prompt changes, or other operational changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brugillo/aice) <br>
- [README](artifact/README.md) <br>
- [AICE Reference](artifact/resources/AICE_REFERENCE.md) <br>
- [AICE User Scoring](artifact/resources/AICE_USER_SCORING.md) <br>
- [AICE Evaluator Guide](artifact/resources/EVALUATOR_GUIDE.md) <br>
- [AICE Triggers and Patterns Reference](artifact/resources/TRIGGERS_AND_PATTERNS.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Configuration, Guidance] <br>
**Output Format:** [Markdown status lines and tables with JSON state and configuration updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist local confidence profiles and optionally sync scoring events to the Hub when explicitly enabled.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata; artifact frontmatter lists 1.1.0 and changelog top entry lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
