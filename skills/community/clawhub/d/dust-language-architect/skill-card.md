## Description: <br>
Expert Dust Language Architect grounded in the full Dust ecosystem, with the Dust Programming Language Specification as canon and all dustlang organization repositories treated as supporting corpus. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[litecreator](https://clawhub.ai/user/litecreator) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, documentation authors, and language designers use this skill to answer Dust language questions, review Dust architecture, and generate repository-grounded explanations or documentation from the Dust ecosystem corpus. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill intentionally directs the agent to consider all files in the Dust repositories, so unrelated private files or secrets could be exposed to agent reasoning if they are present. <br>
Mitigation: Install or run the skill only with Dust repository copies that have been reviewed to exclude secrets and unrelated private files. <br>


## Reference(s): <br>
- [Dust Programming Language Specification](https://github.com/dustlang/dustlang) <br>
- [Dust Compiler and Implementation Repository](https://github.com/dustlang/dust) <br>
- [Dust Website Repository](https://github.com/dustlang/dustlang.github.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown or plain text with repository-grounded explanations and code snippets when relevant] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should distinguish canonical specification facts from implementation evidence, tests, examples, public documentation, implications, and unresolved ambiguity.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
