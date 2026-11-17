## Description:

Generate complete incorporation documents for a new business entity from a simple configuration, including formation filings, governance documents, ledgers, checklists, 83(b) election materials, and restricted stock purchase agreements for supported C-Corp and LLC paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juankisugar-creator](https://clawhub.ai/user/juankisugar-creator)

### License/Terms of Use:


## Use Case:

External founders, operators, and their agents use this skill to draft business formation document packages and filing checklists from structured company information. It is best suited for straightforward Nevada or Delaware C-Corp and LLC formations that will still receive legal and tax review before filing or signing.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The skill can produce high-impact legal and tax documents that may exceed its supported scope.

Mitigation: Limit use to the supported Nevada or Delaware C-Corp and LLC paths and obtain qualified legal or tax review for S-Corp treatment, other states, complex ownership, securities, tax, or investor arrangements.

Risk: Generated packages can contain sensitive formation records, ownership details, tax information, addresses, and signatures.

Mitigation: Handle outputs as sensitive records and avoid cloud upload unless access controls and sharing permissions are deliberately configured.

Risk: Filing deadlines and tax elections can create irreversible consequences if missed or completed incorrectly.

Mitigation: Review the generated checklist immediately, track time-sensitive items such as 83(b) elections, and confirm deadlines against official sources or advisors before acting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/juankisugar-creator/skills/ai-powered-business-formation-playbook)
- [Configuration template](references/config-template.md)
- [Nevada C-Corp reference](references/nevada-corp.md)
- [Delaware C-Corp reference](references/delaware-corp.md)
- [Nevada LLC reference](references/nevada-llc.md)
- [Delaware LLC reference](references/delaware-llc.md)
- [Post-filing learnings](references/post-filing-learnings.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and generated .docx formation document files from JSON or YAML configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sensitive legal, tax, ownership, and address information; outputs require careful review before filing, signing, or cloud sharing.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
