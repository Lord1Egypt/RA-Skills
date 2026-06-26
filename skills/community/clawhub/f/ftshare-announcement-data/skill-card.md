## Description: <br>
Queries A-share announcement and research-report data for market-wide dates or individual stocks, and can download announcement or report PDFs by url_hash from market.ft.tech. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Shawn92](https://clawhub.ai/user/Shawn92) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve A-share announcement or research-report listings by date or stock code, then download selected PDFs when a url_hash is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the skill executes included Python scripts that contact market.ft.tech and may save PDFs locally. <br>
Mitigation: Use only documented subskills, review requested downloads before execution, and choose output filenames deliberately. <br>
Risk: A requested PDF output filename could overwrite an existing file in the skill working directory. <br>
Mitigation: Use unique output filenames and verify the destination before downloading. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Shawn92/ftshare-announcement-data) <br>
- [Publisher profile](https://clawhub.ai/user/Shawn92) <br>
- [market.ft.tech API host](https://market.ft.tech) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, files, guidance] <br>
**Output Format:** [JSON responses for listings and download status, with optional PDF files saved locally and agent-facing summaries in text or Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Network requests contact market.ft.tech; PDF downloads save to a chosen filename under the skill working directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
