## Description: <br>
Automates file uploads on web pages via agent-browser CLI or a Python script, supporting flexible file paths and optional file input selectors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weixizi](https://clawhub.ai/user/weixizi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to upload user-selected local files to web forms, either by emitting agent-browser commands or by running the bundled Python helper with a URL, path, optional selector, and wait time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploading a local file discloses that file to the destination website. <br>
Mitigation: Use the skill only with trusted sites after verifying the destination domain, selector, and resolved full file path; avoid uploading secrets, credentials, private documents, or unrelated workspace files unless the site is intended to receive them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/weixizi/browser-file-uploa) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and Python helper code.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May resolve local file paths and call agent-browser to upload a specified file to a specified web page.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
