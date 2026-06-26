## Description: <br>
A broad OpenClaw multi-skill bundle for vulnerability scanning, API test generation, document summarization, watchdog monitoring, code conversion, sandbox script execution, security alerts, trading and NFT research, UX analysis, and 3D model workflow guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rioo-maker](https://clawhub.ai/user/rioo-maker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this OpenClaw skill pack to add multiple agent workflows, including authorized website vulnerability checks, API example generation, code conversion, summarization, monitoring, market research, and design review. Users should select only the bundled workflows they intend to use and review higher-risk capabilities before enabling them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundle includes a sandbox script executor and dependency-install guidance that may run user-provided code or install packages. <br>
Mitigation: Review or remove the sandbox execution workflow before deployment, run only trusted code, and keep execution in a constrained sandbox. <br>
Risk: The bundle includes financial and NFT research workflows that may influence trading or collection decisions. <br>
Mitigation: Use outputs as research support only, require human review, and avoid connecting the skill directly to real trading or wallet actions. <br>
Risk: The auto-watchdog workflow can run monitoring for long or indefinite periods and collect information from external sources. <br>
Mitigation: Set explicit monitoring duration, sources, and stop conditions before use. <br>
Risk: Some workflows may process private documents, API tokens, logged-in browser sessions, or service access. <br>
Mitigation: Do not provide secrets or logged-in access unless the data exposure is understood and approved for the environment. <br>
Risk: Vulnerability scanning workflows can be misused against systems the user does not own or control. <br>
Mitigation: Run scanning only against explicitly authorized targets and manually verify results before acting on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rioo-maker/12-cool-skills-openclaw-agent) <br>
- [Trading Strategies](artifact/references/trading_strategies.md) <br>
- [API Testing Patterns](artifact/references/api_patterns.md) <br>
- [Sandbox Script Execution Guide](artifact/references/execution_guide.md) <br>
- [Threat Indicators](artifact/references/threat_indicators.md) <br>
- [Common DevTools Issues](artifact/references/devtools_issues.md) <br>
- [Information Sources for Auto-Watchdog](artifact/references/sources.md) <br>
- [NFT Scouting Guide](artifact/references/nft_scouting_guide.md) <br>
- [UX Design Analysis Reference](artifact/references/ux_principles.md) <br>
- [Code Conversion Patterns](artifact/references/conversion-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with code blocks, command examples, generated reports, and workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference bundled scripts and templates; some workflows depend on user-provided targets, documents, API details, market data, or service access.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
