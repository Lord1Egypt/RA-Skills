## Description: <br>
BettaFish Opinion Analysis coordinates web search, media review, sentiment analysis, and report generation to produce social-media opinion analysis reports for brands, events, competitors, policies, and public topics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liyico](https://clawhub.ai/user/liyico) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external analysts, and communications teams use this skill to investigate public opinion, sentiment, reputation risk, and competitive perception, then package findings into formal Word/PDF documents and interactive HTML reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Analysis topics and gathered material may be sent to external search, fetch, browser, curl, or API destinations. <br>
Mitigation: Use only authorized, non-confidential investigations unless data-sharing approval and source-review controls are in place. <br>
Risk: The skill can download media and create shareable Word, PDF, and HTML reports on disk. <br>
Mitigation: Set an approved output directory, review generated reports before sharing, and define retention and cleanup steps for downloaded media and report files. <br>
Risk: Bundled document/PDF/video tooling includes command-line helpers and a LibreOffice shim that may compile and preload native code from /tmp. <br>
Mitigation: Run in a sandboxed environment, review or disable the LibreOffice shim before sensitive use, and install only after security review. <br>


## Reference(s): <br>
- [Bettafish Opinion Analysis on ClawHub](https://clawhub.ai/liyico/bettafish-opinion-analysis) <br>
- [Publisher profile](https://clawhub.ai/user/liyico) <br>
- [Data Sources Guide](references/data_sources.md) <br>
- [Design Guide](references/design_guide.md) <br>
- [Sentiment Guide](references/sentiment_guide.md) <br>
- [FFmpeg](https://ffmpeg.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Word/PDF documents, interactive HTML reports, Markdown guidance, Python code, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are expected to include analysis prose, tables, source lists, charts, and visualizations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
