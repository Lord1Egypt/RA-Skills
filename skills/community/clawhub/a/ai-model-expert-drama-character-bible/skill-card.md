## Description:

This skill helps short-drama and comic-drama teams turn character bible, character profile, relationship, storyboard, scene, and shot-planning needs into structured briefs, prompts, AI-HIVE image or video generation commands, and delivery checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, short-drama writers, comic-drama studios, brands, ecommerce teams, campaign teams, and developers use this skill to plan character settings, character biographies, story and scene assets, shot prompts, and AI-HIVE generation workflows for commercial short-form drama production.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an AI-HIVE API key and may use that key for text, image, video, upload, and task-polling requests.

Mitigation: Use a dedicated low-balance or scoped API key, keep it out of public files and screenshots, and rotate or revoke it after testing.

Risk: The skill can upload selected local media to the configured AI-HIVE endpoint.

Mitigation: Upload only media you are authorized to process and avoid sensitive, private, or regulated content unless your deployment has approved controls.

Risk: The security summary flags broad API-client code and unsafe network/download handling.

Mitigation: Run the scripts in an isolated virtual environment, keep the default endpoint unless you control the replacement, and review outputs before opening or redistributing them.

Risk: Generated files and downloaded media may be written to local output directories.

Mitigation: Choose a dedicated output directory, review filenames before batch runs, and keep generated artifacts separate from important project files.

Risk: Generated character, story, brand, product, or platform guidance may be factually wrong or may rely on unlicensed references.

Mitigation: Verify brand, product, platform, identity, and rights information with the user before publication, and use referenced works only as abstract structural inspiration unless licensed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-model-expert-drama-character-bible)
- [Publisher profile](https://clawhub.ai/user/wubin1836)
- [AI-HIVE homepage](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON files and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local blueprint JSON files, AI-HIVE API requests, uploaded media references, task identifiers, and downloaded image or video outputs when configured with an API key.]

## Skill Version(s):

1.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
