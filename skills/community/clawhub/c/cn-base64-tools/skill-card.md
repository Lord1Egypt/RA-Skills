## Description: <br>
Provides a local Python helper for Base64 text encoding and decoding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to transform short text strings to and from Base64 locally through a Python standard-library script. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive text may be transformed into Base64, which is encoding rather than protection. <br>
Mitigation: Do not pass secrets unless the transformation is intentional, and treat encoded output as sensitive when the source text is sensitive. <br>
Risk: The documentation claims URL-safe and file conversion support that the included script does not implement. <br>
Mitigation: Use the skill for basic local text encode/decode workflows unless the artifact is updated and retested. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freedompixels/cn-base64-tools) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands] <br>
**Output Format:** [JSON for script results; Markdown or inline shell commands for agent guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local Python standard-library execution; basic encode/decode behavior only.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
