## Description: <br>
AI Short Video Factory creates MP4 videos from HTML using HyperFrames. Use for captioned talking-head edits, product launches, data visualizations, code walkthroughs, social clips, GSAP animations, transitions, audio muxing, and deterministic rendering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zrzqbr](https://clawhub.ai/user/zrzqbr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, developers, and marketing teams use this skill to turn text ideas, structured scripts, or existing talking-head media into short MP4 videos with HTML/CSS/GSAP animation, captions, audio processing, and HyperFrames rendering. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run npx/HyperFrames, download browser components, invoke FFmpeg, process local media, and consume significant CPU, disk, and bandwidth. <br>
Mitigation: Run video-production workflows in an isolated project or container, review commands before execution, and budget local storage and render time before starting. <br>
Risk: The scanner summary notes sandbox-bypass rendering guidance and a privileged repair command without enough user-facing caution. <br>
Mitigation: Manually approve any sandbox-disabled render or sudo command, and avoid privileged cache or permission repairs unless the exact path and need are clear. <br>
Risk: Long video audio can be incomplete if the workflow relies on built-in HyperFrames audio behavior. <br>
Mitigation: Use FFmpeg post-render audio muxing for long or narrated videos and verify final audio duration and tail audibility with the provided verification helper. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/zrzqbr/ai-short-video-factory) <br>
- [HyperFrames Animation Guide](references/animation-guide.md) <br>
- [HyperFrames Caption & Subtitle Patterns](references/caption-patterns.md) <br>
- [HyperFrames Composition Rules](references/composition-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with HTML/CSS/JavaScript snippets and shell commands; workflows may render MP4 media files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate or verify WAV/MP4 media through local HyperFrames, FFmpeg, and Python helper scripts.] <br>

## Skill Version(s): <br>
1.2.0 (source: evidence.release.version, SKILL.md frontmatter, CHANGELOG.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
