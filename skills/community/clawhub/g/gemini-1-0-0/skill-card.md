## Description: <br>
Gemini CLI for one-shot Q&A, summaries, and generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kenswj](https://clawhub.ai/user/kenswj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to invoke Gemini CLI for one-shot question answering, summarization, generation, model selection, JSON output, extension management, and initial authentication setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts sent through Gemini CLI may include secrets, private documents, or regulated data. <br>
Mitigation: Avoid sending sensitive data unless the Gemini account and data-handling path are approved for the environment. <br>
Risk: Gemini CLI extension-management commands can change local CLI behavior. <br>
Mitigation: Run extension-management commands only when the user explicitly intends to modify Gemini CLI extensions. <br>
Risk: The Homebrew gemini-cli package and Gemini provider account are external dependencies. <br>
Mitigation: Install and use the skill only when those external dependencies are trusted for the target environment. <br>


## Reference(s): <br>
- [Gemini developer documentation](https://ai.google.dev/) <br>
- [ClawHub skill page](https://clawhub.ai/kenswj/gemini-1-0-0) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON-formatted Gemini CLI output when the skill uses the CLI output-format option.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
