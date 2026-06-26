## Description: <br>
Generate PPT decks from prompts/block XML while preserving corporate brand style. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phil-osophy-42](https://clawhub.ai/user/phil-osophy-42) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, developers, and presentation authors use this skill to generate PowerPoint decks from structured block XML or prompts while reusing a corporate template style. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Caller-supplied template_file or output_filename values may read templates or write output outside the intended skill folder. <br>
Mitigation: Reject absolute paths and '..' traversal, constrain outputs to a dedicated folder, and avoid unexpected overwrites. <br>
Risk: Untrusted XML or PowerPoint templates may cause unsafe or misleading generated deck content. <br>
Mitigation: Use only trusted XML and trusted PPT templates, and do not let untrusted users or automated prompts choose template or output paths. <br>
Risk: Unpinned runtime dependencies can reduce install reproducibility. <br>
Mitigation: Pin python-pptx and other dependencies to reviewed versions before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/phil-osophy-42/12321321123) <br>


## Skill Output: <br>
**Output Type(s):** [Files, JSON] <br>
**Output Format:** [PowerPoint .pptx file with JSON status] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns output_path, slide_count, fallback_count, and message.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and manifest.yaml; SKILL.md frontmatter reports 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
