## Description:

Children's Picture Book Generator turns story scene prompts into PNG illustrations at preset resolutions using Baidu ERNIE-Image-Turbo through an OpenAI-compatible API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[livingbody](https://clawhub.ai/user/livingbody)

### License/Terms of Use:

MIT-0

## Use Case:

Agents, developers, and content creators use this skill to generate single illustration assets for children's picture-book scenes from text prompts, with explicit control over output path and resolution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts are sent to Baidu AI Studio through a Baidu-compatible API.

Mitigation: Use the skill only when sending the prompt content to Baidu AI Studio is acceptable for the intended workflow.

Risk: API keys can be exposed when passed on the command line.

Mitigation: Prefer environment variables for API keys and avoid command-line secrets in shared or logged environments.

Risk: The OpenAI Python dependency may change behavior across releases.

Mitigation: Pin the openai dependency in controlled deployments.

Risk: Generated output is saved to a user-specified filename and can overwrite an existing file.

Mitigation: Save generated images under a dedicated output folder and choose filenames that avoid accidental overwrites.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/livingbody/skills/children-picture)
- [ClawHub publisher profile](https://clawhub.ai/user/livingbody)
- [Baidu AI Studio](https://aistudio.baidu.com)
- [ERNIE Image](https://aistudio.baidu.com/ernieimage)
- [ERNIE-Image model details](https://aistudio.baidu.com/modelsdetail/46030/intro)
- [OpenAI Python SDK](https://github.com/openai/openai-python)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [PNG image file plus command-line status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One image per invocation; supported resolutions are 1024x1024, 1376x768, 1264x848, 1200x896, 896x1200, 848x1264, and 768x1376.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
