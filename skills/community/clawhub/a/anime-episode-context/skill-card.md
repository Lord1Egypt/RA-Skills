## Description: <br>
Maintains cross-episode story, character, and visual consistency for AI manga or anime-drama production pipelines generated one episode at a time from uploaded TXT files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JSinBUPT](https://clawhub.ai/user/JSinBUPT) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators producing episodic anime or manga content use this skill to turn the previous episode summary and current episode TXT into reusable continuity notes, visual anchors, and model-specific prompt context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private drafts, spoilers, or sensitive story details may be carried forward into reusable continuity notes. <br>
Mitigation: Review and redact continuity summaries before reusing them in later prompts or sharing them with other systems. <br>
Risk: Incorrect assumptions or hallucinated details can propagate across later episodes and affect generated text, images, or video. <br>
Mitigation: Keep assumptions explicitly labeled and verify each rolling summary against the source episode before using it as the next episode's context. <br>


## Reference(s): <br>
- [episode-context-schema.md](references/episode-context-schema.md) <br>
- [ClawHub skill page](https://clawhub.ai/JSinBUPT/anime-episode-context) <br>
- [Publisher profile](https://clawhub.ai/user/JSinBUPT) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown templates and concise Chinese continuity notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces rolling episode summaries, current-episode context packs, and text/image/video model-specific prompt anchors.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
