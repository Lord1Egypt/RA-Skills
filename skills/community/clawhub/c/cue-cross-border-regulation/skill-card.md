## Description:

Helps cross-border legal and compliance teams research foreign regulations and prepare Chinese reports with bilingual key provisions and links to official sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[panting09266-ai](https://clawhub.ai/user/panting09266-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External legal and compliance professionals and cross-border business teams use the skill to find and summarize public regulations, including their scope and exemptions, in major jurisdictions such as the United States, European Union, and Singapore. Its reports are research aids and do not constitute formal legal advice.

### Deployment Geography for Use:

Primarily the United States, European Union, and Singapore; coverage of other jurisdictions is limited.

## Known Risks and Mitigations:

Risk: The skill automatically runs changing external runner code, and the artifact review does not fully cover runner or server-side behavior.

Mitigation: Review and pin the runner to a specific commit, approve updates, and restrict its local access.

Risk: Complete business questions may contain confidential identifiers or transaction details, and report-link access or service retention may affect confidentiality.

Mitigation: Configure credentials privately rather than pasting them into chat, remove confidential details from questions, and check Cue's data-retention and report-link access policies.

## Reference(s):

- [Cue playbook](https://cuecue.cn/playbook)
- [EUR-Lex](https://eur-lex.europa.eu)
- [United States Code](https://uscode.house.gov)
- [Electronic Code of Federal Regulations](https://www.ecfr.gov)
- [Singapore Statutes Online](https://sso.agc.gov.sg)

## Skill Output:

**Output Type(s):** [Analysis, Markdown]

**Output Format:** [Markdown research report, primarily in Chinese, with bilingual key provisions and links to official sources.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Coverage focuses on major English-language jurisdictions; reports are based on public sources and are not formal legal advice.]

## Skill Version(s):

1.0.11 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
