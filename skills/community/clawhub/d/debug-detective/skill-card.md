## Description: <br>
Helps agents guide developers through systematic debugging, diagnosis, and profiling across application, system, network, database, and production environments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[royhk920](https://clawhub.ai/user/royhk920) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to investigate software failures, isolate root causes, choose debugging tools, profile performance, and plan verification steps before and after fixes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Debugging commands, traces, and packet captures can expose secrets, private data, or sensitive infrastructure details. <br>
Mitigation: Review examples before running them, avoid placing real secrets directly in shell commands, redact sensitive output, and keep packet captures and traces private. <br>
Risk: Some diagnostics use sudo, packet capture, or production inspection workflows that may affect systems or cross authorization boundaries. <br>
Mitigation: Run privileged or production diagnostics only on systems you are authorized to inspect, and prefer the least invasive commands that can answer the debugging question. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/royhk920/debug-detective) <br>
- [Debug checklist](examples/debug-checklist.md) <br>
- [DevTools cheatsheet](references/devtools-cheatsheet.md) <br>
- [Profiling tools guide](references/profiling-tools-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline code, shell commands, checklists, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
