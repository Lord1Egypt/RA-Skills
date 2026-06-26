## Description: <br>
Monitors Canvas course announcements and assignments, downloads course files, and helps generate Markdown study notes and PDFs with Chinese and math support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huaruoji](https://clawhub.ai/user/huaruoji) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Learners using Canvas use this skill to check course updates, collect course files, and create study notes or mock tests that can be exported to PDF. It is intended for local study workflows where the user configures their institution's Canvas domain and course IDs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow stores a live Canvas login session locally. <br>
Mitigation: Use an official Canvas API token or OAuth when available; otherwise keep the session cookie short-lived and restrict ~/.canvas_cookie permissions to 0600. <br>
Risk: Canvas requests depend on user-supplied institution domains and course IDs. <br>
Mitigation: Verify the Canvas domain and course IDs before running the scripts so requests are sent only to the intended institution. <br>
Risk: The Canvas cookie file is sourced by shell scripts. <br>
Mitigation: Treat ~/.canvas_cookie as sensitive data, do not share it, and prefer parsing cookie values as data instead of sourcing the file. <br>
Risk: The optional remote-debugging browser workflow can expose an authenticated browser session while it is running. <br>
Mitigation: Stop the debugging browser after use and avoid leaving the remote debugging port open. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/huaruoji/canvas-study-helper) <br>
- [Publisher profile](https://clawhub.ai/user/huaruoji) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown templates, bash commands, terminal summaries, downloaded course files, and PDF documents] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local Canvas domain and course ID configuration, a Canvas login session cookie, and tools such as curl, jq, python3, pandoc, and XeLaTeX.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
