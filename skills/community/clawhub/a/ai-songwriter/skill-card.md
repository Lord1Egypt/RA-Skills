## Description:

AI Songwriter turns a user-provided theme into Chinese pop lyrics, Suno style tags, and generated Suno audio links through an automated multi-step workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jason-hou-pe](https://clawhub.ai/user/jason-hou-pe)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creators use this skill to turn a song theme into polished Chinese pop lyrics, Suno-ready style tags, and generated audio links. Agents running the workflow need a KIE_API_KEY or SUNO_API_KEY for the external kie.ai music generation step.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow automatically runs local Node.js code and submits generated lyrics to the external kie.ai API.

Mitigation: Review before installing and run only where automatic local execution and external content submission are acceptable; add a confirmation step before network submission for stricter deployments.

Risk: The workflow uses unsafe command and temporary-file handling for generated lyrics.

Mitigation: Avoid shell interpolation and pass generated content through stdin or a private temporary file with restricted permissions.

Risk: The bundled script includes extra audio URL modes beyond the normal generation workflow.

Mitigation: Document or remove the extra audio URL modes before deployment if they are not required.

## Reference(s):

- [ClawHub AI Songwriter release](https://clawhub.ai/jason-hou-pe/skills/ai-songwriter)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands]

**Output Format:** [Markdown containing lyrics, Suno style tags, generated audio URLs, and command execution details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires KIE_API_KEY or SUNO_API_KEY; generated lyrics are submitted to kie.ai for music generation.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
