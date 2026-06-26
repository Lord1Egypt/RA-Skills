## Description: <br>
FFmpeg operations via the ffmpeg-static npm package (bundled binary) with automatic fallback to a native system FFmpeg installation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fantox](https://clawhub.ai/user/fantox) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to resolve ffmpeg-static or system FFmpeg binaries and prepare FFmpeg or ffprobe commands, Node.js integration patterns, and configuration guidance for media transcoding, conversion, thumbnail extraction, streaming, and inspection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The ffmpeg-static npm package downloads a prebuilt FFmpeg binary during npm install. <br>
Mitigation: Install only when the package and binary source are acceptable for the environment, or use a trusted system FFmpeg binary. <br>
Risk: FFmpeg commands can overwrite existing files when examples use -y. <br>
Mitigation: Use fresh output paths or replace -y with -n when existing files must be preserved. <br>
Risk: Untrusted filenames or URLs passed to FFmpeg can expose arbitrary protocol or file access behavior. <br>
Mitigation: Validate paths, URLs, and media types before passing them to FFmpeg or ffprobe. <br>


## Reference(s): <br>
- [ClawHub ffmpeg-static release page](https://clawhub.ai/fantox/ffmpeg-static) <br>
- [ffmpeg-static package homepage](https://github.com/eugeneware/ffmpeg-static) <br>
- [npm package: ffmpeg-static](https://www.npmjs.com/package/ffmpeg-static) <br>
- [FFmpeg Static API Reference](references/api_reference.md) <br>
- [FFmpeg CLI documentation](https://ffmpeg.org/ffmpeg.html) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with inline bash and JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes copy-paste FFmpeg command templates, Node.js spawn patterns, binary resolution guidance, and ffprobe inspection examples.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
