## Description:

Turn any topic into animated explainer videos with Remotion-driven rendering, TTS voiceover, subtitles, and bilingual Chinese/English support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnsonbuilds](https://clawhub.ai/user/johnsonbuilds)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, educators, and content teams use this skill to turn a topic into a short animated explainer video workflow covering research, script generation, storyboarding, Remotion rendering, TTS voiceover, subtitles, and quality checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local setup may run mutable, unpinned external code and dependencies.

Mitigation: Use the server-resolved commit, require a lockfile for dependencies, avoid global npm installs, and run setup in an isolated workspace or container without production secrets.

Risk: Web research and batch rendering can be network- and resource-heavy.

Mitigation: Apply network controls, job limits, storage limits, and render-time quotas before running batch generation.

Risk: Release license evidence conflicts with artifact text that references noncommercial upstream terms.

Mitigation: Confirm the applicable ClawHub release license and any upstream project terms before commercial deployment.

## Reference(s):

- [Server-resolved GitHub import](https://github.com/johnsonbuilds/awesome-hermes-skills/tree/main/creative/anything2explainer)
- [ClawHub skill page](https://clawhub.ai/johnsonbuilds/skills/anything2explainer)
- [Remotion documentation](https://docs.remotion.dev/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and project configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide an agent through multi-step video generation, batch rendering, and output verification.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
