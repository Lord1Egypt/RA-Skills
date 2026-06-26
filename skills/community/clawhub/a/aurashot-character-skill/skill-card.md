## Description: <br>
AuraShot Character Skill helps agents create and edit identity-preserving character images from face references, including ID photos, scene and outfit generation, and natural-language edits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whbzju](https://clawhub.ai/user/whbzju) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agent builders use this skill to guide character setup, manage local character assets, and call AuraShot commands for identity-preserving image generation and editing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload face photos, reference images, and prompts to AuraShot and may receive hosted image URLs in return. <br>
Mitigation: Use only images the user owns or has explicit consent to process, and tell users when local files must be uploaded to the external service. <br>
Risk: API keys may be stored in `.aurashot.env` for local execution. <br>
Mitigation: Keep `.aurashot.env` private, exclude it from version control, and avoid exposing keys in chat transcripts or generated files. <br>
Risk: Identity-preserving image generation can be misused for deceptive, non-consensual, sexualized, or impersonation content involving real people. <br>
Mitigation: Decline requests that lack consent or appear deceptive, sexualized, or impersonation-oriented for real people. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/whbzju/aurashot-character-skill) <br>
- [AuraShot homepage](https://www.aurashot.art) <br>
- [AuraShot API documentation](https://www.aurashot.art/studio?tab=docs) <br>
- [AuraShot Character Design API Reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Natural-language guidance with inline shell commands and JSON command results from the AuraShot CLI.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local avatar directories, metadata JSON, downloaded image files, and references to hosted image URLs returned by AuraShot.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
