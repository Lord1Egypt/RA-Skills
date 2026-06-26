## Description: <br>
115 Publish helps agents manage 115 cloud-drive accounts through QR login, file browsing and search, share transfer, offline downloads, smart organization, and capacity checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sukris](https://clawhub.ai/user/sukris) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to operate a 115 cloud-drive account from chat, including login, browsing, searching, share transfer, offline download tasks, organization, cleanup advice, and capacity checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: QR login creates a reusable local session for a 115 account. <br>
Mitigation: Install only for accounts where local session reuse is acceptable, review cookie retention behavior, and clear stored cookies when access is no longer needed. <br>
Risk: File organization and transfer features can make broad account-side changes. <br>
Mitigation: Test on a small folder first, back up important data, and require explicit preview and confirmation before bulk move, transfer, or delete operations. <br>
Risk: The security guidance calls out a preference for normal TLS verification. <br>
Mitigation: Prefer a version that uses normal TLS verification for all network flows before use on important accounts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sukris/115-skills) <br>
- [Publisher profile](https://clawhub.ai/user/sukris) <br>
- [115 service homepage](https://115.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Plain text or Markdown status messages, file lists, operation summaries, and QR-code image payloads.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return account-side operation results and user prompts for login or confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: evidence.release.version, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
