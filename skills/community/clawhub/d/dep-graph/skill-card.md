## Description: <br>
Dep Graph analyzes and visualizes dependency trees from manifest files for Node.js, Python, Go, Rust, Ruby, and PHP projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johnnywang2001](https://clawhub.ai/user/johnnywang2001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect project manifests, list dependencies, compare production and development groups, and generate tree, JSON, or summary views for dependency review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review did not include a full artifact content review. <br>
Mitigation: Read the skill text, expected files, and permissions before enabling the skill; avoid granting sensitive credentials or broad filesystem access unless the need is clearly explained. <br>
Risk: The skill reads dependency manifests from the selected project directory and may surface dependency names or version constraints in agent output. <br>
Mitigation: Run it only against intended project directories and review generated dependency output before sharing it outside the workspace. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/johnnywang2001/dep-graph) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and optional JSON dependency summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs dependency groups with version constraints or counts; requires only the Python standard library.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
