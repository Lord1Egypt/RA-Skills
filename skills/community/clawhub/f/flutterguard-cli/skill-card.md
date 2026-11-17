## Description:

Review Flutter Android APK/AAB release artifacts for manifest, permission, cleartext traffic, exported component, embedded secret, signing, size, WebView, deep link, and third-party service risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anasfik](https://clawhub.ai/user/anasfik)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to review Flutter Android APK or AAB release artifacts before shipping. It guides an agent through read-only artifact inspection, evidence collection, risk scoring, and human-approved remediation recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional Google Play APK retrieval can involve account email and AAS token handling.

Mitigation: Prefer a local APK or AAB. If Google Play access is necessary, use the least-privilege option available and revoke or rotate the token after use.

Risk: Artifact inspection depends on local tools and observable APK or AAB evidence, so decompiled or string-based findings can be incomplete.

Mitigation: Treat results as review evidence and confirm sensitive findings before changing permissions, signing, authentication, payments, privacy behavior, or production configuration.

## Reference(s):

- [apkeep](https://github.com/EFForg/apkeep)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with evidence summaries and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Secrets should be redacted; read-only inspection and preservation of the original APK or AAB are preferred.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
