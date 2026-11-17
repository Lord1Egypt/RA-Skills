## Description:

Make a founder video with Pexo for solo founders and small teams by sending a story, product, pitch, or site to the hosted Pexo agent, which writes the script, generates shots, and returns a finished video with music.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pexo](https://clawhub.ai/user/pexo)

### License/Terms of Use:

MIT-0

## Use Case:

External users, solo founders, and small teams use this skill to turn a founder story, product pitch, or website into a finished fundraising, Product Hunt, or personal-brand video through Pexo's hosted video agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, business details, and uploaded media are sent to Pexo's hosted service.

Mitigation: Install only if you trust Pexo and are comfortable sharing those inputs with the service.

Risk: The skill uses a Pexo API key stored in configuration or environment variables.

Mitigation: Use a narrowly scoped key, keep the config file readable only by the user, and rotate the key if it is exposed.

Risk: Changing PEXO_BASE_URL can send requests and credentials to a different endpoint.

Mitigation: Keep PEXO_BASE_URL set to https://pexo.ai unless the replacement endpoint is fully trusted.

Risk: Unpinned installation can make the reviewed artifact differ from a later installed copy.

Mitigation: Inspect the exact installed version or commit before deployment.

## Reference(s):

- [Founder Video skill page](https://clawhub.ai/pexo/skills/founder-video)
- [Pexo homepage](https://pexo.ai)
- [Setup Checklist](references/SETUP-CHECKLIST.md)
- [Troubleshooting](references/TROUBLESHOOTING.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, JSON script outputs, and plain-text project or asset URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PEXO_API_KEY and PEXO_BASE_URL; may upload local media and retrieve signed asset URLs.]

## Skill Version(s):

0.1.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
