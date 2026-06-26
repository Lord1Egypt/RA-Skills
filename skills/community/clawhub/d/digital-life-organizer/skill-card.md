## Description: <br>
Create a privacy-first digital life inventory and cleanup plan from user-supplied information only. This skill does not scan devices, cloud accounts, passwords, or files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to create a privacy-first plan for organizing files, subscriptions, accounts, backups, and recurring digital maintenance from information they choose to provide. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may paste sensitive credentials or private records while building a digital inventory. <br>
Mitigation: Do not request passwords, recovery codes, API keys, cookies, private keys, private documents, or full financial records; work from rough user-supplied descriptions only. <br>
Risk: Cleanup, cancellation, deletion, or account-change guidance could cause data loss or service disruption if followed without preparation. <br>
Mitigation: Recommend reversible steps first, require backups before deletion, and direct users to perform cancellations or account changes themselves on official provider sites. <br>
Risk: Users could mistake checklist language for a security audit or guarantee. <br>
Mitigation: Frame account security output as hygiene guidance and checklists, not audit results or guarantees; recommend reputable password managers and official provider settings pages. <br>


## Reference(s): <br>
- [Safety Boundaries](references/safety-boundaries.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/digital-life-organizer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown plan with checklist sections and an inventory table] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses user-supplied information only; does not execute commands, scan accounts, access files, or make account changes.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter states v1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
