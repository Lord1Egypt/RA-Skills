## Description:

Imports contracts into Contracko from disk, Google Drive, SharePoint, Box or a URL. Use to onboard, migrate, bulk-upload, or file a signed PDF.

This skill is ready for commercial/non-commercial use.

## Publisher:

[contracko](https://clawhub.ai/user/contracko)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to import, migrate, and file contract documents into Contracko from local folders, cloud drives, or authenticated URLs. It helps agents choose the appropriate import path, confirm bulk writes, poll extraction status, and surface import errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses contract:write access to import or ingest contracts, and a batch sent to the wrong workspace may require manual cleanup.

Mitigation: Verify the workspace, document count, and file names with the user before bulk import or ingest operations.

Risk: Confidential contracts could be exposed if an agent creates public links for remote import.

Mitigation: Use signed or authenticated links from the user's own document store, or use the upload path so contract bytes do not pass through public hosting.

Risk: Manual ingest can create thin or misleading records if the agent omits contract analysis and field evidence.

Mitigation: Extract contract text, populate metadata and analysis fields from the document, and include evidence quotes where the destination workflow expects them.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, JSON, API calls]

**Output Format:** [Markdown guidance with inline shell commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes confirmation steps for bulk writes, file-size and MIME checks, idempotency guidance, polling behavior, and error-handling guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
