## Description: <br>
Executes Gemini Deep Research through the gemini-deep-research MCP extension for Gemini CLI, polls in the background, and saves completed reports locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skywalker-lili](https://clawhub.ai/user/skywalker-lili) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and analysts use this skill to start long-running Gemini Deep Research tasks for market, industry, geopolitical, investment, or technical research and save the resulting report as Markdown. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow sends research prompts to Gemini and may use paid API quota. <br>
Mitigation: Avoid sensitive topics unless approved for Gemini use, confirm billing expectations, and ensure the paid Google AI API key is intentionally configured. <br>
Risk: The setup guide installs a third-party Gemini Deep Research extension with auto-update behavior. <br>
Mitigation: Review or pin the extension before use instead of relying on automatic updates. <br>
Risk: Reports and logs are written locally and the polling process runs detached in the background. <br>
Mitigation: Choose the output path explicitly, track the background process, and stop or clean it up when the task is no longer needed. <br>


## Reference(s): <br>
- [Gemini Deep Research setup guide](references/setup-guide.md) <br>
- [gemini-cli-deep-research extension](https://github.com/allenhutchison/gemini-cli-deep-research) <br>
- [Google AI Studio API keys](https://aistudio.google.com/apikey) <br>
- [NotebookLM](https://notebooklm.google.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON status objects, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a user-selected report format, output path, polling interval, and maximum polling duration.] <br>

## Skill Version(s): <br>
1.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
