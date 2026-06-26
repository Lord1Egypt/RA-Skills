## Description: <br>
Discover nearby film and TV shooting locations from a user's city and position, then produce five photo-recreation cases with location details, scene guidance, weather-aware camera settings, and cinematic reference images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kensonh](https://clawhub.ai/user/kensonh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers, film fans, and photographers use this skill to find nearby filming locations and plan scene-recreation photos. It combines location, weather, film-scene, map, camera-setting, and image-generation guidance into five self-contained cases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses and displays location information, including exact coordinates, which can expose sensitive personal location details in transcripts or shared outputs. <br>
Mitigation: Ask users to confirm only the minimum location precision needed, avoid home addresses when possible, and remind them not to share outputs containing exact coordinates. <br>
Risk: The install script can write skill files to different agent platform directories depending on detected or requested platform. <br>
Mitigation: Use the dry-run option or an explicit platform selection before installation so users can preview destination paths. <br>
Risk: Generated scene images and film-location details may not perfectly match real locations, film shots, or current access conditions. <br>
Mitigation: Present generated images as planning references and encourage users to verify access, maps, weather, and local rules before traveling or photographing. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kensonh/film-location-scout) <br>
- [Publisher profile](https://clawhub.ai/user/kensonh) <br>
- [Scene prompt templates](scene-prompts.md) <br>
- [Photography parameters reference](photo-params-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Shell commands, Configuration, Image prompts] <br>
**Output Format:** [Markdown with structured case cards, tables, map links, generated image references, and optional shell commands for installation or distance checks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces five cases with GPS coordinates, film-scene descriptions, weather-aware camera settings, composition tips, and photo recreation guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
