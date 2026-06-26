## Description: <br>
Extracts hyperlinks from every tab of a public Feishu spreadsheet and can optionally download linked articles as Markdown files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangyan9110](https://clawhub.ai/user/wangyan9110) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when they need to collect links from public Feishu spreadsheets, summarize the extracted links by sheet, and optionally archive linked article content as Markdown. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can reuse an existing Chrome remote-debugging session, which may expose logged-in browser context. <br>
Mitigation: Use it only with Feishu documents and extracted links you trust, and avoid running it while a logged-in Chrome debugging session is open unless that is intentional. <br>
Risk: Batch download opens extracted URLs in Chrome and writes article content to a local output folder. <br>
Mitigation: Review extracted URLs before downloading and choose a low-risk output directory. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wangyan9110/feishu-sheet-links) <br>
- [Bun runtime](https://bun.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, a JSON link inventory, and optional Markdown article files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Extraction output groups links by sheet name; optional article downloads support resume.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
