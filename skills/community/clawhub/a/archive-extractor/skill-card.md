## Description: <br>
Recursively extracts archive files from a file or directory, including nested zip, tar, gzip, bzip2, xz, rar, and 7z archives. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiliangzhao20241028](https://clawhub.ai/user/qiliangzhao20241028) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations users use this skill to run a Python extractor over archive files or directories for bulk, nested, and repeatable decompression workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can silently run pip to install Python packages for optional archive formats. <br>
Mitigation: Review before installing, use an isolated environment, remove auto-install behavior if needed, or preinstall required dependencies yourself. <br>
Risk: Recursive extraction of untrusted archives can create operational risk without disk and recursion controls. <br>
Mitigation: Use a dedicated extraction directory and avoid running on untrusted archives unless disk usage and recursion limits are enforced. <br>


## Reference(s): <br>
- [ClawHub archive-extractor package](https://clawhub.ai/qiliangzhao20241028/archive-extractor) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and filesystem extraction results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create extracted directories, .extracted_success markers, and log output while processing archives recursively.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
