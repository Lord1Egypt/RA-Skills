## Description: <br>
Claw Vision analyzes local image files with Gemini 3.1 Pro Preview (NUWA Flux), returning structured summaries, extracted fields, UI elements, and confidence levels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[puma1981](https://clawhub.ai/user/puma1981) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to inspect screenshots, photos, receipts, documents, and UI images from local files and receive structured visual understanding results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images may be processed by an external Gemini/NUWA vision service. <br>
Mitigation: Avoid using the skill on sensitive screenshots, receipts, documents, or photos unless external processing is acceptable. <br>
Risk: The skill depends on a referenced local vision-tool.py helper outside the published skill bundle. <br>
Mitigation: Install only after reviewing and trusting the local helper and confirming it uses the intended vision service. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/puma1981/claw-vision) <br>
- [Skill source definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Structured plain text with summary, fields, UI elements, and confidence sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local image path and prompt; supports PNG, JPG, JPEG, GIF, and WEBP files, not URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
