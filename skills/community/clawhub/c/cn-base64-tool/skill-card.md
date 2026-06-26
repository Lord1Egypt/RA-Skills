## Description: <br>
Cn Base64 Tool provides a pure Python standard-library helper for Base64 encoding and decoding strings and files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when they need local Base64 encoding or decoding for strings and files without external dependencies or API keys. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: File conversion commands read from and write to paths selected by the user, and decode_file can overwrite the output path provided. <br>
Mitigation: Run it only on intentionally selected files, choose output paths deliberately, and avoid targeting files that must be preserved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freedompixels/cn-base64-tool) <br>
- [Publisher profile](https://clawhub.ai/user/freedompixels) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and plain text Base64 output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read user-selected input files and write Base64-decoded content to a user-selected output path.] <br>

## Skill Version(s): <br>
1.2.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
