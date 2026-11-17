## Description:

Create and edit eBay listing videos that document exact-item condition, defects, functional tests, included accessories, refurbished work and collectible details; supports conservative Seedance editing through AI Hive.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, listing operators, and agents use this skill to generate, edit, and document eBay product videos that preserve actual item condition, defects, functional tests, accessories, refurbished work, and collectible details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may send the user's AI Hive API key and selected listing media to a caller-configurable API endpoint.

Mitigation: Use only the trusted AI Hive endpoint, avoid setting --base-url, AI_HIVE_BASE_URL, or config base_url to an untrusted host, and review media before upload.

Risk: The skill stores and reads an AI Hive API key from local configuration.

Mitigation: Use an isolated environment, restrict local configuration file permissions, and rotate the API key if it may have been exposed.

Risk: Generated or edited listing media could misrepresent item condition, defects, tests, or included accessories.

Mitigation: Retain source-to-output records, distinguish actual-item footage from generated context, and review outputs against the listing before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ebay-ecommerce-video-generation-editing)
- [Publisher profile](https://clawhub.ai/user/wubin1836)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with bash commands and generated media file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses AI Hive API credentials and may upload selected listing media for video generation, extension, editing, task polling, and download.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact changelog also contains entries through 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
