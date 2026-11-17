## Description:

Generates videos from text prompts, image prompts, multiple reference images, or keyframes through the Agnes Video V2.0 asynchronous API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lutongsuo](https://clawhub.ai/user/lutongsuo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to generate short videos, animate still images, create multi-image transitions, and produce keyframe animations for storytelling, marketing, social media, and product demos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, image URLs, and the Agnes API key are sent to the Agnes API.

Mitigation: Use only with inputs and credentials approved for the Agnes service, and avoid submitting sensitive prompts or private image URLs unless permitted.

Risk: The bundled shell scripts were flagged for unsafe coding, including heredoc injection risk and an unvalidated video download path.

Mitigation: Review and fix the shell scripts before execution, especially prompt interpolation and output path handling.

Risk: The test script creates a real video task rather than performing a read-only connection check.

Mitigation: Run connection tests only when task creation side effects and possible API usage costs are acceptable.

Risk: The main video script contains a broken extra fi that may prevent successful execution.

Mitigation: Correct the shell syntax error and rerun shell syntax checks before using the script.

## Reference(s):

- [Agnes Video V2.0 API](references/API.md)
- [Agnes Video V2.0 Prompt Guide](references/PROMPT_GUIDE.md)
- [Agnes Video V2.0 Examples](references/EXAMPLES.md)
- [ClawHub skill page](https://clawhub.ai/lutongsuo/skills/agnes-video)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with bash commands, JSON API examples, and optional downloaded video files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses an asynchronous task flow that creates a video task, polls for completion, and can save an output video file.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
