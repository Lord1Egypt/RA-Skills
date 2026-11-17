## Description:

Admin skill to sign into Cosmonyx, fetch companies, filter/export records as PDF or Excel, optionally email the export, or send reminder emails to filtered companies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[waqas-orcalo](https://clawhub.ai/user/waqas-orcalo)

### License/Terms of Use:

MIT

## Use Case:

Administrators use this skill to authenticate to Cosmonyx, retrieve company records, filter by compliance, risk, KYC, or expiry criteria, and export or email the selected records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented email workflow can expose sensitive company data or turn recipient and file path text into shell execution.

Mitigation: Install only in a controlled admin environment; use structured execution, validate recipients and attachment paths, and require explicit confirmation before exporting or emailing data.

Risk: SMTP authentication may use credentials while sending exports or reminder emails.

Mitigation: Store SMTP credentials carefully and require encrypted SMTP transport before authentication.

## Reference(s):

- [Comonyx Admin ClawHub Page](https://clawhub.ai/waqas-orcalo/skills/comonyx-admin)
- [Cosmonyx Admin Sign-In Endpoint](https://gateway-dev.cosmonyx.co/auth/signin)
- [Cosmonyx Companies Endpoint](https://gateway-dev.cosmonyx.co/companies)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands, Configuration guidance]

**Output Format:** [Markdown responses with generated PDF or Excel files and shell commands for optional email delivery]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Handles admin credentials, company records, SMTP settings, recipient addresses, and optional export attachments.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
