## Description: <br>
Automates EPUB book processing by extracting text, cover art, summaries, framework analysis, and optional study assets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ntsnail](https://clawhub.ai/user/ntsnail) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and productivity-focused readers use this skill to turn EPUB uploads into a local folder of extracted text, summaries, quality reports, and optional study materials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The processing script can request administrator-level package installation when jq is missing. <br>
Mitigation: Preinstall jq, python3, and unzip before use, and decline unexpected sudo prompts during skill execution. <br>
Risk: The skill is designed to run automatically when an EPUB file is received, which can blur execution boundaries. <br>
Mitigation: Use it only with EPUB files the user intentionally provides and review the generated file list before relying on outputs. <br>
Risk: Failed or interrupted runs can leave temporary EPUB extraction folders under /tmp. <br>
Mitigation: Check for and remove leftover /tmp/epub_extracted_* folders after failed processing. <br>
Risk: Image-heavy, encrypted, or malformed EPUBs may produce little usable text or incomplete summaries. <br>
Mitigation: Review the generated quality report and manually supplement summary or framework files when automatic extraction is insufficient. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ntsnail/book-processor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Generated local files including .txt, .md, .mmd, .json, and a brief processing summary.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires jq, python3, and unzip; can use process_config.json to enable optional generated assets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
