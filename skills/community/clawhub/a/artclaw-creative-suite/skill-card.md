## Description:

Invokes ARTCLAW platform content-creation capabilities through a CLI-backed REST API workflow, including image generation, video generation, workflow execution, multimodal analysis, and job management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alanhuangyoo](https://clawhub.ai/user/alanhuangyoo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative operators use this skill to submit ARTCLAW image, video, workflow, and multimodal analysis jobs from an agent environment. It also guides account setup, asynchronous job handling, result delivery, and job-status follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access ARTCLAW API credentials and optional chat-delivery credentials.

Mitigation: Install only from a trusted publisher, prefer environment-provided API keys, and scope delivery credentials to the minimum channels needed.

Risk: The skill can run asynchronous generation and delivery flows using user-provided prompts, URLs, and file paths.

Mitigation: Do not pass untrusted prompts, URLs, or local file paths into spawn or delivery mode, and review job metadata before sharing generated media.

Risk: The skill includes a self-update path that can replace installed files.

Mitigation: Use dry-run or independent source verification before self-update, and review changes before continuing to use the updated skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alanhuangyoo/skills/artclaw-creative-suite)
- [Publisher profile](https://clawhub.ai/user/alanhuangyoo)
- [ARTCLAW platform](https://artclaw.com/)
- [ARTCLAW API base](https://artclaw.com/api/v1)
- [ARTCLAW API key settings](https://artclaw.com/settings)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated media jobs return job metadata and result URLs; analysis commands return synchronous text or JSON responses.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
