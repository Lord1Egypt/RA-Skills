## Description: <br>
Polish a technical blog draft into a 1000-1200 word, 4-5 section en-US article, preserve technical terms and code, and generate consistent hero and per-section image prompts when the user asks to polish and translate a blog with images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[j3ffyang](https://clawhub.ai/user/j3ffyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical writers, and blog authors use this skill to turn a technical draft into a polished en-US article while keeping technical meaning intact. It also prepares a consistent image prompt package for a hero image and each section. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence flags broad unsandboxed execution and possible automatic involvement of reviewer tools. <br>
Mitigation: Install only from a trusted maintainer workflow, prefer `--no-yolo` or `AUTOREVIEW_YOLO=0`, and disable automatic fallback reviewers for private diffs. <br>
Risk: Auto-run test or static-check behavior can act on repository content during review workflows. <br>
Mitigation: Review any auto-run test or static-check behavior before use and run the skill in a controlled workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/j3ffyang/blog-polish-enus-images) <br>
- [Publisher profile](https://clawhub.ai/user/j3ffyang) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Files, Guidance] <br>
**Output Format:** [Structured JSON with output paths plus polished Markdown and single-line image prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns polishedPath, imagePaths, and imagePrompts; may save files under the configured output directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
