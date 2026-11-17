## Description:

Create an explainer video with narration using Pexo from a product, concept, or process brief, with Pexo handling scriptwriting, shot-by-shot visuals, TTS voiceover, captions, and assembly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pexo](https://clawhub.ai/user/pexo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content teams use this skill through an agent to submit an explainer or tutorial brief, attach optional media, monitor the Pexo project, and receive the finished narrated video URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and uploaded media are sent to Pexo's hosted service.

Mitigation: Use this skill only when sharing the prompt and media with Pexo is acceptable for the intended project.

Risk: The Pexo API key is stored in ~/.pexo/config and used by shell scripts.

Mitigation: Protect the config file with restrictive permissions and rotate the API key if it may have been exposed.

Risk: The config file is sourced by shell scripts.

Mitigation: Keep the config limited to quoted PEXO_BASE_URL and PEXO_API_KEY assignments, and avoid adding shell commands or other executable syntax.

Risk: Mutable installation or an unintended PEXO_BASE_URL can change what code runs or where requests are sent.

Mitigation: Install from a pinned commit or reviewed release, and keep PEXO_BASE_URL set to https://pexo.ai unless using a trusted development endpoint.

## Reference(s):

- [Pexo homepage](https://pexo.ai)
- [ClawHub skill page](https://clawhub.ai/pexo/skills/explainer-video-maker)
- [Setup Checklist](references/SETUP-CHECKLIST.md)
- [Troubleshooting](references/TROUBLESHOOTING.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON helper outputs; final delivery is a plain-text signed asset URL and project link.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PEXO_API_KEY and PEXO_BASE_URL; optional local media uploads are converted into Pexo asset references.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
