## Description:

Manage Coda Packs via REST API v1. Supports listing, creating, updating, and deleting private Packs. Requires CODA_API_TOKEN. Delete requires confirmation. Note: Builds, Gallery submission, Analytics, and Collaborators require Coda's Pack SDK CLI, not available via REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0x7466](https://clawhub.ai/user/0x7466)

### License/Terms of Use:


## Use Case:

Developers use this skill to manage private Coda Pack shells from an agent workflow, including listing Packs, creating new shells, updating metadata, and deleting unused Packs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Coda API token with Pack-management permissions can create, update, or delete private Packs.

Mitigation: Use the least-privileged Coda token available, prefer CODA_API_TOKEN over command-line token arguments, and rotate the token if it may have been exposed.

Risk: Pack deletion is irreversible, and forced deletion can bypass interactive confirmation.

Mitigation: Double-check Pack IDs and names before deletion, and reserve --force for deliberate automation with independent safeguards.

Risk: Pack SDK commands shown by the skill use npm/npx tooling that may change over time if left unpinned.

Mitigation: Pin or locally lock @codahq/packs-sdk before running Pack development commands.

## Reference(s):

- [Coda Pack SDK Guides](https://coda.io/packs/build/latest/guides/overview/)
- [Coda Pack SDK Quickstart](https://coda.io/packs/build/latest/guides/quickstart/)
- [Coda API Docs](https://coda.io/developers/apis/v1)
- [Coda Pack SDK npm Package](https://www.npmjs.com/package/@codahq/packs-sdk)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with inline shell commands and CLI output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call the Coda REST API v1 and may create, update, or delete private Coda Packs when given a valid CODA_API_TOKEN.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
