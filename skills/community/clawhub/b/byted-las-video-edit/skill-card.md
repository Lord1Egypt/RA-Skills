## Description: <br>
Byted Las Video Edit helps agents extract and clip segments from long videos using natural-language descriptions, optional reference images, and Volcengine LAS simple or detail modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volcengine-skills](https://clawhub.ai/user/volcengine-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and video operators use this skill to submit Volcengine LAS video-editing jobs, estimate cost, poll task status, and return clip metadata and download links for requested scenes, people, objects, actions, or highlights. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow installs a remote Volcengine SDK package during environment initialization. <br>
Mitigation: Install only if the publisher and SDK source are trusted; review scripts/env_init.sh and pin or verify the SDK package before use. <br>
Risk: A helper may execute local .env content as shell code. <br>
Mitigation: Review local environment files before running helpers and avoid placing executable shell content in project .env files. <br>
Risk: The skill requires LAS credentials and may upload local videos or reference images to Volcengine or TOS for processing. <br>
Mitigation: Use a limited LAS API key, confirm the estimated cost before submission, and avoid sending media that is not approved for the target service. <br>


## Reference(s): <br>
- [las_video_edit API Reference](references/api.md) <br>
- [Volcengine LAS Pricing Reference](references/prices.md) <br>
- [Volcengine las_video_edit API Documentation](https://www.volcengine.com/docs/6492/2221469?lang=zh) <br>
- [Volcengine LAS Pricing](https://www.volcengine.com/docs/6492/1544808) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes cost estimates, user confirmation checkpoints, task IDs, clip metadata, TOS or local output paths, download links, and a billing disclaimer.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
