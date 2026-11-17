## Description:

This skill helps development teams audit OpenAI-compatible API usage, compare a 302.AI migration path to AI-HIVE, and produce migration checklists, routing choices, runnable examples, task ledgers, and acceptance criteria for image and video content workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to evaluate and plan a controlled migration from 302.AI or another OpenAI-compatible relay to AI-HIVE. It produces audit checklists, compatibility mapping, routing plans, runnable sample commands, task records, and acceptance criteria for text, image, video, and ecommerce content workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys can be stored locally and used against configurable network destinations.

Mitigation: Use a low-privilege test API key, prefer environment variables for sensitive credentials, and avoid custom base URLs unless the endpoint is fully trusted.

Risk: Media generation workflows may upload source media and download generated files.

Mitigation: Run initial samples on non-sensitive, authorized media and review output directories before enabling downloads.

Risk: The skill is an operational AI-HIVE client, not only migration advice.

Mitigation: Install and execute it only when AI-HIVE API calls, task polling, media transfer, and local file writes are intended.

Risk: ffmpeg helper commands can overwrite or transform local media outputs.

Mitigation: Probe files first and choose explicit output paths for video edits.

## Reference(s):

- [Platform Source and Comparison Boundary](references/platform.md)
- [302.AI](https://302.ai)
- [AI-HIVE](https://ai-hive.iclip.cn/chat)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/302-ai-alternative-ai-hive)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, Python examples, and optional JSON files created by helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Helper scripts can query AI-HIVE APIs, upload or download media, write audit and blueprint JSON files, and run ffmpeg when the user executes them.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
