## Description: <br>
Agent-native double-entry business ledger for any entity type, supporting transaction recording, auditing, reporting, and data integrity validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[taylorhou](https://clawhub.ai/user/taylorhou) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and operators use this skill to set up an entity ledger, record double-entry transactions, query financial reports, audit hash-chain integrity, and adapt the protocol for vertical business workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The quickstart asks users to run validation code from an external GitHub repository that may be unpinned. <br>
Mitigation: Inspect or pin the repository before running node validate.js. <br>
Risk: Ledger files may contain private business, entity, or financial data, and proposed entries may be incorrect if accepted without review. <br>
Mitigation: Keep ledgers private, review proposed journal entries before accepting them, and back up or version-control the repository. <br>


## Reference(s): <br>
- [biz-in-a-box Protocol Spec](references/spec.md) <br>
- [Default Chart of Accounts](references/accounts.md) <br>
- [Verticals](references/verticals.md) <br>
- [biz-in-a-box Website](https://biz-in-a-box.org) <br>
- [biz-in-a-box GitHub Repository](https://github.com/taylorhou/biz-in-a-box) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON, YAML, and bash snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose ledger files, journal entries, validation commands, and report queries for user review.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
