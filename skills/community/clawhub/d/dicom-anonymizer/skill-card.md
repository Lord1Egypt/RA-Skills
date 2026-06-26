## Description: <br>
Batch anonymizes DICOM medical images by removing or replacing patient sensitive metadata while preserving image data for research use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and clinical data teams use this skill to process DICOM files or folders, generate anonymized output files, and produce audit logs before research sharing. Outputs still require independent de-identification review before use with medical data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles medical imaging data and scanner evidence warns that anonymized output should not be treated as HIPAA-compliant without further review. <br>
Mitigation: Run the tool only on copies of source images and require independent de-identification review for burned-in text, dates, private tags, and residual PHI before sharing outputs. <br>
Risk: Audit logs and preserved study linkage can retain sensitive patient or linkage information. <br>
Mitigation: Keep audit logs private, restrict access to generated outputs, and disable study-linkage preservation unless it is required for the approved research workflow. <br>
Risk: The release depends on pydicom for local DICOM parsing and writing. <br>
Mitigation: Install in an isolated environment and pin pydicom to a patched version before processing medical files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AIPOCH-AI/dicom-anonymizer) <br>
- [PHI tag reference](references/phi_tags.json) <br>
- [Python dependencies](references/requirements.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local anonymized DICOM files and optional JSON audit logs when the included Python script is run.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
