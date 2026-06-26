## Description: <br>
Audits an agent codebase against the 12-Factor Agents methodology and reports evidence-backed compliance findings and recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review LLM-powered agent architectures, compare implementations against the 12-Factor Agents methodology, and plan concrete improvements from file-level evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads a user-selected codebase and may include local file snippets in its analysis. <br>
Mitigation: Run it only on repositories you are authorized to review, and avoid pointing it at secrets or private material you do not want summarized. <br>
Risk: Architecture recommendations can be misleading if the cited evidence is incomplete or the reviewed codebase omits relevant files. <br>
Mitigation: Review cited paths, snippets, and recommendations before acting on the report. <br>


## Reference(s): <br>
- [12-Factor Agents](https://github.com/humanlayer/12-factor-agents) <br>
- [Per-Factor Analysis Framework](references/factors.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown analysis with summary tables, file citations, snippets, and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a codebase_path and can optionally use a docs_path; scoring is gated on cited evidence before Strong, Partial, or Weak ratings are assigned.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
