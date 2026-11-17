## Description:

Automates client reporting for agencies and freelancers by pulling analytics, search, social, and custom metrics, generating branded reports, and delivering them by email or Slack.

This skill is ready for commercial/non-commercial use.

## Publisher:

[reighlan](https://clawhub.ai/user/reighlan)

### License/Terms of Use:


## Use Case:

Agencies, freelancers, and external client-facing teams use this skill to set up reporting workspaces, collect marketing metrics, generate branded recurring reports, and deliver them to clients.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive client reports, credentials, and local paths may be stored in configuration, cache, and report files.

Mitigation: Use a trusted local workspace, keep configuration and report files under restrictive permissions, and prefer environment variables or a secret manager for API keys.

Risk: Email or Slack delivery can send client data to unintended outbound destinations.

Mitigation: Verify every recipient email address and Slack webhook before delivery, and avoid running delivery against untrusted client configurations.

Risk: Client names, domains, webhook URLs, and local paths are not described as fully validated by the release evidence.

Mitigation: Use safe client slugs, review domains and paths before execution, and add path validation, webhook allowlisting, and domain validation before broader deployment.

## Reference(s):

- [Google Analytics 4 API Setup](references/ga4-setup.md)
- [Report Customization](references/report-customization.md)
- [Google Cloud API Library](https://console.cloud.google.com/apis/library)
- [ClawHub Skill Page](https://clawhub.ai/reighlan/skills/client-reporting)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples; generated reports may be Markdown, HTML, or PDF, with metrics stored as JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local client workspaces, config files, cached metrics, templates, and report files when its scripts are run.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
