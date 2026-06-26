## Description: <br>
Runs a Gemini CLI deep research workflow to generate market, industry, or technical research reports from a user-provided topic. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skywalker-lili](https://clawhub.ai/user/skywalker-lili) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and operators use this skill to send a research topic to the Gemini Deep Research MCP extension, choose a report format, and save a Markdown report for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research topics, filters, and report options are sent to an external report provider. <br>
Mitigation: Avoid confidential, regulated, or proprietary topics unless approved for that provider. <br>
Risk: The helper can save generated Markdown reports to a user-selected path. <br>
Mitigation: Review the destination path before running the workflow and inspect the report before relying on it. <br>


## Reference(s): <br>
- [Gemini Deep Research Setup Guide](references/setup-guide.md) <br>
- [gemini-cli-deep-research Extension](https://github.com/allenhutchison/gemini-cli-deep-research) <br>
- [Google AI Studio API Keys](https://aistudio.google.com/apikey) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown report file with JSON status from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Gemini CLI, the gemini-deep-research extension, Node.js 18+, and a paid Google AI API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
