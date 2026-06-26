## Description: <br>
Audits STL, OBJ, and 3MF model files for file integrity, metadata completeness, print-size fit, copyright indicators, and sensitive-content risk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kuihuar](https://clawhub.ai/user/kuihuar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, makers, and reviewers use this skill to assess 3D model files before printing, sharing, or reuse. It guides checks for model validity, required metadata, dimensional fit, copyright/IP signals, and politically sensitive or inappropriate content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated checks are narrower than the broad 3D audit workflow and may miss geometry, metadata, copyright, or sensitive-content issues. <br>
Mitigation: Treat results as advisory and independently verify 3MF geometry, metadata completeness, and legal or content decisions before important use. <br>
Risk: The artifact includes a publish script that can publish the skill package if run intentionally. <br>
Mitigation: Do not run publish.sh unless you intend to publish this skill package from the current environment. <br>


## Reference(s): <br>
- [Copyright Guidelines](references/copyright-guidelines.md) <br>
- [Printer Specifications](references/printer-specs.md) <br>
- [Sensitive Content Guidance](references/sensitive-content.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Code] <br>
**Output Format:** [Markdown audit guidance with inline shell commands and optional JSON outputs from local validation scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces advisory review results; important geometry, legal, and content decisions require independent verification.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
