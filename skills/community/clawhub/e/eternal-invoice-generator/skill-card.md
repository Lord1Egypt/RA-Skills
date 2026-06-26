## Description: <br>
Generates professional PDF invoices and payment reminders from command-line inputs with itemized totals, tax, discounts, currency selection, and payment details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eternal0404](https://clawhub.ai/user/eternal0404) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, freelancers, and small-business operators use this skill to create local PDF invoices and payment reminders from structured line items, client details, payment terms, and optional bank details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Invoices and reminders may contain client, address, payment, or bank information. <br>
Mitigation: Store generated PDFs securely and avoid adding unnecessary sensitive details. <br>
Risk: The skill retains local invoice-number state in ~/.invoices/counter.json. <br>
Mitigation: Delete ~/.invoices/counter.json if local numbering state should not be retained. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/eternal0404/eternal-invoice-generator) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [PDF files with command-line status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes PDFs to the requested output path or current directory and stores invoice-number state in ~/.invoices/counter.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
