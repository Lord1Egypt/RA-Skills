## Description: <br>
Dev Skill generates SwiftUI iOS application code from PRD documents, including architecture, UI components, data models, and QA handoff. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tc1993](https://clawhub.ai/user/tc1993) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to transform PRD markdown into a SwiftUI iOS app project with MVVM structure, data models, views, services, tests, and build guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates project files under dev-output/. <br>
Mitigation: Review generated files before adding them to a repository or build pipeline. <br>
Risk: Generated code is handed to qa-skill after creation. <br>
Mitigation: Avoid confidential PRDs unless that downstream handoff is acceptable. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Code, Files, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Generated Swift and project files with Markdown build instructions and next steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates project files under dev-output/ and hands generated code to qa-skill.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
