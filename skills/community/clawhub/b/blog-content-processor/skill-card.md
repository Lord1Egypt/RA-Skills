## Description: <br>
Process blog content to extract videos and generate GIF previews. Works with blogwatcher, video-frames, and gifgrep skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content automation teams use this skill to process RSS or Atom blog feeds, extract embedded video URLs, and generate GIF preview clips for downstream workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ClawHub security evidence reports no harmful scanner or telemetry findings, but notes limited artifact-backed review depth. <br>
Mitigation: Review the skill contents, declared dependencies, and requested permissions before installing or running it. <br>
Risk: The skill processes RSS feeds, embedded video URLs, and media files, which can expose agents to untrusted external content. <br>
Mitigation: Run the workflow in a sandboxed environment, prefer trusted feeds, and keep media-processing dependencies patched. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/terrycarter1985/blog-content-processor) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with bash commands and generated GIF preview files when executed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes feed URLs and writes GIF previews to a configured output directory.] <br>

## Skill Version(s): <br>
10.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
