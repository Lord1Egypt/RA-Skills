## Description:

bozo-jiaodu converts image camera-angle requests into one of 96 standardized <sks> camera-position prompts and identifies non-angle image-editing requests as out of scope.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bozoyan](https://clawhub.ai/user/bozoyan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to translate creative image angle descriptions, especially Chinese camera-position requests, into standardized <sks> prompts. Users may also follow the bundled BizyAir shell-script workflow to create and retrieve remote image angle adjustment tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes credentialed shell scripts that send image URLs, prompts, request IDs, and output URLs to BizyAir.

Mitigation: Use only with non-sensitive images and approved URLs, keep BIZYAIR_API_KEY private and scoped, and review the scripts before execution.

Risk: The security summary flags hidden local agent permission settings and shell/curl access as suspicious.

Mitigation: Review or remove hidden local settings before installation and restrict shell/curl permissions in managed environments.

Risk: Prompt conversion is constrained to a fixed set of 96 camera-position prompts and may choose a close match for ambiguous input.

Mitigation: Review the generated <sks> prompt before sending it to an image-editing workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bozoyan/skills/bozo-jiaodu)
- [Skill source](artifact/SKILL.md)
- [BizyAir script README](artifact/scripts/README.md)
- [Evaluation cases](artifact/evals/evals.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text camera prompts, Markdown result tables, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Camera-angle prompt outputs must start with <sks>; BizyAir execution requires BIZYAIR_API_KEY, an image URL, a camera prompt, and a request ID for polling.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
