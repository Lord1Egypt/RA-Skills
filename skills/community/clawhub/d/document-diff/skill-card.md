## Description: <br>
Compares two documents by parsing them with SoMark into Markdown, then producing structured reports of added, removed, and changed content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[soul-code](https://clawhub.ai/user/soul-code) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and document reviewers use this skill to compare versions of contracts, reports, policies, or manuals and summarize significant content changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Compared documents are uploaded to SoMark for parsing. <br>
Mitigation: Use the skill only with documents that the user is permitted to send to SoMark, and avoid highly confidential, regulated, or client-restricted files unless that transfer is approved. <br>
Risk: The skill requires a SoMark API key. <br>
Mitigation: Keep SOMARK_API_KEY in the environment and do not paste the credential into chat or commit it to files. <br>
Risk: Parsed Markdown and diff outputs are saved locally in the configured output directory. <br>
Mitigation: Choose an appropriate output directory and review or remove generated files when they contain sensitive document content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/soul-code/document-diff) <br>
- [SoMark API base](https://somark.tech/api/v1) <br>
- [SoMark API key setup](https://somark.tech/login) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON summaries, parsed Markdown files, and human-facing guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes parsed Markdown for each input document, a diff_report.md file, and a diff_summary.json file to the selected output directory.] <br>

## Skill Version(s): <br>
0.1.2 (source: release evidence and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
