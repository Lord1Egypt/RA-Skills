## Description:

Guides agents to generate AI music and songs with Diffrythm and Tencent Song Generation through the inference.sh CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[okaris](https://clawhub.ai/user/okaris)

### License/Terms of Use:


## Use Case:

External developers and content creators use this skill to generate instrumentals, songs with vocals, background music, podcast jingles, and game soundtracks from prompts using inference.sh audio apps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The quick start runs a live internet installer directly in a shell before authentication.

Mitigation: Use a manual, version-pinned CLI download with an independently published checksum or signature, and run login as a separate step.

Risk: Related optional skills may expand the agent's audio and video capabilities beyond this skill's music-generation scope.

Mitigation: Review and approve each optional related skill separately before adding it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/okaris/skills/ai-music-generation)
- [inference.sh](https://inference.sh)
- [Running Apps](https://inference.sh/docs/apps/running)
- [Content Pipeline Example](https://inference.sh/docs/examples/content-pipeline)
- [Apps Overview](https://inference.sh/docs/apps/overview)
- [CLI Checksums](https://dist.inference.sh/cli/checksums.txt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown instructions with inline shell commands and JSON CLI inputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes inference.sh app IDs, prompt examples, and install guidance.]

## Skill Version(s):

0.1.5 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
