## Description:

Searches Chinese design patents by product name and Locarno class, then organizes representative images into a side-by-side comparison list.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

External product designers and product teams use this skill to find comparable Chinese design patents before developing or launching a product. It produces a comparison list with representative images; it does not provide an infringement determination.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: API-key handling and cache-path validation need review before use.

Mitigation: Use a limited-spend key supplied outside chat, review any persistent key storage, and set a task budget. Avoid sharing confidential design details.

Risk: Until validation and redirect protections are confirmed, unusual patent-number inputs or non-default endpoints may increase risk.

Mitigation: Use ordinary patent numbers and the default HTTPS endpoint.

## Reference(s):

- [Search workflow](references/search-workflow.md)
- [Query syntax](references/query-syntax.md)
- [API reference](references/api-reference.md)
- [PatentMax API platform](https://api.ip930.com/features/api-platform)

## Skill Output:

**Output Type(s):** [Analysis, Files, CSV, Images, Guidance]

**Output Format:** [CSV comparison list with representative patent images and concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Covers Chinese design patents; includes one representative image per selected patent and does not provide a legal infringement conclusion.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
