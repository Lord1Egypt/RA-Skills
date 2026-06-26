## Description: <br>
Rename audio files with Chinese/special characters to simple English names for mlx-stt compatibility. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ayakolin](https://clawhub.ai/user/ayakolin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and audio transcription users use this skill to rename local audio files with non-ASCII or special-character filenames before passing them to tools such as mlx-stt. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Batch mode or broad filename-fix prompts can rename more local audio files than intended. <br>
Mitigation: Verify the exact file or directory path before execution, especially when using --all, and run on a copied folder when preservation of original filenames matters. <br>


## Reference(s): <br>
- [Audio Rename on ClawHub](https://clawhub.ai/ayakolin/audio-rename) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, code, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Renames local files in place and prints the resulting filename and location.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
