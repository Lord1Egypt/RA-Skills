## Description: <br>
Extract plain-text transcripts from YouTube videos using a local Python script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hushenglang](https://clawhub.ai/user/hushenglang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to extract plain-text YouTube transcripts from video URLs or video IDs for downstream review, analysis, or summarization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence reports that the skill ships a YouTube/Google cookie file that appears to contain account session material. <br>
Mitigation: Remove the bundled cookie file before installation or use; require any cookie-based authentication to be explicitly user-provided, documented, and limited to the requested video, and revoke or rotate the likely affected Google/YouTube session. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hushenglang/extract-youtube-transcript) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text transcript output with Markdown usage guidance and shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can list available transcript languages and can write transcript text to a file when an output path is provided.] <br>

## Skill Version(s): <br>
2.1.0 (source: frontmatter and server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
