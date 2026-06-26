## Description: <br>
CZSC Chan-theory technical analysis skill for K-line generation, stroke and segment recognition, fractal signal extraction, and A-share backtest visualization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangweigang-jpg](https://clawhub.ai/user/tangweigang-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and finance researchers use this skill to build A-share quantitative strategy workflows with ZVT and CZSC, including data collection, signal computation, backtesting, and report or visualization generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can generate and run finance data and backtest code, including dependency installation. <br>
Mitigation: Use an isolated environment and review generated code, package choices, and execution commands before running them. <br>
Risk: The skill may use external data providers or integrations that require paid-provider, broker, OAuth, or sensitive credentials. <br>
Mitigation: Provide credentials only for integrations you intend to use, scope them narrowly, and verify generated code destinations before execution. <br>
Risk: The skill may write local ZVT data and saved skill files. <br>
Mitigation: Set explicit writable data paths, review filesystem destinations, and avoid sharing workspaces that contain private market data or credentials. <br>
Risk: Security evidence marks the release suspicious because its behavior is broader than the narrow CZSC listing suggests. <br>
Mitigation: Review the scanner guidance and artifact behavior before deployment, especially for credential use, uploads, and persistent setup. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tangweigang-jpg/czsc-chan-theory) <br>
- [Known Use Cases](references/USE_CASES.md) <br>
- [Semantic Locks and Preconditions](references/LOCKS.md) <br>
- [Component Capability Map](references/COMPONENTS.md) <br>
- [Constraints](references/CONSTRAINTS.md) <br>
- [Anti-Patterns](references/ANTI_PATTERNS.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide local ZVT data setup, external data-provider access, and backtest/report file generation.] <br>

## Skill Version(s): <br>
0.3.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
