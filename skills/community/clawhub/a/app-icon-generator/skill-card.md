## Description:

Generates professional app icons for iOS, Android, and web apps from text prompts using the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blammectrappora](https://clawhub.ai/user/blammectrappora)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, startups, indie makers, and designers use this skill to request app icon artwork from text descriptions, with optional size selection and reference-image style inheritance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, optional reference UUIDs, and the Neta API token are sent to a third-party service.

Mitigation: Avoid sensitive prompt content, use a disposable or limited-scope API token, and review the third-party service before production use.

Risk: Passing the token on the command line can expose it through shell history, process listings, terminal scrollback, or logs.

Mitigation: Use a token dedicated to this workflow, run on trusted systems, and clear shell history or logs that may capture command invocations.

Risk: Installing with an unpinned npx command can execute package content from the resolved source path.

Mitigation: Install only from trusted ClawHub/source paths, avoid administrator privileges, and pin or review the installed artifact before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/blammectrappora/skills/app-icon-generator)
- [Publisher profile](https://clawhub.ai/user/blammectrappora)
- [Neta API token access](https://www.neta.art/open/)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text image URL with CLI guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports square, portrait, landscape, and tall image dimensions; optional reference image UUID can guide style inheritance.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
