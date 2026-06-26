## Description: <br>
Guides developers through elephant-guide backend file upload, download, display, module definition, cache handling, and formal FileMedia persistence workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gerald-luo](https://clawhub.ai/user/gerald-luo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when adding image or attachment workflows to elephant-guide backend modules, including temporary uploads, display/download endpoints, FileMediaModule values, and conversion of cached files into formal FileMedia records. It is explicitly scoped away from the older AtroSnow project that uses .c suffix interfaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The final saveFileMediaFile workflow may be inappropriate for normal business-module persistence and could bypass expected service-layer checks if copied without review. <br>
Mitigation: Prefer the documented service-layer createFileMedia pattern, and verify authorization, input validation, audit logging, and file lifecycle handling in the target application. <br>
Risk: The artifact contains one confirmed inconsistency in file-finalization guidance, which could confuse implementation choices. <br>
Mitigation: Treat the service-layer createFileMedia guidance as the safer default and review file-save flows against the actual elephant-guide code before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gerald-luo/atrosnow-file-management) <br>
- [Publisher profile](https://clawhub.ai/user/gerald-luo) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, API Calls, Configuration instructions] <br>
**Output Format:** [Markdown with Java, JavaScript, Vue, JSON, and HTTP examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides endpoint paths, request parameters, response examples, service-layer persistence patterns, enum values, troubleshooting notes, and a development checklist.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
