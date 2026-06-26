## Description: <br>
Use this skill when a digital-forensic examiner, DFIR responder, or e-discovery custodian needs to draft a court-admissible chain-of-custody record aligned to NIST SP 800-86 and ISO/IEC 27037. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archlab-space](https://clawhub.ai/user/archlab-space) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Digital forensic examiners, DFIR responders, e-discovery custodians, investigators, and counsel use this skill to collect case facts and draft a review-only chain-of-custody package for digital evidence. It structures evidence-item records, acquisition details, transfer logs, working-copy handling, integrity checks, and unresolved questions for examiner and counsel review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A bundled review helper may run nested Codex review with full sandbox bypass. <br>
Mitigation: Install only after reviewing the maintainer workflow and privilege level; use --no-yolo or AUTOREVIEW_YOLO=0 for safer autoreview operation. <br>
Risk: Moderation or publishing workflows can act with ClawHub or GitHub credentials. <br>
Mitigation: Run those workflows only with intended credentials and explicit targets. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/archlab-space/chain-of-custody-log-drafter) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown draft with structured tables and review notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs remain unsigned drafts and require examiner-of-record and counsel review.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
