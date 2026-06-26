## Description: <br>
Automatically clean disk space by removing temp files, browser cache, recycle bin or trash contents, and log files on Windows, Linux, and macOS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ahqazi-dev](https://clawhub.ai/user/ahqazi-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to free local disk space by running or being guided through OS-specific cleanup of temporary files, browser caches, trash, and logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can delete broad local cache, log, trash, and system-managed folders. <br>
Mitigation: Use Confirm Mode, review each target path before approval, and avoid running the skill as administrator or root. <br>
Risk: The scripts do not fully enforce the stated safe-cleaning and older-than-one-day promises. <br>
Mitigation: Do not rely on age-based protection claims; back up important data and skip any cleanup target whose contents are unclear. <br>


## Reference(s): <br>
- [Windows Disk Cleaner](artifact/windows-cleaner.md) <br>
- [Linux Disk Cleaner](artifact/linux-cleaner.md) <br>
- [macOS Disk Cleaner](artifact/mac-cleaner.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with Python code and shell execution steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include interactive confirmation prompts and a cleanup summary showing categories cleaned, skipped items, and reported space freed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
