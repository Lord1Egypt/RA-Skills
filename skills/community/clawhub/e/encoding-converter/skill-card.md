## Description: <br>
Converts and verifies data across Base64, URL encoding, HEX, HTML entities, hashes, JWT payloads, and binary, octal, decimal, and hexadecimal formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaiyuelv](https://clawhub.ai/user/kaiyuelv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill for local debugging, data inspection, and format conversion tasks such as encoding or decoding text, calculating hashes, viewing JWT header and payload contents, and converting numeric bases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: JWT decode output may be mistaken for a verified authentication or authorization result. <br>
Mitigation: Use the decoded JWT only for inspection unless the token signature, algorithm, issuer, audience, and expiration are separately verified. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kaiyuelv/encoding-converter) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, guidance] <br>
**Output Format:** [Plain text values, Python strings and dictionaries, and Markdown with Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local conversion and decoding output; JWT decoding does not verify signatures.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
