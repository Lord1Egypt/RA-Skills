## Description:

Baidu Wenku AI Picture Book creates static or dynamic AI-generated picture-book videos from story text and returns generated video URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ide-rea](https://clawhub.ai/user/ide-rea)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, educators, marketers, and media teams use this skill to submit story text to Baidu Wenku or Qianfan, create a static or dynamic picture-book generation task, and poll until video URLs are available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted story content and task IDs can be redirected through an environment-provided scheduler URL.

Mitigation: Install and run the skill only in trusted environments, and leave DUMATE_SCHEDULER_URL and DUMATE_SESSION_ID unset unless the scheduler service is explicitly trusted.

Risk: Story text may contain confidential or regulated content that should not be submitted to an external generation service.

Mitigation: Do not submit confidential, sensitive, or regulated story content; review content and data-handling requirements before use.

Risk: Providing the Baidu API key as a command-line argument can expose it through shell history or process listings.

Mitigation: Provide BAIDU_API_KEY through the environment instead of command-line arguments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ide-rea/skills/ai-picture-book)
- [Baidu Qianfan API base](https://qianfan.baidubce.com/v2)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and BAIDU_API_KEY; successful task results may include video_bos_url values.]

## Skill Version(s):

1.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
