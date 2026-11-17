## Description:

Helps short-drama, comic-video, brand, commerce, traffic-acquisition, and overseas content teams turn ideas, scripts, character images, or reference videos into storyboard, animatic, previs, and deliverable video-generation workflows through AI-HIVE.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, studios, brands, commerce teams, and content operators use this skill to plan and generate short-drama or comic-video assets, including production blueprints, character and scene boards, shot prompts, AI-HIVE generation commands, task tracking, and delivery checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and uses an AI-HIVE API key.

Mitigation: Use a revocable key, keep it out of public files and screenshots, and run the skill in an isolated environment.

Risk: The API key could be sent to an untrusted endpoint if the base URL is changed.

Mitigation: Keep AI_HIVE_BASE_URL and config base_url set to the official AI-HIVE endpoint unless the endpoint has been explicitly trusted.

Risk: Selected images, videos, audio, prompts, and task data may be uploaded to AI-HIVE.

Mitigation: Upload only media the user is authorized to process and avoid including sensitive or unapproved personal, brand, or client data.

Risk: Generated drama, storyboard, or marketing content can include continuity, copyright, likeness, factual, subtitle, or platform-safety issues.

Mitigation: Review generated outputs for authorization, character and scene consistency, factual accuracy, subtitle safety areas, and channel-specific publication rules before use.

Risk: Repeated generation or retrying timed-out tasks may create unexpected cost.

Mitigation: Record task IDs, query existing tasks after timeouts, and check pricing snapshots, models, quantities, and routing choices before submitting batches.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-model-expert-drama-animatic-previs)
- [AI-HIVE homepage](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and JSON configuration or task outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local blueprint JSON files, query AI-HIVE task state, upload selected media, and download generated image or video results when invoked with the bundled scripts.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
