## Description: <br>
Automatically add technical jargon to the user's tech glossary GitHub repository when encountered during coding sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[emanxchan](https://clawhub.ai/user/emanxchan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to recognize unfamiliar technical terms during coding sessions and add concise, analogy-based glossary entries to a user's tech glossary repository. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically edit, commit, and push to a GitHub glossary repository from broad coding-session triggers without a clear approval step. <br>
Mitigation: Require the agent to show proposed glossary entries and local diffs first, then require explicit approval before any commit or git push. <br>


## Reference(s): <br>
- [Glossary Format Reference](references/glossary-format.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown glossary entries with inline code examples and git shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update a glossary file and propose or run git commit and push commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
