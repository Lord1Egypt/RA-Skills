## Description: <br>
Amplifier delegates complex tasks to a multi-agent framework for research, multi-file code work, architecture reviews, and other work that benefits from parallel specialist agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bkrabach](https://clawhub.ai/user/bkrabach) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use Amplifier to delegate complex research, implementation, review, and planning tasks to a multi-agent workflow when the work benefits from specialist agents or parallel investigation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill delegates task details to the Amplifier framework, which may involve privacy and session-retention considerations. <br>
Mitigation: Avoid sending secrets, credentials, regulated data, or private business material unless the configured Amplifier data handling and session retention behavior is understood and accepted. <br>
Risk: The skill installs and invokes the referenced Amplifier OpenClaw package. <br>
Mitigation: Install only after reviewing and trusting the referenced package and its configured dependencies. <br>


## Reference(s): <br>
- [Amplifier OpenClaw integration package](https://github.com/microsoft/amplifier-app-openclaw) <br>
- [ClawHub skill page](https://clawhub.ai/bkrabach/amplifier-openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Text or Markdown with optional shell command snippets and JSON status, usage, and cost details from Amplifier runs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include delegated task responses, error summaries, status values, session references, and estimated cost metadata.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
