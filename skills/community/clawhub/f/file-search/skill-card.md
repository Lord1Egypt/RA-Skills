## Description: <br>
Fast file-name and content search using `fd` and `rg` (ripgrep). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Xejrax](https://clawhub.ai/user/Xejrax) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to quickly locate files by name and search file contents with standard local command-line tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search results may reveal matching filenames or file contents from directories that contain secrets, credentials, private documents, or customer data. <br>
Mitigation: Use the skill only on directories intentionally selected for search, and avoid broad searches over sensitive folders unless that exposure is acceptable. <br>
Risk: The skill depends on local `fd` and `rg` binaries being installed from trusted sources. <br>
Mitigation: Install `fd-find` and `ripgrep` from trusted operating system repositories before using the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Xejrax/file-search) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/Xejrax) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local `fd` and `rg` binaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
