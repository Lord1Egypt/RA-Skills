## Description: <br>
DiskMan helps agents scan, analyze, clean, and migrate directories for disk space management with rule-based and optional AI-enhanced recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[heyy259](https://clawhub.ai/user/heyy259) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical users use this skill to find large directories, assess cleanup or migration options, and run risk-aware disk space management workflows through CLI, Python, or MCP tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can delete, move, link, and scan directories, which may affect important local data. <br>
Mitigation: Use dry-run first, verify exact resolved paths before cleanup or migration, back up important folders, and avoid elevated privileges unless necessary. <br>
Risk: Optional AI analysis can send directory metadata or project path information to an external provider. <br>
Mitigation: Prefer rule-based mode or a local AI provider for sensitive paths, and review AI provider configuration before enabling network-backed analysis. <br>
Risk: Cleanup or migration recommendations may be incorrect for unfamiliar directories. <br>
Mitigation: Treat recommendations as advisory, review high-risk findings manually, and require explicit user confirmation before destructive or filesystem-changing operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/heyy259/diskman) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples, JSON configuration snippets, filesystem paths, risk labels, and operation summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce dry-run cleanup summaries, migration plans, symbolic-link status, and optional AI-backed recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and user changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
