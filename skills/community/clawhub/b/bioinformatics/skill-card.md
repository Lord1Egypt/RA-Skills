## Description: <br>
Analyze DNA, RNA, and protein sequences with alignment, variant calling, and expression analysis pipelines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Researchers, bioinformaticians, and developers use this skill to plan and run local sequence-analysis workflows, including quality control, alignment, file-format conversion, RNA-seq analysis, and variant calling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sequencing data can be sensitive, and the skill may guide local analysis over user-provided biological data. <br>
Mitigation: Keep raw data read-only or backed up, choose secure output paths, and review commands before running them. <br>
Risk: Optional local memory under ~/bioinformatics/ can retain project details and activation preferences. <br>
Mitigation: Enable memory only with user consent and save only project details or preferences the user wants retained locally. <br>
Risk: Bioinformatics pipelines can produce misleading results when inputs, reference genomes, or coordinate conventions are mismatched. <br>
Mitigation: Run input quality checks first, track the reference genome per project, preserve raw files, and log tool versions and command parameters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/bioinformatics) <br>
- [Skill homepage](https://clawic.com/skills/bioinformatics) <br>
- [Setup](setup.md) <br>
- [File Formats](formats.md) <br>
- [Tool Reference](tools.md) <br>
- [RNA-seq Pipeline](rnaseq.md) <br>
- [Variant Calling Pipeline](variants.md) <br>
- [Memory Template](memory-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash, R, and configuration code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local file outputs, pipeline configurations, logs, and memory updates under user-approved paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
