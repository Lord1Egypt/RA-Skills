## Description:

Generate illustrations and visuals using Antekirt artists and prompts, including image generation, SVG vectorization, and short video animation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andrejdorsian](https://clawhub.ai/user/andrejdorsian)

### License/Terms of Use:

MIT-0

## Use Case:

External users, team members, and developers use this skill to select an Antekirt artist, submit visual prompts, and receive generated image, SVG, or video URLs for use or download.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends API keys, prompts, artist selections, and generation metadata to a configurable network endpoint.

Mitigation: Use it only for intended Antekirt workflows, set ANTEKIRT_BASE_URL exactly to https://api.antekirt.com, and avoid environments where that variable can be overridden unexpectedly.

Risk: Broad image-generation trigger phrases may activate the skill and consume Antekirt credits.

Mitigation: Confirm the user intends to use Antekirt before starting generation, especially for video or repeated image requests.

Risk: Generated assets depend on asynchronous provider jobs that may fail, time out, or return no usable output.

Mitigation: Surface failed or timed-out jobs clearly and preserve artistId, prompt, and generationId for follow-up or audit.

## Reference(s):

- [Antekirt API Endpoints](artifact/references/api-endpoints.md)
- [Antekirt Documentation](https://antekirt.com/docs)
- [ClawHub Skill Page](https://clawhub.ai/andrejdorsian/skills/antekirt-generate-artist-backed-illustrations)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and CLI output containing generated asset URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ANTEKIRT_API_KEY, ANTEKIRT_BASE_URL, node, curl, and Antekirt account credits.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
