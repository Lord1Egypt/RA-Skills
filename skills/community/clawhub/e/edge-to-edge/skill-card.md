## Description: <br>
Use this skill to migrate your Jetpack Compose app to add adaptive edge-to-edge support and troubleshoot common issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ntriq-gh](https://clawhub.ai/user/ntriq-gh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Android developers and engineers use this skill to update Jetpack Compose apps for SDK 35 edge-to-edge behavior, apply safe system and IME insets, and troubleshoot overlapping UI around status and navigation bars. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Applying the skill may lead an agent to change Android Activity code, SDK targets, and AndroidManifest settings, which can introduce build or UI regressions. <br>
Mitigation: Apply changes on a branch, review source and manifest diffs carefully, and run the Android build and tests afterward. <br>
Risk: Incorrect inset handling can cause double padding, obscured input fields, or system bar legibility issues in Jetpack Compose screens. <br>
Mitigation: Follow one inset strategy per component, check IME behavior on affected screens, and manually verify status and navigation bar layouts. <br>
Risk: The artifact metadata names Google LLC as author, but server-resolved provenance is unavailable. <br>
Mitigation: Do not treat the metadata author claim as independently verified provenance; rely on the server-resolved publisher handle for ownership. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ntriq-gh/edge-to-edge) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/ntriq-gh) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown guidance with Kotlin and AndroidManifest XML code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces implementation guidance for Android Jetpack Compose projects; users should review proposed source and manifest changes before applying them.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
