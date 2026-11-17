## Description:

End-to-end release workflows for TestFlight and App Store using asc publish, builds, versions, and submit commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rudrankriyam](https://clawhub.ai/user/rudrankriyam)

### License/Terms of Use:


## Use Case:

Developers and release engineers use this skill to guide TestFlight distribution and App Store submission workflows with asc CLI commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide commands that distribute TestFlight builds or submit real App Store releases when the user directs execution.

Mitigation: Review the app ID, IPA path, TestFlight group, version, build, and any --confirm or --notify flags before running generated commands.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes command templates for TestFlight distribution, App Store submission, build lookup, submission status, and cancellation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
