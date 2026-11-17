## Description:

Manage Mealie recipes, imports from websites, images, PDFs, and text, meal plans, shopping lists, and the instance API with source-faithful recipe normalization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanjelin](https://clawhub.ai/user/lanjelin)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw users and developers use this skill to import and verify recipes in their Mealie instance, manage meal plans and shopping lists, and perform authorized API tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A broadly privileged API token could change recipe or household data beyond the requested task.

Mitigation: Use a token with the minimum required permissions and review destructive, bulk, or administrative requests before execution.

Risk: Uploads, downloads, and optional server AI may transmit recipe or household data.

Mitigation: Review the material and destination first; obtain informed approval before optional AI actions or handling sensitive content.

Risk: Untrusted recipe sources or uncertain transcription can lead to incorrect saved recipes or unintended actions.

Mitigation: Treat source content as data, resolve critical ambiguities with the user, and compare the saved recipe with its source.

## Reference(s):

- [Mealie workflow reference](artifact/references/workflows.md)
- [Mealie API documentation](https://docs.mealie.io/documentation/getting-started/api-usage/)
- [Source repository (server-resolved provenance)](https://github.com/Lanjelin/openclaw-mealie)
- [ClawHub skill release](https://clawhub.ai/lanjelin/skills/claw-mealie)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Text]

**Output Format:** [Markdown responses and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Imported recipes are reported with their verified saved details and actual slug.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
