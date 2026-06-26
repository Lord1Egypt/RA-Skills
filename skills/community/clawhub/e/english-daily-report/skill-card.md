## Description: <br>
Generates daily English learning reports with news summaries, Chinese translations, vocabulary notes, PDF files, and audio versions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaofangzheng](https://clawhub.ai/user/zhaofangzheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
English learners and instructors use this skill to create daily study material from current news or clearly labeled fallback study passages. The skill supports bilingual reading practice, vocabulary review, printable PDF output, and MP3 listening practice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may contact news sites, search services, and a TTS provider, optionally using a Brave API key. <br>
Mitigation: Use only approved services, provide secrets through the intended configuration path, and review fetched sources before sharing generated reports. <br>
Risk: The skill runs local Chrome or Chromium to render PDFs and writes generated files to the workspace uploads directory. <br>
Mitigation: Install Chrome or Chromium from a trusted source, review the bundled PDF script before first use, and inspect generated files before sending them externally. <br>
Risk: Fallback study material could be mistaken for real news if labels are removed. <br>
Mitigation: Keep the report's Real News or Study Material labels and source links visible in text, PDF, and audio workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhaofangzheng/english-daily-report) <br>
- [Example English Daily Report](references/example-report.md) <br>
- [Google Chrome](https://www.google.com/chrome/) <br>
- [Brave Search API](https://brave.com/search/api/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Configuration, Guidance] <br>
**Output Format:** [Markdown text plus generated PDF and MP3 files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates uploads/english-daily-DATE.pdf and uploads/english-daily-DATE.mp3 when dependencies are available.] <br>

## Skill Version(s): <br>
1.2.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
