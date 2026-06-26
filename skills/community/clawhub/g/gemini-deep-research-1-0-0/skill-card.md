## Description: <br>
Perform complex, long-running research tasks using Gemini Deep Research Agent for multi-source synthesis, competitive analysis, market research, and comprehensive technical investigations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lion504](https://clawhub.ai/user/Lion504) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and research-focused agents use this skill to run Gemini Deep Research jobs that break down complex topics, search the web, and synthesize findings into reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research prompts and referenced context are sent to Google's Gemini service. <br>
Mitigation: Do not include confidential documents or sensitive personal data unless the applicable Google API terms and retention settings are acceptable. <br>
Risk: Generated markdown and JSON outputs may contain sensitive research context. <br>
Mitigation: Store, share, and delete saved output files according to the sensitivity of the submitted research request and returned report. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Lion504/gemini-deep-research-1-0-0) <br>
- [Google AI Studio API key](https://aistudio.google.com/apikey) <br>
- [Gemini Generative Language API](https://generativelanguage.googleapis.com/v1beta) <br>
- [Gemini interactions endpoint](https://generativelanguage.googleapis.com/v1beta/interactions) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown report, JSON interaction metadata, and terminal progress output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves timestamped markdown and JSON files locally; long-running jobs may take minutes to hours.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
