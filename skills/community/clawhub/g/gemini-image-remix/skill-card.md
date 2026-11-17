## Description:

Advanced image generation and remixing using Gemini, supporting Gemini 2.5 Flash Image by default and Gemini 3.0 Pro image preview for advanced tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rdeangel](https://clawhub.ai/user/rdeangel)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to generate new images from prompts, remix one or more reference images, and save the generated result as a PNG file through a Gemini-powered command-line workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected images are sent to Gemini/Google for generation or editing.

Mitigation: Use the skill only for content approved for that service, and avoid confidential or regulated images unless the use has been reviewed.

Risk: API keys can be exposed if passed directly on the command line.

Mitigation: Provide credentials through GEMINI_API_KEY instead of the --api-key option.

Risk: Dependencies are installed through uv without a lockfile in the artifact.

Mitigation: Run in an environment with pinned dependencies or a reviewed lockfile before broader deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rdeangel/skills/gemini-image-remix)
- [Publisher profile](https://clawhub.ai/user/rdeangel)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Configuration instructions]

**Output Format:** [PNG image files with command-line status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uv and GEMINI_API_KEY; accepts prompt, output filename, optional input images, resolution, aspect ratio, and model selection.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
