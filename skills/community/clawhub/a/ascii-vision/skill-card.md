## Description: <br>
Fallback image viewer when vision models are unavailable. Converts images to ASCII art via ffmpeg and Python for brightness distribution, texture analysis, edge detection, and color sampling without any vision API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chdlc](https://clawhub.ai/user/chdlc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when a vision model is unavailable or unsuitable and they need a local, text-based inspection of image brightness, structure, texture, edges, or coarse color samples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local image-processing commands against user-selected files. <br>
Mitigation: Use trusted local installations of ffmpeg and Python, verify target image paths before running commands, and avoid broad wildcards in private folders unless all matching files are intended for processing. <br>
Risk: ASCII and sampled-color output can support quick visual diagnosis but does not provide semantic image understanding. <br>
Mitigation: Use the output as a fallback for structure, brightness, texture, and coarse color checks; prefer a real vision model when semantic object, text, face, or scene interpretation is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chdlc/ascii-vision) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and plain-text ASCII analysis output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local ffmpeg and python3; outputs ASCII renderings, brightness statistics, edge counts, and RGB hex samples depending on the command used.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
