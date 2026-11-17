## Description:

Helps short-drama and manhua teams turn episode synopsis requests into executable planning briefs, character and scene assets, shot prompts, AI-HIVE generation tasks, and delivery checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creative, commerce, and production teams use this skill to plan short-drama episode outlines, structure reusable story assets, and generate or track AI-HIVE image and video tasks for commercial delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store and use an AI-HIVE API key locally.

Mitigation: Keep API keys out of public files and screenshots, store them only in the local configuration or environment, and rotate or revoke keys when no longer needed.

Risk: The skill can upload local media to AI-HIVE.

Mitigation: Upload only media that the user is authorized to share, and avoid private or sensitive files unless the AI-HIVE account and workflow are trusted.

Risk: Image and video generation tasks may be billable and may continue after local polling times out.

Mitigation: Review model pricing and routing before submission, save task IDs, and query existing tasks instead of resubmitting after a timeout.

Risk: Changing AI_HIVE_BASE_URL or --base-url can direct credentials and media to an untrusted service.

Mitigation: Use the default AI-HIVE endpoint unless the alternate endpoint is explicitly trusted.

Risk: Generated outputs may be downloaded to local directories.

Mitigation: Prefer --no-download until the task source and output directory are trusted.

## Reference(s):

- [AI-HIVE](https://ai-hive.iclip.cn/chat)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-model-expert-drama-episode-synopsis)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and JSON file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local blueprint JSON files, submit AI-HIVE generation tasks, print task JSON, and optionally download generated media files.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
