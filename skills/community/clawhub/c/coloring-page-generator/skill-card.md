## Description:

Generates printable black-and-white coloring page line art from text descriptions through the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blammectrappora](https://clawhub.ai/user/blammectrappora)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request printable coloring page images, including kids sheets, adult coloring pages, mandalas, animals, fantasy scenes, and custom line art.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, reference UUIDs, and the Neta token are sent to a third-party AI service.

Mitigation: Use a short-lived or revocable Neta token and avoid confidential, regulated, or sensitive material in prompts and references.

Risk: Installing or running an unverified release can introduce ordinary supply-chain risk.

Mitigation: Install only from a trusted source and prefer a pinned or verified release when available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/blammectrappora/skills/coloring-page-generator)
- [Neta API token page](https://www.neta.art/open/)

## Skill Output:

**Output Type(s):** [Text, Shell commands, API Calls]

**Output Format:** [Plain text URL from command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta token; optional size and reference image UUID parameters affect generation.]

## Skill Version(s):

1.0.0 (source: release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
