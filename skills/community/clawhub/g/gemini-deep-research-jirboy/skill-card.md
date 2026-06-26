## Description: <br>
Compatibility skill for Gemini Deep Research that accepts a research topic, calls Gemini's deep research API, and saves synthesized Markdown and JSON reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jirboy](https://clawhub.ai/user/jirboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run multi-step research on a supplied topic, synthesize web findings, and produce reusable research reports. It is also retained as a compatibility entry point for workflows moving to the unified research skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research prompts, formatting instructions, and optional Gemini file-search-store context are sent to Google. <br>
Mitigation: Use only when sharing that context with Google is acceptable, prefer GEMINI_API_KEY from the environment, and avoid including sensitive data in prompts or selected file-search stores. <br>
Risk: Generated Markdown and JSON reports may contain sensitive research topics or source context on disk. <br>
Mitigation: Choose an appropriate output directory and delete generated report and metadata files when the topic is sensitive. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jirboy/gemini-deep-research-jirboy) <br>
- [Google Generative Language API v1beta endpoint](https://generativelanguage.googleapis.com/v1beta) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands] <br>
**Output Format:** [Markdown report, JSON interaction metadata, and terminal progress text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes timestamped deep-research Markdown and JSON files to the selected output directory.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
