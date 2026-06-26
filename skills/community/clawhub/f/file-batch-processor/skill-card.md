## Description: <br>
Processes local files in batches by renaming files, compressing images, converting images or text files to PDF, and organizing files by type. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lx19840614](https://clawhub.ai/user/lx19840614) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users such as professionals, students, and shop owners use this skill to run local batch file cleanup, image compression, PDF conversion, and file organization workflows on selected folders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local batch operations can rename, move, create, and overwrite many files in a selected folder. <br>
Mitigation: Use --dry-run first, test on a copied folder, and back up important files before processing. <br>
Risk: Bundled promotion material incentivizes positive 5-star reviews, which can reduce the reliability of public review signals. <br>
Mitigation: Treat public reviews cautiously and evaluate the skill through direct testing and scan results. <br>


## Reference(s): <br>
- [File Renaming Patterns Guide](artifact/references/naming_patterns.md) <br>
- [Image Compression Technical Guide](artifact/references/compression_guide.md) <br>
- [File Type Identification Rules](artifact/references/file_types.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Files] <br>
**Output Format:** [Markdown with inline shell commands and local file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs local Python scripts; dry-run mode is available for preview.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact documentation lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
