## Description: <br>
Meta-agent that routes bioinformatics requests to specialised sub-skills and handles file type detection, analysis planning, report generation, and reproducibility export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[manuelcorpas](https://clawhub.ai/user/manuelcorpas) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, researchers, and bioinformatics analysts use this skill to route biological analysis requests to specialised skills, plan multi-step workflows, and generate reproducible analysis reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reports and audit logs may contain sensitive genomic, biomedical, file path, command, or project details. <br>
Mitigation: Use a dedicated working directory, keep generated reports and logs private, and avoid sharing outputs from sensitive projects without review. <br>
Risk: Routed multi-step analyses may depend on other skills or networked tools that change privacy and execution risk. <br>
Mitigation: Review the proposed analysis plan before approval, confirm any networked analysis explicitly, and do not upload genomic data to external services without user confirmation. <br>


## Reference(s): <br>
- [ClawBio project homepage](https://github.com/manuelcorpas/ClawBio) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, reproducibility commands, checksums, audit log entries, and optional JSON routing output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include file paths, command logs, checksums, and project details from local bioinformatics work.] <br>

## Skill Version(s): <br>
0.1.0 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
