## Description: <br>
Surveys an existing codebase to understand its structure, scope, architecture, and current state before planning or implementation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adelvillar1](https://clawhub.ai/user/adelvillar1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to orient an agent in an unfamiliar or long-neglected repository, survey architecture and project state, and produce a concise markdown report before planning or implementation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A repository survey can expose private project context or credential-adjacent details if the agent reads outside the intended scope. <br>
Mitigation: Keep the survey scoped to the intended repository and do not approve reads of local/private context or secret files unless that information is appropriate to use. <br>
Risk: The generated architecture or maintainability summary may be incomplete or misleading if source files are sampled too narrowly or stale documentation is treated as current. <br>
Mitigation: Review the synthesized report against the repository's current source, docs, and security guidance before using it for planning or implementation. <br>


## Reference(s): <br>
- [Codebase Survey Checklist](references/codebase-survey-checklist.md) <br>
- [Targeted Domain Deep Dive Checklist](references/targeted-deep-dive-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with command snippets, tables, and concise analysis] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Synthesizes findings instead of dumping raw files and includes cautions around secrets and private local context.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
