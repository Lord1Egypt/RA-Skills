## Description: <br>
BibiGPT CLI for summarizing videos, audio, and podcasts directly in the terminal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JimmyLv](https://clawhub.ai/user/JimmyLv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to summarize YouTube, Bilibili, podcast, audio, and other BibiGPT-supported URLs from a terminal. It also helps check BibiGPT authentication status and choose Markdown, transcript, chapter, or JSON output modes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The BibiGPT app or API may receive submitted URLs, transcripts, media metadata, and account or API-token access. <br>
Mitigation: Install only from trusted BibiGPT package sources and avoid submitting private or internal links unless sharing them with BibiGPT is allowed. <br>
Risk: Summarization depends on a local BibiGPT installation, active login session, or BIBI_API_TOKEN value. <br>
Mitigation: Check authentication with the documented CLI command before use and keep tokens out of shared shell history, logs, and generated artifacts. <br>


## Reference(s): <br>
- [BibiGPT desktop download](https://bibigpt.co/download/desktop) <br>
- [BibiGPT pricing](https://bibigpt.co/pricing) <br>
- [ClawHub skill page](https://clawhub.ai/JimmyLv/bibigpt-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown, JSON] <br>
**Output Format:** [Markdown guidance with shell command examples; BibiGPT CLI output may be Markdown text, subtitles, chapter summaries, or pretty-printed JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Progress is sent to stderr by the BibiGPT CLI; successful command output is sent to stdout.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
