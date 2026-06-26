## Description: <br>
Encode or decode text using Base64, URL percent-encoding, or HTML entities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ohernandez-dev-blossom](https://clawhub.ai/user/ohernandez-dev-blossom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and other users can use this skill to transform provided text between readable text and Base64, URL percent-encoding, or HTML entity encodings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may mistake Base64, URL encoding, or HTML entity encoding for encryption. <br>
Mitigation: Explain that these encodings are reversible formatting methods and avoid processing secrets unless the user accepts that the text may remain in chat context. <br>
Risk: Plain text handling is unsuitable for binary or non-text files. <br>
Mitigation: For binary data, advise using a tool that accepts raw bytes or file uploads instead of pasted text. <br>


## Reference(s): <br>
- [Base64 Encode on ClawHub](https://clawhub.ai/ohernandez-dev-blossom/base64-encode) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Plain text string with a brief note] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Transforms user-provided text; empty input returns an empty string with a note.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
