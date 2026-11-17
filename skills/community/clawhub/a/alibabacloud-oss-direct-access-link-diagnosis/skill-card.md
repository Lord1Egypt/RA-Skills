## Description:

Diagnoses Alibaba Cloud OSS direct-access link failures involving downloads, preview, 403 errors, custom domains, and referer rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OSS administrators use this skill to investigate why direct object links download instead of previewing, return 403, fail through a custom domain, or are blocked by referer rules, then review suggested fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Suggested ACL remediation commands can change object access despite the skill's read-only description; recursive changes can expose private objects.

Mitigation: Treat any ossutil set-acl command, especially one using -r, as a separate manual change requiring independent review, exact object-level scope, and explicit confirmation.

Risk: Automatic bucket enumeration can disclose account bucket names without explicit opt-in.

Mitigation: Supply the exact bucket name rather than relying on auto-enumeration, and grant diagnostic credentials only narrowly scoped read-only RAM permissions.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/sdk-team/skills/alibabacloud-oss-direct-access-link-diagnosis)
- [Preview and download playbook](artifact/references/preview-download-playbook.md)
- [403 error diagnosis](artifact/references/ec-0003-00000005-bisection.md)
- [Custom domain binding guide](artifact/references/domain-binding-guide.md)
- [Referer rules](artifact/references/referer-rules.md)
- [Read-only RAM policies](artifact/references/ram-policies.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Configuration templates, Shell commands]

**Output Format:** [Markdown guidance based on a structured diagnostic report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports findings, limitations, next actions, and manual configuration guidance.]

## Skill Version(s):

0.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
