## Description: <br>
Chexian Baodan Tong helps insurance agents and insurance-company staff organize car-insurance policy PDFs by extracting policy identifiers, renaming files, and optionally packaging the folder as a ZIP archive. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wwbwin](https://clawhub.ai/user/wwbwin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External insurance agents and insurance-company staff use this skill to process local car-insurance policy PDFs, extract license plate, policyholder, and policy-number fields, rename files for filing, and create an archive package. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill renames PDF files in the selected folder, which can change filenames that users still need in their original form. <br>
Mitigation: Run first with --no-rename --no-pack, or run on a copied folder before processing original policy files. <br>
Risk: ZIP packaging can include unrelated or sensitive files if the selected folder contains more than the intended policy PDFs. <br>
Mitigation: Use a dedicated folder containing only the intended insurance PDFs, or keep --no-pack enabled. <br>
Risk: API mode can send policy document content to the configured external provider. <br>
Mitigation: Avoid --api unless the provider and endpoint are trusted and appropriate for the sensitivity of the policy data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wwbwin/chexian-baodan-tong) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Command-line guidance and local file outputs, including renamed PDF files and an optional ZIP archive.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The script can run locally with pdfminer.six or in API mode using INSURANCE_API_KEY, INSURANCE_API_ENDPOINT, and INSURANCE_API_MODEL.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
