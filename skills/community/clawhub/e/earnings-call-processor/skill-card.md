## Description: <br>
Transcribe earnings call audio via Whisper, analyze stock price data, and generate structured Feishu documents summarizing financial results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and finance analysts use this skill to turn earnings call audio and stock history CSV data into a transcript, computed financial indicators, and Feishu-ready summary content for review and publication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes selected earnings call audio and stock CSV data on the local machine. <br>
Mitigation: Use trusted local input files, run the skill in a dedicated output directory, and avoid placing sensitive recordings or market data in shared paths. <br>
Risk: Generated Feishu-ready content may contain transcription errors or misleading financial summaries. <br>
Mitigation: Review the transcript, computed indicators, and generated Feishu content before sharing or publishing. <br>
Risk: The pipeline depends on local Whisper and pandas installations. <br>
Mitigation: Install dependencies from trusted sources and verify the local environment before processing earnings call material. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/earnings-call-processor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Local files containing a transcript, financial indicators JSON, and Feishu-ready Markdown content.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-selected audio and stock CSV inputs plus local Whisper and pandas installations.] <br>

## Skill Version(s): <br>
3.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
