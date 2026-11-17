## Description:

AI children's book illustration generator that creates whimsical storybook art, picture book pages, fairy tale scenes, and kids' story illustrations via the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blammectrappora](https://clawhub.ai/user/blammectrappora)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, authors, teachers, parents, and publishing workflows use this skill to generate children's book illustration image URLs from text prompts with optional size and reference-image controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and reference image IDs are sent to the Neta/TalesOfAI API.

Mitigation: Do not submit private manuscripts, personal data, secrets, or regulated content unless the provider's terms and retention policy are acceptable.

Risk: The documented token flag can expose API tokens through shell history, shared machine process listings, CI logs, or copied commands.

Mitigation: Avoid placing real tokens directly on the command line in shared environments; prefer controlled secret handling and scrub logs.

Risk: The documented install command is unpinned, so the installed source may change over time.

Mitigation: Prefer a pinned or reviewed install source before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/blammectrappora/skills/children-book-illustration-generator)
- [Neta AI Open](https://www.neta.art/open/)

## Skill Output:

**Output Type(s):** [Text, API Calls, Shell commands]

**Output Format:** [Plain text image URL with command-line status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta API token; supports portrait, landscape, square, and tall image sizes plus optional reference image UUID for style inheritance.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
