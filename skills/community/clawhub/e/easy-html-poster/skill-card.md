## Description: <br>
Davos helps agents create HTML-based poster templates for Chinese social posts and capture them with a browser screenshot workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhsongchao](https://clawhub.ai/user/zhsongchao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, marketers, and agents assisting them use this skill to draft vertical HTML poster templates for agriculture, legal, warning, or social-sharing messages, then capture the result in a browser. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Temporary HTML files or screenshots can be mixed with unrelated desktop files or overwrite existing work. <br>
Mitigation: Create posters in a dedicated temporary folder, use explicit filenames, and remove temporary files after capture. <br>
Risk: A local HTTP server can expose files if it serves a broad directory or is left running. <br>
Mitigation: Serve only the poster folder, bind the server to 127.0.0.1, and stop it immediately after screenshotting. <br>
Risk: Generated poster content may be inaccurate, sensitive, or unsuitable for public sharing. <br>
Mitigation: Review the rendered poster and screenshot before publishing or sending it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhsongchao/easy-html-poster) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with HTML/CSS snippets and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local poster files and screenshot workflow guidance; no API calls are required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
