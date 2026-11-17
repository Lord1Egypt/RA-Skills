## Description:

Turn an article into a narrated explainer video by creating an outline and storyboard, generating voiceover, and building and validating the video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

People who want a narrated explainer, report, courseware, or training video from an article or document can use this skill to guide video creation through prompts and follow-up project sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends prompts to dLazy's hosted service and uploads attached files to its media storage.

Mitigation: Review the service details and only send content you are comfortable sharing with dLazy.

Risk: The security scan had medium confidence and was partial; it noted project-listing and login behavior and could not resolve some references or package details.

Mitigation: Review the install and service details and confirm that the login and project-listing behavior fits your needs before use.

Risk: The CLI requires a dLazy API key, which may be saved in the local CLI configuration or supplied through an environment variable.

Mitigation: Keep the key private and rotate or revoke it from the dLazy dashboard if it is exposed.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dlazyai/skills/dlazy-article-to-video)
- [CLI project page](https://github.com/dlazy-ai/cli)
- [CLI npm package](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy homepage](https://dlazy.com)

## Skill Output:

**Output Type(s):** [Video, Text, Shell commands, Configuration instructions]

**Output Format:** [Narrated explainer video with textual status and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Projects can continue across multiple chat sessions; attached files are uploaded to the service.]

## Skill Version(s):

1.0.46 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
