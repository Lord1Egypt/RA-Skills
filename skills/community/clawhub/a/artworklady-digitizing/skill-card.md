## Description:

Artwork Lady embroidery-digitizing intake adapter that uses Playwright to submit digitizing jobs to the Artwork Lady portal, defaults to dry-run validation, and can fetch completed files from the orders page by job reference.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zmtucker](https://clawhub.ai/user/zmtucker)

### License/Terms of Use:

MIT-0

## Use Case:

Operations agents and workflow developers use this skill to send embroidery digitizing jobs to Artwork Lady and retrieve completed stitch files when the portal has no API. It is intended to be called by a routine that supplies job details, local artwork files, and exactly-once status handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send customer artwork and job details to the external Artwork Lady portal when confirm is true.

Mitigation: Install only for workflows that intentionally use Artwork Lady, run dry runs first, and require explicit confirm:true for live submission.

Risk: Portal credentials and saved browser state can expose account access if handled casually.

Mitigation: Use bound environment secrets instead of chat or inline JSON credentials, and keep state and artifact paths inside a controlled workspace.

Risk: A retry after a crash could submit the same job more than once because the portal does not provide a durable confirmation id.

Mitigation: Make the calling routine record submitted job references and submitted-at timestamps, and skip records that already carry a submission marker.

## Reference(s):

- [Artwork Lady portal](https://www.artworklady.com)
- [Artwork Lady placeorder flow notes](references/placeorder_flow_notes.md)
- [ClawHub skill page](https://clawhub.ai/zmtucker/skills/artworklady-digitizing)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files, guidance]

**Output Format:** [JSON command output with Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Submit returns dry_run, submitted, or structured error results; fetch returns fetched, pending, or not_found results with downloaded file paths when available.]

## Skill Version(s):

0.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
