## Description: <br>
Gemini CLI for one-shot Q&A, summaries, and generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andy27725](https://clawhub.ai/user/andy27725) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to ask one-shot questions, request summaries, generate text, select Gemini models, request JSON output, and manage Gemini CLI extensions from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and authenticated usage are sent through Gemini, which may be inappropriate for secrets or regulated data. <br>
Mitigation: Avoid sending secrets or regulated data unless that use is approved for the relevant Gemini account and environment. <br>
Risk: Extension-management commands and unsafe CLI flags can change Gemini CLI behavior or reduce safety controls. <br>
Mitigation: Use extension commands and unsafe flags only deliberately, and review planned commands before execution. <br>
Risk: The skill depends on the Homebrew gemini-cli package and the local gemini binary. <br>
Mitigation: Install only from trusted package sources and confirm the expected gemini binary is present before use. <br>


## Reference(s): <br>
- [Gemini AI Developer Documentation](https://ai.google.dev/) <br>
- [ClawHub Skill Page](https://clawhub.ai/andy27725/gemini-andy27725) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON-oriented Gemini CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gemini binary; the skill may direct the user through Gemini CLI authentication and extension-management commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
