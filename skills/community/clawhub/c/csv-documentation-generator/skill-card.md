## Description: <br>
Use when generating computer system validation (CSV) documentation for pharmaceutical and medical device industries, including validation plans, URS, FS, IQ/OQ/PQ documents, and traceability matrices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zealot00](https://clawhub.ai/user/zealot00) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate bilingual CSV validation documentation for GMP-regulated pharmaceutical and medical device systems. It supports validation plans, URS, FS, IQ/OQ/PQ protocols, risk assessments, traceability matrices, and related Word or Excel outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run Python setup, scan project source files, and write generated requirements, audit, template, Word, or Excel files. <br>
Mitigation: Run it in a dedicated project directory and review generated or modified files before relying on them or committing changes. <br>
Risk: Optional Git hooks or cross-skill system-prompt rules may persist behavior beyond a single generation task. <br>
Mitigation: Avoid global hook installation and add cross-skill agent rules only when that persistent behavior is explicitly intended. <br>


## Reference(s): <br>
- [Project homepage](https://github.com/zealot00/csv-documentation-generator) <br>
- [GAMP 5 reference](references/gamp-5.md) <br>
- [21 CFR Part 11 reference](references/21cfr-part11.md) <br>
- [EU Annex 11 reference](references/annex-11.md) <br>
- [Data integrity reference](references/data-integrity.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands and generated Word or Excel document files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on the requested document type, project name, system name, GAMP category, language, and output directory.] <br>

## Skill Version(s): <br>
1.6.4 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
