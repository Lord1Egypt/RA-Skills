## Description:

Gemini CLI tool for building, debugging & deploying with AI. Use when querying codebases, generating apps from images/PDFs, automating workflows, or performing AI-powered code tasks from the command line.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bigbubbaagent-bot](https://clawhub.ai/user/bigbubbaagent-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to install and operate Gemini CLI from an agent session for codebase analysis, code generation from images or PDFs, debugging, and workflow automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Gemini CLI workflows can send selected local code, images, and PDFs to Google's Gemini service.

Mitigation: Use only on data approved for external AI processing, and avoid proprietary, regulated, client, or secret-bearing files unless organizational policy allows that transfer.

Risk: Batch analysis can submit unintended files when run across broad or untrusted directories.

Mitigation: Review input directories and file selections before running batch-analyze.sh, and run it only on trusted paths.

Risk: API keys can be exposed if passed directly on the command line or stored in insecure shell profiles.

Mitigation: Prefer a session-scoped GEMINI_API_KEY environment variable, avoid command-line key arguments, and never commit keys to repositories.

Risk: Generated outputs may be written to unexpected or sensitive locations when save or output paths are misconfigured.

Mitigation: Review output paths before using --save, --output, or helper scripts that create result files.

## Reference(s):

- [ClawHub Gemini CLI Skill](https://clawhub.ai/bigbubbaagent-bot/skills/gemini-cli)
- [Gemini CLI Command Reference](references/commands.md)
- [Gemini CLI Usage Examples](references/examples.md)
- [Google AI Studio API Keys](https://aistudio.google.com/app/apikey)
- [Gemini CLI Documentation](https://geminicli.com/docs)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and file outputs from Gemini CLI workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GEMINI_API_KEY, local gemini and node binaries, internet access, and available Google API quota.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
