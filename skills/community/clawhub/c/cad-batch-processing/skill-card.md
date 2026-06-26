## Description: <br>
Provides CAD batch-processing assistance for reading DXF drawing data, replacing text, renaming layers, modifying block attributes, generating simple DXF drawings, backing up project files, renaming CAD files, and watermarking PDFs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[137984917-cyber](https://clawhub.ai/user/137984917-cyber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Interior design practitioners and CAD automation users can use this skill to inspect drawing contents, batch-update project names or title-block data, normalize layer attributes, generate basic floor-plan DXF files, and prepare project backups or PDF deliverables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Batch text replacement, layer changes, attribute edits, renaming, and PDF watermarking can modify project files in place. <br>
Mitigation: Work on copies or backups first and test commands on a small folder before running against a full CAD project. <br>
Risk: Extracted JSON may include text, coordinates, layer names, and block attributes from confidential drawings. <br>
Mitigation: Use explicit output files and handle extracted JSON under the same access controls as the source CAD files. <br>
Risk: PDF export depends on local CAD command-line tooling and may require environment-specific configuration. <br>
Mitigation: Confirm the local CAD export command and review generated PDFs before sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/137984917-cyber/cad-batch-processing) <br>
- [Publisher profile](https://clawhub.ai/user/137984917-cyber) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON, Files, Guidance] <br>
**Output Format:** [Markdown guidance with Python examples, shell commands, JSON extraction output, and generated or modified CAD/PDF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local Python scripts operate on user-supplied DXF, DWG, PDF, and folder paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
