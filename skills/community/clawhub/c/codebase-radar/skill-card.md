## Description: <br>
Scan codebase for dependency graph, tech debt hotspots, and module health scores. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use Codebase Radar to inspect repositories for dependency structure, tech debt signals, circular dependencies, and module health scores before planning maintenance or refactoring work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The ClawHub security review flags the release as suspicious because an autoreview helper may bypass sandbox and approval protections by default. <br>
Mitigation: Review before installing, use only in trusted repositories, and disable the full-access autoreview default unless that behavior is explicitly required. <br>
Risk: Large repositories can increase scan time or memory use. <br>
Mitigation: Use a max-files limit for large repositories and review generated reports before acting on refactoring recommendations. <br>


## Reference(s): <br>
- [Codebase Radar on ClawHub](https://clawhub.ai/harrylabsj/codebase-radar) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, or Mermaid dependency graph output depending on command options] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only analysis output; large repositories may require a max-files limit.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
