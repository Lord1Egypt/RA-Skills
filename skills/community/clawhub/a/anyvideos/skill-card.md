## Description: <br>
Download videos, images, and audio from YouTube, Twitter, Instagram, Facebook, Vimeo, Tumblr, TikTok, Bilibili, and 1000+ more websites. Just paste a URL and get direct download links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mstscmsn](https://clawhub.ai/user/mstscmsn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to request media download options from the AnyVideos API, choose a quality, and save or deliver the resulting video, image, or audio file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Media URLs submitted to the AnyVideos service may reveal private, signed, internal, or account-specific content, and API usage may consume credits or quota. <br>
Mitigation: Avoid submitting sensitive URLs and confirm the API key, remaining balance, and intended request before extracting media. <br>
Risk: Local install and download commands such as ffmpeg, curl, or wget can affect the local environment or overwrite files. <br>
Mitigation: Review commands before running them, choose output paths deliberately, and check whether a target file already exists before writing. <br>
Risk: Some sources may be unsupported, temporarily unavailable, or too large to send directly in chat. <br>
Mitigation: Validate the URL, present available quality and size information, warn before large downloads, and provide a saved path or direct link fallback when delivery is not practical. <br>


## Reference(s): <br>
- [AnyVideos](https://anyvideos.yx.lu) <br>
- [AnyVideos Extract API](https://anyvideos.yx.lu/api/extract) <br>
- [ClawHub Skill Page](https://clawhub.ai/mstscmsn/anyvideos) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown responses with quality tables, API request details, shell commands, direct download links, and saved file paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ANYVIDEOS_API_KEY and may use ffmpeg, curl, or wget to download and merge media files.] <br>

## Skill Version(s): <br>
1.0.4 (source: ClawHub release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
