## Description: <br>
Content News Thai generates 1080x1350 news-style social media images with Thai text overlays and matching captions for Facebook and Instagram. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mewic](https://clawhub.ai/user/mewic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, marketers, and agent users use this skill to create Thai news-style post images and short captions from headline, subheadline, background, source, and brand inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup installs system packages, npm dependencies, and Thai font files. <br>
Mitigation: Run setup deliberately in a trusted project or container and review the dependency installation before use. <br>
Risk: The generator can load remote background-image URLs and write image files to caller-specified paths. <br>
Mitigation: Use trusted background-image URLs and safe output paths such as a workspace file or /tmp image file. <br>


## Reference(s): <br>
- [Content News Thai on ClawHub](https://clawhub.ai/mewic/content-news-thai) <br>
- [Kanit Bold font source](https://github.com/google/fonts/raw/main/ofl/kanit/Kanit-Bold.ttf) <br>
- [Kanit Light font source](https://github.com/google/fonts/raw/main/ofl/kanit/Kanit-Light.ttf) <br>
- [Sarabun SemiBold font source](https://github.com/google/fonts/raw/main/ofl/sarabun/Sarabun-SemiBold.ttf) <br>
- [Prompt Bold font source](https://github.com/google/fonts/raw/main/ofl/prompt/Prompt-Bold.ttf) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Markdown, Shell commands, Guidance] <br>
**Output Format:** [JSON command output, JPEG image file, and Markdown caption text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates 1080x1350 JPG images; accepts optional background image paths or URLs and writes to a caller-provided output path or workspace default.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence, scripts/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
