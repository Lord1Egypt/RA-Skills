## Description: <br>
Generate music using Volcengine Imagination API. Supports vocal songs, instrumental BGM, and lyrics generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volcengine-skills](https://clawhub.ai/user/volcengine-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate vocal songs, instrumental background music, soundtracks, and lyrics through Volcengine's music generation API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, lyrics, and generation settings are sent to Volcengine. <br>
Mitigation: Avoid submitting sensitive or proprietary lyrics unless that use is acceptable under Volcengine's terms. <br>
Risk: Song and BGM generation may use paid postpaid API billing by default. <br>
Mitigation: Use a dedicated Volcengine account or key with spending limits and review billing settings before generation. <br>
Risk: The skill requires Volcengine access keys for API calls. <br>
Mitigation: Use least-privilege credentials and do not store keys in shared workspace files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/volcengine-skills/byted-music-generate) <br>
- [Volcengine Music Generation Docs](https://www.volcengine.com/docs/84992) <br>
- [Volcengine API Signature Guide](https://www.volcengine.com/docs/6369/67269) <br>
- [Volcengine Music Generation Parameters](references/parameters.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON results from the generation script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns status, mode, task_id, audio_url, duration, lyrics, and error fields when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
