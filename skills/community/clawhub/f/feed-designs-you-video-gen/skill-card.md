## Description: <br>
Create vertical algorithm-control shorts with five equal caption beats across the runtime, UI/data-stream montage, and WeryAI video generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoucdr](https://clawhub.ai/user/zoucdr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and agents use this skill to prepare vertical social videos critiquing algorithmic feeds, with fixed five-beat caption timing and WeryAI generation settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, generation parameters, and supplied public image URLs are sent to WeryAI using the user's API key. <br>
Mitigation: Use the skill only when external processing is intended, and avoid private screenshots or sensitive imagery unless the user explicitly approves that processing. <br>
Risk: The skill requires a paid external API key and network access. <br>
Mitigation: Keep WERYAI_API_KEY in the environment, do not paste or log the secret, and confirm expected WeryAI usage before submitting generation jobs. <br>
Risk: Generated rhetoric about algorithmic feeds could imply factual platform internals or individual targeting beyond the skill's intended critique. <br>
Mitigation: Frame outputs as system critique, avoid named individuals, and do not claim illegal surveillance unless the user clearly requests fiction. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zoucdr/feed-designs-you-video-gen) <br>
- [WeryAI video API reference](resources/WERYAI_VIDEO_API.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with prompt text, inline JSON, shell commands, and a final video link when generation succeeds.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WERYAI_API_KEY, Node.js 18+, network access, and WeryAI credits.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
