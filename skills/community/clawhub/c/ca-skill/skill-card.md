## Description: <br>
Full-service CA skill for TallyPrime running locally that reads accounting reports and helps post or update vouchers through TallyPrime XML-over-HTTP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[purvik6062](https://clawhub.ai/user/purvik6062) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External accountants, CAs, and developers use this skill to connect an agent to a local TallyPrime instance, inspect accounting reports, manage masters, and prepare or post supervised voucher changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and change local TallyPrime accounting books. <br>
Mitigation: Use only with a trusted localhost Tally server, confirm the exact company and date scope before reads, and require explicit review before any create, alter, or cancel action. <br>
Risk: Incorrect company, ledger, GST, voucher class, or total values could create inaccurate accounting records. <br>
Mitigation: Verify company spelling, required ledgers, GST fields, voucher class settings, balanced totals, and current backups before write operations. <br>


## Reference(s): <br>
- [Reports & Data Export](reference/reports.md) <br>
- [Vouchers](reference/vouchers.md) <br>
- [Masters](reference/masters.md) <br>
- [Inventory](reference/inventory.md) <br>
- [Errors & Troubleshooting](reference/errors.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown guidance with XML and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TALLY_URL for a trusted local TallyPrime server.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
