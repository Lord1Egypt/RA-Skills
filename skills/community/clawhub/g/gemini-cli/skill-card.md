## Description: <br>
Gemini CLI tool for building, debugging and deploying with AI from the command line. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bigbubbaagent-bot](https://clawhub.ai/user/bigbubbaagent-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to query codebases, generate code or documentation from images and PDFs, automate AI-assisted workflows, and run Gemini-powered debugging or code review from a terminal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected files and prompts may be sent to Google's Gemini service. <br>
Mitigation: Run Gemini commands only on intended directories and avoid including secrets, customer data, or regulated content in prompts or context. <br>
Risk: API keys may be exposed if placed directly on command lines or stored in synced shell profiles. <br>
Mitigation: Use a scoped Gemini API key through a local environment variable and avoid committing or syncing shell files that contain credentials. <br>
Risk: Batch or context commands can process more files than intended. <br>
Mitigation: Review input paths before running batch workflows and narrow command scope to the files required for the task. <br>


## Reference(s): <br>
- [Gemini CLI Command Reference](references/commands.md) <br>
- [Gemini CLI Usage Examples](references/examples.md) <br>
- [Gemini API Key](https://aistudio.google.com/app/apikey) <br>
- [Gemini CLI Documentation](https://geminicli.com/docs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands and generated text or code files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on selected Gemini CLI commands, local file context, Google service availability, and API quota limits.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
