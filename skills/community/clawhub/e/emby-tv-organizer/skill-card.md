## Description: <br>
Helps organize TV-series folders for Emby by scanning media files, proposing Emby-compatible names and season folders, preserving episode titles when detected, and generating an Excel rename table after user confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[851032763](https://clawhub.ai/user/851032763) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and media-library operators use this skill to review and apply Emby-compatible TV episode organization plans, including season and episode detection, special-episode handling, subtitle matching, and Excel audit output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Excel helper can install the openpyxl Python package during normal use if it is missing. <br>
Mitigation: Install a trusted, pinned openpyxl dependency through the normal environment setup before using the Excel feature. <br>
Risk: The skill proposes file move and rename operations that could affect a media library if approved without review. <br>
Mitigation: Review the generated rename plan carefully before approving file operations; the skill is designed to preview first and avoid overwriting existing targets. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/851032763/emby-tv-organizer) <br>
- [Episode Pattern Reference](references/episode_patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown plans and tables with optional JSON input for an Excel-generation script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill is designed to preview proposed file moves and renames before execution and to produce an Excel comparison table after confirmation.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
