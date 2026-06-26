## Description: <br>
Track compliance requirements and generate audit trail reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security practitioners, and compliance reviewers use this skill to record timestamped audit notes, policy checks, credential lifecycle events, and export or search local audit trails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-entered compliance notes, credentials, tokens, personal data, or sensitive evidence may be saved in plaintext local files and included in exports. <br>
Mitigation: Do not enter secrets or sensitive compliance evidence unless plaintext local storage under ~/.local/share/compliance is acceptable for the environment. <br>
Risk: Commands such as hash, verify, rotate, store, and retrieve record audit notes but do not perform those security operations. <br>
Mitigation: Use the skill as a local record-keeping aid and rely on separate approved tools for actual credential rotation, hashing, verification, storage, and retrieval. <br>


## Reference(s): <br>
- [Compliance on ClawHub](https://clawhub.ai/bytesagain-lab/compliance) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, Shell commands] <br>
**Output Format:** [Terminal text plus local log and export files in JSON, CSV, or TXT.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local records under ~/.local/share/compliance.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
