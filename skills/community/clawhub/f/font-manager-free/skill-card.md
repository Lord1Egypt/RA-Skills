## Description: <br>
Font Manager Free helps agents review web typography for font selection, safe pairing, cross-platform font weights, line height, line width, uppercase spacing, orphan and widow handling, and font-loading performance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and performance engineers use this skill to inspect and improve web typography choices, CSS font usage, readability settings, and font-loading practices. It is intended for font and typography analysis rather than unrelated project-management workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan verdict is suspicious because the skill includes unrelated project-management routing language while requesting command and write capabilities. <br>
Mitigation: Review before installing, constrain activation to typography and font-analysis work, and do not allow the unrelated project-management wording to broaden when the skill should run. <br>
Risk: The artifact advertises command-line features that depend on a required font-manager.py script, but only SKILL.md is present. <br>
Mitigation: Verify whether the missing script is intentionally omitted or required before relying on the advertised analyze, check-pairing, suggest, perf-check, or perf-optimize commands. <br>


## Reference(s): <br>
- [Artifact Skill Definition](artifact/SKILL.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/thcjp/skills/font-manager-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CSS snippets, shell command examples, and optional JSON-style result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May request local read, exec, and write capabilities; advertised command-line features refer to a font-manager.py script that is not present in the artifact.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
