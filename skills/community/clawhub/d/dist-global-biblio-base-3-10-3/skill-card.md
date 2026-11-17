## Description:

Helps users search Chinese and international scholarly literature, review bibliographic details, and access available Chinese-journal and open-access PDFs through SmartLib services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j-levee](https://clawhub.ai/user/j-levee)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, and other literature-search users can find papers and supporting references, inspect article details, and retrieve available full texts. Use requires an email account and may consume search or download quotas.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package exposes a shared gateway secret.

Mitigation: Review the package before installation and use it only if you trust its publisher.

Risk: Email addresses, searches, downloads, quota actions, and payment-status checks are sent to SmartLib-related services.

Mitigation: Confirm you are comfortable sharing this activity with those services before registering or searching.

Risk: Automatic quota use and paid upgrade flows can incur charges; foreign PDFs may come from third-party sources.

Mitigation: Review quota and payment prompts before proceeding, and verify the source and access rights of downloaded PDFs.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/j-levee/skills/dist-global-biblio-base-3-10-3)
- [SmartLib service](https://www.vipslib.com/)
- [Account and quota guidance](references/account.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, PDF download links, Guidance]

**Output Format:** [Markdown search results with citations, article details, availability links, and quota status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese and English literature results; full-text access depends on availability and quota.]

## Skill Version(s):

1.0.0 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
