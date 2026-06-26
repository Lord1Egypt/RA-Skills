## Description: <br>
Scan project dependencies for license compatibility issues, GPL contamination, and compliance violations across npm, pip, Go, Rust, and Ruby ecosystems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and compliance reviewers use this skill to audit project dependency licenses, identify policy violations or unknown licenses, generate reports, and add CI license gates before shipping. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads dependency manifests, lockfiles, installed package metadata, and optional license policy files in the project directory being scanned. <br>
Mitigation: Run it only against intended project directories and review results before using them for compliance decisions. <br>
Risk: Some ecosystems may report UNKNOWN license values when local package metadata is unavailable. <br>
Mitigation: Manually verify unknown licenses before approving release or CI enforcement decisions. <br>


## Reference(s): <br>
- [Custom License Policy](references/custom-policy.md) <br>
- [Dependency License Audit on ClawHub](https://clawhub.ai/charlie-morrison/dependency-license-audit) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, code, shell commands, configuration] <br>
**Output Format:** [Text, JSON, or Markdown reports with dependency tables, issue summaries, recommendations, and CI exit codes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can read custom .license-policy.json rules and optionally include npm transitive dependencies.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
