## Description: <br>
Use when a Codex thread or local session is slow because prior turns contain heavy image, screenshot, or base64 payloads. Helps locate the session JSONL, back it up, remove only embedded image blobs, preserve conversation text, and validate the cleaned file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vyctorbrzezowski](https://clawhub.ai/user/vyctorbrzezowski) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Codex users use this skill to shrink local Codex session logs that contain large embedded image or base64 payloads while preserving conversation text and structure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can inspect and modify local Codex session JSONL files, which may contain sensitive conversation data. <br>
Mitigation: Run the scrubber in dry-run mode first, confirm the target file and expected size reduction, and keep the backup until the cleaned session opens correctly. <br>
Risk: Choosing the wrong session file could remove image payloads from an unintended local history file. <br>
Mitigation: Identify the target by thread id or exact file path, stop if multiple files match, and review the reported backup path and validation results after writing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/vyctorbrzezowski/codex-session-image-scrubber) <br>
- [Server-resolved GitHub Source](https://github.com/vyctorbrzezowski/skills) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, text] <br>
**Output Format:** [Markdown with inline shell commands and JSON status output from the scrubber] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run is the default; write mode creates a backup and reports size, replacement, and parse statistics.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
