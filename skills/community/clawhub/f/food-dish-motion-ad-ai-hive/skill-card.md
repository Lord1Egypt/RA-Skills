## Description:

Turns restaurant dish motion-ad requests into production-ready workflows, scripts, prompts, AI-HIVE video-generation commands, and quality checks for food brands, delivery merchants, and local-commerce operators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External restaurant brands, delivery merchants, food e-commerce teams, and local-commerce operators use this skill to turn authorized dish assets, store facts, platform requirements, and campaign goals into short-form motion-ad plans and AI-HIVE generation commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AI-HIVE API keys could be exposed through logs, screenshots, or repository commits.

Mitigation: Use environment variables or the local config flow, keep keys out of shared outputs, and verify local config file permissions before use.

Risk: Video or image generation may incur charges after task submission.

Mitigation: Confirm the prompt, files, model, route, and pricing snapshot before generation; use a small sample before batch work.

Risk: Uploaded reference media may include private, copyrighted, trademarked, or otherwise unauthorized content.

Mitigation: Upload only media the user has rights to use and avoid replicating protected ads, logos, music, personalities, or exact shot sequences.

Risk: Food, price, store, quantity, or promotional claims can mislead viewers if generated from unverified facts.

Mitigation: Verify product and campaign facts before publication and mark unknown prices, store details, performance claims, or ingredient claims as pending review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/food-dish-motion-ad-ai-hive)
- [AI-HIVE chat](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API base](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with JSON briefs, prompt text, shell command examples, task records, and generated media file paths when commands run.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create blueprint JSON files, upload authorized media to AI-HIVE, submit asynchronous generation tasks, poll task status, and download resulting media.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
