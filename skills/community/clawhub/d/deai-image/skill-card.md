## Description: <br>
Detects and removes AI-image fingerprints by stripping metadata, adding grain, recompressing files, and altering images to reduce detection by AI-image detectors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[swaylq](https://clawhub.ai/user/swaylq) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers can run CLI workflows to process single images or batches by stripping provenance metadata and applying image transformations. Use only for lawful, authorized research or personal workflows where altering AI-image provenance is acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can be used to hide AI-generated origin from platforms, viewers, or provenance systems. <br>
Mitigation: Use it only for lawful, authorized research or personal workflows, and do not use it to misrepresent AI-generated content. <br>
Risk: The bundled scripts can permanently remove metadata from original image files. <br>
Mitigation: Run the skill only on copies and preserve original files separately. <br>
Risk: Image transformations and recompression can reduce visual quality or introduce artifacts. <br>
Mitigation: Start with the lightest processing strength that meets the authorized workflow and review outputs before distribution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/swaylq/deai-image) <br>
- [Publisher profile](https://clawhub.ai/user/swaylq) <br>
- [Hive Moderation AI-generated content detection](https://hivemoderation.com/ai-generated-content-detection) <br>
- [Illuminarty](https://illuminarty.ai/) <br>
- [AI or Not](https://aiornot.com/) <br>
- [Content Credentials Verify](https://contentcredentials.org/verify) <br>
- [Google SynthID](https://deepmind.google/models/synthid/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Configuration instructions, Files, Guidance] <br>
**Output Format:** [Markdown with inline bash and Python command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces processed image files and terminal status output when the agent runs the bundled scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
