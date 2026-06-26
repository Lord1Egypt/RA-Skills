## Description: <br>
Processes blog content to extract embedded videos and generate lightweight GIF previews for quick scanning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content workflows use this skill to process blog or RSS feeds, extract embedded video URLs, and generate GIF previews for quick scanning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Untrusted feeds or media files can expose media-processing steps to malformed or oversized inputs. <br>
Mitigation: Use feeds and videos you trust, and apply size limits, time limits, and sandboxing where possible. <br>
Risk: The artifact does not include the executable implementation file referenced by package.json. <br>
Mitigation: If installing as an npm package, verify the missing implementation file, dependency versions, and source provenance first. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/blog-content-proc) <br>


## Skill Output: <br>
**Output Type(s):** [text, files, guidance] <br>
**Output Format:** [Markdown guidance with extracted video URLs and generated GIF preview file paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May rely on RSS parsing and ffmpeg-based media processing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
