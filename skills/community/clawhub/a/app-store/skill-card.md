## Description:

Publish and manage iOS and Android apps with account setup, submission workflows, review compliance, and rejection handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and release managers use this skill to prepare iOS and Android app store submissions, manage beta testing tracks, handle review feedback, and plan CI/CD release automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copied release automation commands can publish or alter production mobile apps.

Mitigation: Require manual approval gates for release lanes before using the automation examples.

Risk: App Store Connect and Google Play credentials are sensitive and are referenced in automation workflows.

Mitigation: Store credentials only in protected CI secrets and do not commit certificates, private keys, or service account files.

## Reference(s):

- [CI/CD & Automation](automation.md)
- [Testing & Beta Distribution](testing.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with checklists, tables, and inline code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; no tools or MCP integrations detected.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
