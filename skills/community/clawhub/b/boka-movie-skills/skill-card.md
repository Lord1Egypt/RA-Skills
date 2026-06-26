## Description: <br>
Bona Movie Production is Bona Group's film-grade production skill for image generation, image editing, and video generation with Nano Banana, Seedance, and Kling models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chengzipidaily](https://clawhub.ai/user/chengzipidaily) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and agents use this skill to prepare and submit Bona image, image-editing, and video-generation tasks, then query or wait for generation results. It is suited for film-grade visual production workflows such as key visuals, posters, character sheets, image-to-video, reference-driven video, and audio-driven video. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, private media URLs, audio references, and video references are sent to an external Bona service for processing. <br>
Mitigation: Do not submit confidential prompts, private media URLs, or sensitive audio/video references unless external processing by the Bona service is acceptable. <br>
Risk: The skill requires a Bona API key or access token for generation and query requests. <br>
Mitigation: Store credentials in environment variables or a secret manager, avoid committing them to files, and rotate them if they may have been exposed. <br>
Risk: Generation tasks can take minutes and may fail, time out, or complete without a result URL in the immediate response. <br>
Mitigation: Use task status as the authoritative signal, continue polling while work is in progress, and report failed or missing-result states without silently changing the requested workflow. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/chengzipidaily/boka-movie-skills) <br>
- [Publisher Profile](https://clawhub.ai/user/chengzipidaily) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown usage guidance with shell command examples and JSON API responses from the Bona client] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Bona API key or access token. Generated media is produced by the external Bona service and returned through task responses or follow-up queries.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
