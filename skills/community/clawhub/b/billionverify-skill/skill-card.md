## Description:

Verify email addresses using the BillionVerify API for single checks, batch lists, bulk file verification, credit balance checks, and webhook management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[billionverifier](https://clawhub.ai/user/billionverifier)

### License/Terms of Use:

MIT

## Use Case:

External developers and teams use this skill to prepare BillionVerify API requests for email verification workflows, including individual addresses, email batches, uploaded files, credit checks, and webhook setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bulk and file verification can send email addresses or spreadsheet contents to BillionVerify.

Mitigation: Confirm authorization for the addresses, remove unrelated spreadsheet data, and avoid uploading data that is not needed for verification.

Risk: Verification requests may consume paid BillionVerify credits.

Mitigation: Check credit balance and review batch or file size before running large verification jobs.

Risk: Webhook setup can expose callback URLs and creation-time secrets.

Mitigation: Use HTTPS webhook URLs you control and store webhook secrets securely when they are returned.

## Reference(s):

- [BillionVerify API Documentation](https://billionverify.com/docs)
- [BillionVerify Website](https://billionverify.com/)
- [ClawHub Skill Page](https://clawhub.ai/billionverifier/skills/billionverify-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include curl commands, API endpoint details, environment-variable setup, request bodies, and result-handling guidance.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
