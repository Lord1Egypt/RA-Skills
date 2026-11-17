## Description:

Helps ad teams diagnose failed advertising creatives by separating creative, product, audience, landing-page, and delivery factors, then producing repair priorities, refreshed scripts, prompts, checklists, and optional AI-HIVE generation commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External marketing operators, ecommerce teams, editors, and developers use this skill to turn low-performing ad creative evidence into a diagnosis, evidence gaps, platform fit checks, repair priorities, revised scripts, prompts, runnable commands, and acceptance criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent AI-HIVE API keys may be stored and reused by the skill.

Mitigation: Use a scoped or disposable AI-HIVE API key, keep the local config file private, and remove or rotate the key after use.

Risk: A custom API base URL can receive the bearer token and uploaded media.

Mitigation: Use only the legitimate AI-HIVE HTTPS API endpoint unless the publisher and endpoint are independently trusted.

Risk: Generation commands may upload local media or create paid AI-HIVE tasks.

Mitigation: Review prompts, routing, uploaded files, and model parameters before execution, and start with small samples before batch work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ad-creative-failure-diagnosis-ai-hive)
- [AI-HIVE chat and API access](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API base URL](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON snippets and inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create blueprint JSON files, process local video with ffmpeg, upload media to AI-HIVE, submit asynchronous generation tasks, poll task status, and download generated assets when the user authorizes execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
