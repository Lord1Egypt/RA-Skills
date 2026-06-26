## Description: <br>
Deploys a medical image segmentation API using TotalSegmentator and MONAI for DICOM upload, CT/MRI segmentation, batch processing, 3D export, and statistics generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sunshine-del-ux](https://clawhub.ai/user/Sunshine-del-ux) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and medical-imaging engineers use this skill to start and operate an API for DICOM segmentation workflows backed by TotalSegmentator and MONAI. It supports upload, task-status, result, health-check, batch-processing, 3D export, and statistics workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package is incomplete and may require files such as api_server.py and requirements.txt that are not present in the artifact. <br>
Mitigation: Review the actual server code and dependency file before running the skill. <br>
Risk: DICOM uploads may contain sensitive medical data. <br>
Mitigation: Test with de-identified sample data and do not use real patient data without authentication, TLS, firewall controls, pinned dependencies, and an output cleanup policy. <br>
Risk: The quick-start script defaults to binding the API server to 0.0.0.0. <br>
Mitigation: Bind to localhost unless intentionally deploying the service behind appropriate network controls. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Sunshine-del-ux/dicom-segmentation-api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and API endpoint guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide an agent to start a FastAPI service, install dependencies from requirements.txt, and configure host and port values.] <br>

## Skill Version(s): <br>
1.0.0 (source: artifact metadata and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
