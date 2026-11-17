## Description:

Uses a Gemini web session to send prompts, continue conversations, upload images or files, retrieve Gemini replies, and recover login or page state when needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lainxxx](https://clawhub.ai/user/lainxxx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill when they want an agent to operate the Gemini web interface for a real conversation, including prompt submission, conversation continuation, and optional file or image upload.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use an authenticated Gemini web session and send prompts or selected files/images to Gemini.

Mitigation: Use it only with inputs intended for Gemini, avoid sensitive files, and add an explicit confirmation step for file or image uploads in sensitive workflows.

Risk: The release evidence says the skill relies on unaudited runtime scripts that are not present in the artifact.

Mitigation: Review, provide, and scan the runtime scripts before deployment or execution.

Risk: The skill may launch or reuse Chrome in the background, which can make session activity less visible to the user.

Mitigation: Run it with a dedicated browser profile or visible headed mode when monitoring session activity is required.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/lainXXX/gemini-web-automation-skill)
- [ClawHub skill page](https://clawhub.ai/lainxxx/skills/gemini-web-automation-skill)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Structured JSON from the runtime and concise text or Markdown guidance to the user.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Gemini replies, runtime error routing, login recovery guidance, and file or image upload handling.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
