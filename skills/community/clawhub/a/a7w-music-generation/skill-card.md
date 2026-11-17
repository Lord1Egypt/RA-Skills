## Description:

Helps agents generate songs and lyrics, work with reference audio and voices, and export music through the a7w music API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2253128](https://clawhub.ai/user/2253128)

### License/Terms of Use:

MIT

## Use Case:

Creators and developers use this skill to request music and lyrics, process reference audio or voices, and retrieve export links using their own a7w API account. Client-facing licensing of generated work requires separate upstream confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API-key exposure or unexpected use of account credits.

Mitigation: Use your own a7w key, keep it out of shared shell history, and review usage and charges.

Risk: The bundled general-purpose client can access API features beyond music generation.

Mitigation: Restrict use of the client to approved music-generation endpoints and review commands before execution.

Risk: Voice cloning or reference audio may involve material used without consent or authorization.

Mitigation: Use only voices and recordings for which you have clear consent or usage rights.

Risk: Client sublicensing or exclusive-rights claims may exceed upstream permissions.

Mitigation: Obtain written upstream confirmation before sublicensing, and avoid unsupported exclusivity or ownership guarantees.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/2253128/skills/a7w-music-generation)
- [Getting started](artifact/references/getting-started.md)
- [Music creation API](artifact/references/api-create.md)
- [Voice cloning API](artifact/references/api-voice_clone.md)
- [Authorization and rights boundaries](artifact/references/授权与权利边界.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON responses]

**Output Format:** [Markdown instructions, command examples, and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [API results may include links to generated media; generation consumes the user's account credits.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
