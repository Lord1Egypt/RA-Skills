## Description: <br>
Cpu is a Bash-based local operations journal that records, searches, summarizes, and exports sysops notes under ~/.local/share/cpu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain3](https://clawhub.ai/user/bytesagain3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators can use this skill to record local scan notes, monitoring observations, alerts, fixes, cleanup actions, backups, restores, benchmarks, and comparisons. It should be treated as a plaintext journal, not as an authoritative CPU load, temperature, or process-monitoring tool. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may mistake Cpu for a real CPU monitor even though the security evidence says it stores searchable local operations notes. <br>
Mitigation: Describe it as a plaintext operations journal and use a separate trusted system tool for actual CPU load, temperature, or top-process data. <br>
Risk: Operational notes entered into Cpu are stored locally in plaintext and may later be exported. <br>
Mitigation: Do not enter passwords, tokens, private incident notes, sensitive hostnames, or backup details unless plaintext local storage and export are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bytesagain3/cpu) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with bash command examples; runtime commands write local log files and optional JSON, CSV, or TXT exports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local plaintext files under ~/.local/share/cpu and does not require network access, external dependencies, or API keys.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
