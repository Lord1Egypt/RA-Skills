## Description: <br>
Use this skill when the user wants to install, run, or troubleshoot the published `deyo` transcription CLI, including one-time API key login, output file selection, source selection, and user-visible progress updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[casatwy](https://clawhub.ai/user/casatwy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agent users use Deyo to install or configure the published transcription CLI, authenticate with a Deyo API key, transcribe supported links, choose output formats and files, and receive concise progress updates during longer runs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install or upgrade the third-party @casatwy/deyo npm package and use the Deyo service. <br>
Mitigation: Install only when the user trusts the Deyo service and npm package, and surface installation failures instead of silently working around them. <br>
Risk: The skill stores a Deyo API key locally for future CLI use. <br>
Mitigation: Check auth status first, reveal only the last four characters of an existing key, and ask before replacing stored credentials. <br>
Risk: Transcription links and related content are sent to Deyo for processing. <br>
Mitigation: Confirm the target URL and use the CLI defaults unless the user explicitly requests source, language, format, or output-file changes. <br>


## Reference(s): <br>
- [Deyo Skill Release Page](https://clawhub.ai/casatwy/deyo) <br>
- [Deyo API Keys](https://deyo.miaobi.fun/me/api-keys) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Text, Markdown, Files] <br>
**Output Format:** [Markdown or plain text with inline shell commands; CLI progress can be parsed from JSONL on stderr.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce transcript text on stdout or transcript files in text, SRT, VTT, or JSON formats.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
