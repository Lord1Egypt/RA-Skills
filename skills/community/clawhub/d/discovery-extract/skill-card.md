## Description: <br>
Cross-domain scientific discovery through structured extraction of scientific publications; the skill extracts provides/requires relationships to surface hidden connections between fields. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pcdeni](https://clawhub.ai/user/pcdeni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and research analysts use this skill to discover scientific papers, extract structured facts and cross-domain provides/requires relationships, validate the resulting JSON, and save or submit extraction batches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches public paper metadata from research APIs. <br>
Mitigation: Install and run it only when outbound public research metadata queries are acceptable for the environment. <br>
Risk: The optional submission workflow can publish saved extraction JSON and metadata through the user's GitHub account. <br>
Mitigation: Review batch files and GitHub CLI commands before running submission steps. <br>


## Reference(s): <br>
- [Discovery Engine repository](https://github.com/pcdeni/discovery-engine) <br>
- [ClawHub skill page](https://clawhub.ai/pcdeni/discovery-extract) <br>
- [Extraction prompt](references/prompt.txt) <br>
- [Extraction schema](references/schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON extraction files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves extraction JSON locally and can optionally guide GitHub pull request submission.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata; artifact frontmatter and clawhub.json list 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
