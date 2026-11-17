## Description:

Normalizes informal Chinese defect descriptions into reproducible ZenTao bug records and can log in to ZenTao to submit each issue with required fields, attachments, and submission results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elsemk](https://clawhub.ai/user/elsemk)

### License/Terms of Use:

MIT-0

## Use Case:

QA testers, product reviewers, and development teams use this skill to turn meeting notes, screenshots, or informal defect reports into consistent ZenTao bug entries. In controlled ZenTao workflows, it can submit those entries when credentials, product IDs, and supporting evidence are provided.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill defaults to live ZenTao ticket submission.

Mitigation: Use dry-run or explicit confirmation before live submission in a controlled ZenTao workflow.

Risk: Credentials and saved token state can expose ZenTao access.

Mitigation: Provide credentials through a secure secret mechanism, avoid CLI credential exposure where possible, and protect or delete the saved token state file.

Risk: Local attachment handling can upload unintended evidence files.

Mitigation: Restrict attachment paths to user-selected screenshots, recordings, or other approved evidence files.

Risk: Submitting to an untrusted or misconfigured ZenTao target can expose data or create records in the wrong system.

Mitigation: Set ZENTAO_URL explicitly, trust the target URL before use, and keep SSL verification enabled.

## Reference(s):

- [templates-zh.md](references/templates-zh.md)
- [submit-bugs-input.example.json](references/submit-bugs-input.example.json)
- [module-map.example.json](references/module-map.example.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [ZenTao field-structured Markdown plus JSON input/result files and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PRD and UI evidence before formal bug output; live submission depends on ZenTao credentials, product/module configuration, optional attachments, dedupe, and retry settings.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
