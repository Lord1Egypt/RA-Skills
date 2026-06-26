## Description: <br>
Reviews CloudKit code for container setup, record handling, subscriptions, and sharing patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review Swift CloudKit code for container configuration, record handling, subscriptions, sharing, and release-readiness issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scan summary says the unpacked target artifact was not clearly available for direct review. <br>
Mitigation: Review the installed skill files at install time and confirm that any requested local or account access matches expected behavior. <br>
Risk: CloudKit review findings can be misleading if based on isolated snippets or unverified deployment assumptions. <br>
Mitigation: Apply the skill's hard gates: cite a current file and line, read the full surrounding unit, inspect concrete CloudKit or deployment artifacts when required, and downgrade unsupported claims to review questions. <br>


## Reference(s): <br>
- [CloudKit Container Setup](artifact/references/container-setup.md) <br>
- [CloudKit Records](artifact/references/records.md) <br>
- [CloudKit Subscriptions](artifact/references/subscriptions.md) <br>
- [CloudKit Sharing](artifact/references/sharing.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/anderskev/cloudkit-code-review) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown review findings with file and line references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings are expected to use [FILE:LINE] ISSUE_TITLE and include review questions when evidence is incomplete.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
