## Description:

Access the CarsXE vehicle data APIs for VIN decoding, license plate lookup, market value, vehicle history, safety recalls, lien and theft checks, OBD-II code decoding, vehicle images, international VIN decoding, Year/Make/Model lookups, ownership workflows, and plate or VIN OCR from images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[carsxe](https://clawhub.ai/user/carsxe)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to route vehicle-data requests to CarsXE APIs and present structured results for VINs, plates, recalls, market value, ownership, liens, diagnostics, images, and OCR workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access sensitive owner and resident lookup workflows when the API key has Enterprise ownership access.

Mitigation: Use a separate least-privilege CarsXE key for ordinary vehicle lookups and require explicit user approval before ownership, person, address, or ZIP searches.

Risk: VIN, plate, OCR image, bulk VIN, lien, theft, and ownership queries may expose sensitive vehicle or personal data.

Mitigation: Treat expanded request URLs and returned owner data as sensitive, and avoid ownership ZIP, person, or address searches unless the user has a legitimate authorized purpose.

Risk: Bulk recalls and ownership ZIP searches can create large or billable requests.

Mitigation: Confirm the intended scope before high-volume batch recalls or ZIP ownership lookups, especially when a request could bill many units.

## Reference(s):

- [CarsXE API Docs](https://api.carsxe.com/docs)
- [CarsXE Skill Listing](https://clawhub.ai/carsxe/skills/carsxe)
- [API Reference](references/api-reference.md)
- [Ownership](references/ownership.md)
- [Recalls Batch](references/recalls-batch.md)
- [Recalls by YMM](references/recalls-ymm.md)
- [YMM Options](references/ymm-options.md)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Configuration instructions, Markdown, Guidance]

**Output Format:** [Markdown with inline API requests, shell commands, and summarized JSON or CSV results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CARSXE_KEY and may process sensitive vehicle, plate, image, owner, or resident data.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
