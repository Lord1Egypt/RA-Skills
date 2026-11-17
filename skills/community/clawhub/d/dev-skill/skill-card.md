## Description:

Generates SwiftUI iOS application code from PRD documents, including project structure, MVVM components, data management, and build and QA handoff guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tc1993](https://clawhub.ai/user/tc1993)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn PRD markdown into a SwiftUI iOS project with models, view models, views, services, persistence, networking, and build guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated project files are expected to be written into dev-output/ and may conflict with existing workspace contents.

Mitigation: Run the skill in a workspace where dev-output/ is acceptable and check for existing files before generation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tc1993/skills/dev-skill)
- [Publisher Profile](https://clawhub.ai/user/tc1993)

## Skill Output:

**Output Type(s):** [Code, Files, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with generated Swift and Xcode project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a multi-file Xcode project in dev-output/ and hands generated code to qa-skill.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
