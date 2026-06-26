## Description: <br>
Generates and verifies Architectural Decision Record Markdown using the MADR template and E.C.A.D.R. Definition of Done criteria. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to draft, format, and check ADRs from known decisions, including context exploration, numbering, MADR sections, and completeness gaps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated ADRs may contain incomplete assumptions or unresolved investigation gaps. <br>
Mitigation: Review the ADR, resolve any [INVESTIGATE] markers, and verify local file diffs before committing or sharing. <br>
Risk: The skill may inspect local project context and create ADR files under docs/adrs/. <br>
Mitigation: Use it only in repositories where ADR creation is intended and review any created or changed files. <br>


## Reference(s): <br>
- [MADR Template](references/madr-template.md) <br>
- [Definition of Done: E.C.A.D.R. Criteria](references/definition-of-done.md) <br>
- [Markdown Any Decision Records](https://adr.github.io/madr/) <br>
- [ClawHub Skill Page](https://clawhub.ai/anderskev/adr-writing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown ADR files with YAML frontmatter, optional investigation markers, and brief shell command guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates docs/adrs/NNNN-slugified-title.md when used to write an ADR; the numbering helper can allocate one or more ADR numbers.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
