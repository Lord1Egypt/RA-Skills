## Description:

Batch image generation assistant for BizyAir asynchronous APIs, supporting multiple API keys from local files, remote URLs, or environment variables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bozoyan](https://clawhub.ai/user/bozoyan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run batch BizyAir image generation jobs across multiple API keys, including storyboard scenes and custom web app calls. It helps create tasks, poll task status, and present generated image URLs in Markdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys and prompt contents are sent to BizyAir and may be handled in local task state.

Mitigation: Use limited or disposable BizyAir keys, avoid sensitive prompts, and verify that /tmp/bizyair.txt is removed after use.

Risk: Remote key URLs can expose credentials or pull keys from an untrusted source.

Mitigation: Prefer local key files or environment variables, and only use remote key URLs from trusted, access-controlled locations.

Risk: The skill can automatically append model-related prompt text when person or portrait keywords are detected.

Mitigation: Review generated prompts before task creation and make prompt expansion explicit for sensitive or regulated image generation workflows.

## Reference(s):

- [BizyAir OpenAPI endpoint](https://api.bizyair.cn/w/v1/webapp/task/openapi)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown with task summaries, image URL tables, and inline shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write temporary task state to /tmp/bizyair.txt and image URL lists under a temporary results directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
