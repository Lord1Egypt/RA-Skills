## Description:

Generates images through CreatOK's image generation API and can recover interrupted image generation flows from an existing task id.

This skill is ready for commercial/non-commercial use.

## Publisher:

[newt0n](https://clawhub.ai/user/newt0n)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request AI-generated images or product images, optionally with reference images, and to resume or check existing generation tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Malformed run_id values can write result files outside the intended .artifacts folder.

Mitigation: Run the skill only with trusted or sandboxed run IDs, and review generated artifact paths before using it in less controlled environments.

Risk: Prompts, selected reference images, and generation metadata are sent to CreatOK, and result details are stored locally.

Mitigation: Avoid submitting sensitive prompts or images unless the CreatOK workspace and local artifact storage meet the user's data handling requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/newt0n/skills/creatok-generate-image)
- [Publisher profile](https://clawhub.ai/user/newt0n)
- [Common Rules](references/common-rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, api calls, files, guidance]

**Output Format:** [Markdown responses with image URLs, plus local JSON and Markdown result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes task status, image URLs, raw response details, and errors under the skill artifact output directory.]

## Skill Version(s):

0.1.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
