## Description:

Generates AI-assisted outfit recommendations from date, city, province, and style preferences by calling the AI Closet API and composing returned items into shareable outfit images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[houdamiao](https://clawhub.ai/user/houdamiao)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to request outfit ideas such as casual, business, sport, or date looks. The agent extracts available context, runs the bundled script, and returns the generated outfit overview image with the script output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends outfit context and an API key to a third-party AI Closet API.

Mitigation: Use it only with a trusted API operator, limit the key to this service, and avoid sharing sensitive personal context in prompts.

Risk: The remote API influences which images are downloaded, processed, and opened on the local machine.

Mitigation: Run the skill in a constrained environment without sensitive local files or internal network access, and review generated files before broader use.

Risk: The script writes temporary image files and automatically previews the generated overview image.

Mitigation: Avoid shared multi-user systems and consider disabling or reviewing preview behavior before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/houdamiao/skills/aicloset-outfit)
- [AI Closet API base URL](https://aicloset-dev-h5.wxbjq.top)
- [AI Closet outfit generation endpoint](https://aicloset-dev-h5.wxbjq.top/algorithm/open/system_outfit/create_task)

## Skill Output:

**Output Type(s):** [text, shell commands, image files, configuration, guidance]

**Output Format:** [Plain text terminal output with a MEDIA file path and generated PNG outfit overview.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AICLOSET_API_KEY and ImageMagick; writes generated outfit images to a temporary local directory.]

## Skill Version(s):

0.9.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
