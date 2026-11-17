## Description:

Analyzes video content with Volcengine LAS Doubao vision-language models to answer questions, summarize scenes, detect objects and actions, and generate captions or annotations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcengine-skills](https://clawhub.ai/user/volcengine-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run Volcengine LAS video understanding workflows for video Q&A, scene and object analysis, action recognition, captioning, summaries, and annotations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The environment setup can create or reuse a Python virtual environment and install or update the Volcengine LAS SDK from a remote URL.

Mitigation: Review the setup script before use, and prefer a pinned, hash-verified dependency install for controlled environments.

Risk: The workflow uploads video inputs and optional result files to Volcengine LAS/TOS using LAS credentials.

Mitigation: Confirm the video data is approved for the external service, use least-privilege credentials, and verify LAS region and TOS bucket alignment before upload.

Risk: The polling helper sources a project-level .env file, which could be unsafe in an untrusted workspace.

Mitigation: Inspect or replace .env handling before running the polling helper, and do not run it in workspaces where environment files may be untrusted.

## Reference(s):

- [las_vlm_video API Reference](references/api.md)
- [Volcengine LAS Pricing Reference](references/prices.md)
- [ClawHub Skill Page](https://clawhub.ai/volcengine-skills/skills/byted-las-vlm-video)
- [Volcengine LAS Pricing](https://www.volcengine.com/docs/6492/1544808)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON payload examples, shell commands, and local result files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create result JSON, summary text, event JSON, polling logs, completion status files, and optional uploaded result links; cost estimates are explicitly approximate.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
