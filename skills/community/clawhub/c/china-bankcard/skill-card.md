## Description: <br>
Parses and validates Chinese bank card numbers offline to identify issuing bank, card type, card organization, card length, and Luhn checksum status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ToBeWin](https://clawhub.ai/user/ToBeWin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze Chinese bank card numbers in chat or validation workflows, including issuer lookup, card network classification, debit or credit identification, length checks, and Luhn validation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bank card numbers are sensitive financial data. <br>
Mitigation: Mask card numbers in responses and do not request or include CVV, PIN, expiry date, passwords, identity documents, or banking login details. <br>
Risk: BIN and Luhn results can be mistaken for proof that a bank account exists. <br>
Mitigation: Present issuer and checksum results as informational only and direct users to official bank channels when account existence or current card status matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ToBeWin/china-bankcard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown text with masked bank card numbers and validation results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fully offline output; masks card numbers by retaining only the first four and last four digits.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
