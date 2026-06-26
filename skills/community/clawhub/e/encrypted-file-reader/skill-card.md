## Description: <br>
Reads local text, Word, and Excel files that the user is already authorized to access, including files in protected enterprise environments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[endcy](https://clawhub.ai/user/endcy) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and AI agents use this skill to read explicitly named local files and return their contents for analysis, summarization, or follow-up work. It is intended for files the user can already access through authorized local applications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local files read by the helper may be exposed to the AI session output. <br>
Mitigation: Use the skill only with explicitly named files whose contents are appropriate to share in the current AI/tool context. <br>
Risk: Credentials, secrets, private business documents, or broad filesystem paths could disclose sensitive information if selected. <br>
Mitigation: Avoid using the skill on secrets or sensitive private documents unless the user has confirmed that disclosure into the session is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/endcy/encrypted-file-reader) <br>
- [Publisher profile](https://clawhub.ai/user/endcy) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text file contents on stdout or error text on stderr.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The caller provides a local file path; supported inputs include text files, .docx, and .xlsx files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
