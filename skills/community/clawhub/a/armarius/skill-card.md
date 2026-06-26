## Description: <br>
Armarius applies a session-wide prompt-injection policy that classifies external content as data and instructs the agent to neutralize suspected injection attempts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tatlantis](https://clawhub.ai/user/tatlantis) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and security engineers use this skill to add prompt-injection defenses to OpenClaw and Python-based agent workflows, especially when processing tool outputs, web pages, emails, documents, or API responses. It is suited to users who want a strict always-on policy for separating user control instructions from untrusted external content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives itself broad session-wide authority for prompt-injection handling. <br>
Mitigation: Install only when a strict session-wide prompt-injection policy is desired, and review its behavior against the agent's existing instruction hierarchy before deployment. <br>
Risk: The skill requires full unredacted logging of suspicious content, which may expose sensitive files, emails, API responses, or private tool outputs. <br>
Mitigation: Redact secrets and use short excerpts instead of full verbatim payloads before using the skill with sensitive or private content. <br>
Risk: The README install and demo commands rely on an external package and repository. <br>
Mitigation: Inspect the external Armarius package or repository separately before running installation or demo commands. <br>


## Reference(s): <br>
- [Armarius GitHub repository](https://github.com/tatlantis/armarius) <br>
- [Armarius issues](https://github.com/tatlantis/armarius/issues) <br>
- [ClawHub skill listing](https://clawhub.ai/tatlantis/armarius) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline code and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May append full verbatim logs when suspected prompt injection is detected.] <br>

## Skill Version(s): <br>
1.1.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
