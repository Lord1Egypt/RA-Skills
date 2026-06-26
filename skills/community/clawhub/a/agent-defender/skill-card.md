## Description: <br>
Agent Defender provides static scanning, runtime protection, and DLP checks for AI agent skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caidongyun](https://clawhub.ai/user/caidongyun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use Agent Defender to scan AI agent skills, inspect rule matches, run DLP checks, and optionally monitor runtime behavior before deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Autonomous rule-development, rule-sync, backup/restore, and cross-project execution features can repeatedly run or modify local rules. <br>
Mitigation: Review the control scripts, imported rules, and sync sources before use; run in an isolated workspace and avoid starting background daemons unless required. <br>
Risk: Runtime-protection claims may be limited until independently tested. <br>
Mitigation: Treat scan and runtime results as advisory, validate them against representative samples, and keep human review in the deployment workflow. <br>
Risk: Cross-project sync can import rules or behavior from sibling projects that may not be trusted. <br>
Mitigation: Use only trusted sync sources, inspect imported rule changes, and keep backups before applying updates. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/caidongyun/agent-defender) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>
- [README_SIGMA_YARA.md](artifact/README_SIGMA_YARA.md) <br>
- [QUICK_REFERENCE.md](artifact/QUICK_REFERENCE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown documentation, shell commands, JSON/YAML rules, and Python code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify local rule files, backups, sync reports, and scan reports when helper scripts are executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
