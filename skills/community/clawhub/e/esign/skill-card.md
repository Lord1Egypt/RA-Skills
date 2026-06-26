## Description: <br>
Send files for e-signature with Nota Sign, including local files, uploaded attachments, or URLs, with signer collection, credential setup, environment selection, file validation, and Node.js runtime fallback support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[notasign](https://clawhub.ai/user/notasign) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to prepare and send supported documents for electronic signature through Nota Sign. It is intended for workflows that need signer collection, Nota Sign credential configuration, production or UAT environment selection, and command execution guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends selected documents and signer names and emails to Nota Sign. <br>
Mitigation: Confirm the document, signer email addresses, region, and PROD or UAT environment before sending. <br>
Risk: Nota Sign credentials and a Base64 PKCS#8 private key may be stored locally. <br>
Mitigation: Store configuration only in the intended path, avoid echoing secrets, and protect ~/.notasign/config.json with strict file permissions. <br>
Risk: The temporary Node.js fallback can download node@20 and tsx from npm. <br>
Mitigation: Use a trusted local Node.js 18+ runtime in sensitive environments, and allow the npm fallback only when that network dependency is acceptable. <br>


## Reference(s): <br>
- [Nota Sign ClawHub listing](https://clawhub.ai/notasign/esign) <br>
- [Nota Sign publisher profile](https://clawhub.ai/user/notasign) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline JSON and bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return an envelope ID and send summary after execution; may also surface validation or API errors with the next required action.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
