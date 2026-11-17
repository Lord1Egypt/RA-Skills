## Description:

Builds multi-step AI content creation pipelines that combine image, video, audio, and text generation through inference.sh CLI workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[okaris](https://clawhub.ai/user/okaris)

### License/Terms of Use:


## Use Case:

Developers, creators, and marketing teams use this skill to plan and run AI-assisted content pipelines for short videos, social media assets, product demos, and blog-to-video workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends remote installer and related-skill commands that may execute mutable code or install unpinned dependencies.

Mitigation: Review install commands before execution, prefer pinned releases, verify checksums or signatures, and run in a non-administrative environment.

Risk: Pipeline inputs may include confidential drafts, private media, secrets, or regulated data sent through inference.sh or underlying providers.

Mitigation: Avoid sensitive inputs unless the relevant privacy, retention, and provider terms have been reviewed and approved.

## Reference(s):

- [AI Content Pipeline skill page](https://clawhub.ai/okaris/skills/ai-content-pipeline)
- [inference.sh](https://inference.sh)
- [Content Pipeline Example](https://inference.sh/docs/examples/content-pipeline)
- [Building Workflows](https://inference.sh/blog/guides/ai-workflows)
- [CLI checksum verification](https://dist.inference.sh/cli/checksums.txt)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown]

**Output Format:** [Markdown with inline shell commands and JSON input examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces workflow plans, command sequences, and example inputs for running media-generation pipelines.]

## Skill Version(s):

0.1.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
