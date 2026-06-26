## Description: <br>
Perform complex, long-running research tasks using Gemini Deep Research Agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arun-8687](https://clawhub.ai/user/arun-8687) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, researchers, and analysts use this skill to run long-running Gemini Deep Research jobs for multi-source synthesis, competitive analysis, market research, and technical investigations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research prompts and optional file-search context are sent to Google through the Gemini API. <br>
Mitigation: Use only with data that may be shared with Google under the applicable terms, and avoid including sensitive file-search stores unless approved. <br>
Risk: Long-running research jobs may incur API costs or consume quota. <br>
Mitigation: Monitor Gemini API quota and costs before starting broad or repeated research jobs. <br>
Risk: Reports and interaction metadata may contain sensitive research content. <br>
Mitigation: Write outputs to a private directory and restrict access to generated Markdown and JSON files. <br>
Risk: Providing the API key as a command-line argument can expose it in shell history or process lists on shared systems. <br>
Mitigation: Prefer the GEMINI_API_KEY environment variable for credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/arun-8687/gemini-deep-research) <br>
- [Google AI Studio API keys](https://aistudio.google.com/apikey) <br>
- [Gemini interactions API endpoint](https://generativelanguage.googleapis.com/v1beta/interactions) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown report plus JSON interaction metadata; progress updates may stream to stderr.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves timestamped deep-research-YYYY-MM-DD-HH-MM-SS.md and .json files to the selected output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
