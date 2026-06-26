## Description: <br>
Analyzes software projects and generates a structured Markdown documentation system using Intent, Contract, and Constraint tracks, intelligent grouping, template derivation, and an 18-dimension completeness check. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leonardo-lb](https://clawhub.ai/user/leonardo-lb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to create or redesign a repository documentation system, including project analysis, document grouping, Markdown templates, entry files, and completeness checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads a repository and writes documentation, so generated files may contain incorrect project assumptions or stale technical details. <br>
Mitigation: Run it on a clean branch and review generated documentation before committing or relying on it. <br>
Risk: The workflow can copy a helper shell script into the target project. <br>
Mitigation: Review the copied md-sections.sh script and any generated shell commands before execution or commit. <br>
Risk: Optional field research may expose private project context if used on sensitive repositories. <br>
Mitigation: Decline optional web research when working with private code, confidential architecture, or sensitive documentation. <br>


## Reference(s): <br>
- [Three Track Philosophy](references/three-track-philosophy.md) <br>
- [Grouping Detection](references/grouping-detection.md) <br>
- [Template Derivation](references/template-derivation.md) <br>
- [Completeness Checklist](references/completeness-checklist.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/leonardo-lb/doc-system-generator) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown documentation files with analysis summaries, self-check reports, and shell command snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update repository documentation, entry files, and a copied md-sections.sh helper script.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
