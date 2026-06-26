## Description: <br>
Organize, summarize, and index technical documentation from any source into structured, source-linked documentation notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brauliodiasribeiro](https://clawhub.ai/user/brauliodiasribeiro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical writers, and teams use this skill to turn raw documentation from repositories, websites, manuals, or mixed sources into numbered Markdown topic files with indexes, source links, concise summaries, and setup guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Source documentation may contain private or secret material that could be summarized into generated notes. <br>
Mitigation: Use a specific source and destination folder, and avoid pointing the skill at private or secret-containing documentation unless that material is intended to be summarized. <br>
Risk: Generated documentation can become misleading if summaries or proposed file changes are accepted without review. <br>
Mitigation: Review proposed file changes before applying them, keep original source links in each file, and use living-document markers to support future updates. <br>


## Reference(s): <br>
- [Workflow Patterns](references/workflow-patterns.md) <br>
- [Output Examples](references/output-examples.md) <br>
- [Structure Validator](scripts/validate_structure.py) <br>
- [Doc Setup on ClawHub](https://clawhub.ai/brauliodiasribeiro/doc-setup) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown notes with numbered files, source attribution, tables, checklists, and inline command or configuration blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated notes are intended to preserve source links and living-document markers; optional validation checks numbered Markdown structure and source attribution.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
