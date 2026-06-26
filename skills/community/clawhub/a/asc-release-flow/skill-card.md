## Description: <br>
End-to-end release workflows for TestFlight and App Store using asc publish, builds, versions, and submit commands. Use when asked to upload a build, distribute to TestFlight, or submit to App Store. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rudrankriyam](https://clawhub.ai/user/rudrankriyam) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and release engineers use this skill to plan and run TestFlight and App Store release workflows with asc CLI commands, including upload, distribution, build attachment, submission, status checks, and cancellation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide real TestFlight or App Store release actions when used with Apple developer credentials. <br>
Mitigation: Use trusted asc tooling, least-privilege App Store Connect credentials where possible, and verify the Apple account/team, app ID, IPA path, version, build ID, TestFlight groups, and any --confirm action before running commands. <br>
Risk: Incorrect command flags or identifiers could upload, distribute, submit, cancel, or otherwise change the wrong app release. <br>
Mitigation: Run command-specific --help, review generated commands, and confirm target app and submission identifiers before execution. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that require Apple developer credentials and explicit confirmation before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and user changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
