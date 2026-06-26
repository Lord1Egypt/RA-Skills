## Description: <br>
Create secure shareable self-destructing notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[easyFloyd](https://clawhub.ai/user/easyFloyd) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to turn sensitive text into an encrypted, one-time-read note and return a shareable URL from a configured FadNote endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Encrypted note ciphertext is uploaded to the configured FADNOTE_URL endpoint. <br>
Mitigation: Use a trusted or self-hosted endpoint for highly sensitive content and review the configured endpoint before creating a note. <br>
Risk: The generated URL contains the decryption key and can reveal the note to whoever opens it first before expiry. <br>
Mitigation: Share the full URL only through trusted channels, avoid logging it, and choose an appropriate TTL for the sensitivity of the content. <br>


## Reference(s): <br>
- [ClawHub FadNote page](https://clawhub.ai/easyFloyd/fadnote) <br>
- [FadNote source repository](https://github.com/easyFloyd/fadnote) <br>
- [FadNote live service](https://fadnote.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text shareable URL by default, or JSON containing noteId, expiresIn, and decryptionUrl when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and a configured or trusted FADNOTE_URL; accepts direct text or stdin with an optional TTL.] <br>

## Skill Version(s): <br>
1.0.2 (source: SKILL.md frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
