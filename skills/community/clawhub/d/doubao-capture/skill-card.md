## Description: <br>
Capture Doubao translation results with auto-scroll and auto-end detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[banner90](https://clawhub.ai/user/banner90) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and workflow agents use this skill to capture translated subtitles from a visible Doubao translation window as part of a YouTube translation workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The plugin entry points to an absolute Python file outside the reviewed package. <br>
Mitigation: Review before installing, verify the referenced capture script, or ask the publisher to include the script in the package and use a package-relative entry path. <br>
Risk: Windows GUI automation depends on the correct Doubao window handle and a visible desktop session. <br>
Mitigation: Run only with a verified Doubao translation window handle, an expected output directory, and an active Windows desktop session. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/banner90/doubao-capture) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns success or error JSON and writes captured subtitle text files to the configured Windows output directory.] <br>

## Skill Version(s): <br>
1.0.6 (source: ClawHub release metadata; artifact package.json declares 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
