## Description:

Convert a blog post supplied as text or a link into a narrated video with a storyboard and voiceover for social media or YouTube.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

External users can give the skill a blog post as text or a link and use it to create a narrated video project for social media or YouTube.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The trigger description focuses on blog posts, while the instructions also describe converting broader document types.

Mitigation: Check that the skill's current trigger and file-to-video workflow match the content and task you intend to submit.

Risk: Prompts and files attached through the CLI are sent to dLazy services, and attached files are uploaded to its media storage.

Mitigation: Do not submit sensitive material unless that transfer is permitted for your use case.

Risk: The workflow requires running the dLazy CLI and authenticating with a dLazy API key.

Mitigation: Review the CLI package and service terms before use, and keep the API key private.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dlazyai/skills/dlazy-blog-to-video)
- [dLazy website](https://dlazy.com)
- [CLI source link listed in skill metadata](https://github.com/dlazy-ai/cli)
- [dLazy CLI on npm](https://www.npmjs.com/package/@dlazy/cli)

## Skill Output:

**Output Type(s):** [Video, Text, Guidance]

**Output Format:** [Narrated video project with a storyboard and voiceover, accompanied by text responses and CLI guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Projects can continue across chat sessions; local files attached to a request are uploaded to dLazy media storage.]

## Skill Version(s):

1.0.44 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
