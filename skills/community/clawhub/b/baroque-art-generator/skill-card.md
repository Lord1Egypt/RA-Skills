## Description:

Generates dramatic baroque-style oil painting images from text prompts, with optional size selection and reference-image style inheritance through the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blammectrappora](https://clawhub.ai/user/blammectrappora)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to turn subject descriptions into baroque-style image-generation requests and receive a generated image URL. It is suited for classical art prints, portraits, ornate historical artwork, and related visual concepts where the user accepts the Neta API data flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends prompts, optional reference UUIDs, and a Neta token to api.talesofai.com.

Mitigation: Install only after accepting that data flow, and prefer a pinned or verified install path.

Risk: The API token is provided through command-line arguments and may appear in shell history, process listings, CI logs, or command telemetry.

Mitigation: Use a limited-scope token where possible, avoid logging command invocations, and rotate the token if exposure is suspected.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/blammectrappora/skills/baroque-art-generator)
- [Neta AI Open](https://www.neta.art/open/)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration]

**Output Format:** [Plain text image URL with command-line status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta API token; supports portrait, landscape, square, and tall sizes plus an optional reference image UUID.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
