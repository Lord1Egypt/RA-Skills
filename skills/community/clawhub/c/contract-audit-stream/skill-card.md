## Description:

Audits batches of contracts through the dyinsight.cn SSE contract-audit API using either public file URLs or multipart file uploads, with the audit perspective set to PARTY_JIA or PARTY_YI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tzz-v](https://clawhub.ai/user/tzz-v)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit up to five contracts for automated review from either the party A or party B perspective and receive streamed progress plus audit results. It is intended for workflows where the user is authorized to send the contract files or public URLs to the dyinsight.cn service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Contracts, public URLs, and the API key are sent to dyinsight.cn for processing.

Mitigation: Use the skill only for material the user is authorized to share, and confirm privacy, retention, and billing terms before sending sensitive or unredacted contracts.

Risk: The artifact stores the API key in config.json, which can expose credentials if committed or shared.

Mitigation: Prefer an environment variable or secret manager, do not commit a populated config.json, and rotate the key if it was exposed.

Risk: Automated contract audit output may be incomplete or misleading for legal or commercial decisions.

Mitigation: Route audit results through qualified human review before relying on them for negotiations, approvals, or legal action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tzz-v/skills/contract-audit-stream)
- [Contract audit API endpoint](https://dyinsight.cn/api/v1/skills/contract/audit)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with curl examples; API calls return text/event-stream progress events and a final JSON audit result.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an api_key, a PARTY_JIA or PARTY_YI perspective, and either file_urls or multipart files; accepts up to five files and up to 5MB total upload size.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
