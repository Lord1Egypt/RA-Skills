## Description: <br>
Multi-stage deep research with reflection loops, multi-query retrieval, LLM chunk selection, and citation integrity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vardhineediganesh877-ui](https://clawhub.ai/user/vardhineediganesh877-ui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and researchers use this skill to turn broad research questions into cited reports, summaries, briefs, or structured JSON through staged planning, retrieval, analysis, reflection, and writing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research questions, prompts, and retrieved source text can be sent to configured search, GitHub, documentation, and LLM providers. <br>
Mitigation: Use mock/offline modes or a trusted local provider for sensitive work, and only configure providers approved for the data being researched. <br>
Risk: The skill can save research outputs, checkpoints, and source-derived artifacts locally. <br>
Mitigation: Run it in a sandboxed workspace and choose explicit output and checkpoint paths before execution. <br>
Risk: Generated reports may contain incorrect, stale, or weakly supported claims despite citation-oriented workflow controls. <br>
Mitigation: Review cited sources and verify citations before relying on generated reports for decisions. <br>


## Reference(s): <br>
- [Deep Research Pipeline documentation](DOCS.md) <br>
- [Deep Research Pipeline skill definition](SKILL.md) <br>
- [ClawHub release page](https://clawhub.ai/vardhineediganesh877-ui/deep-research-pipeline) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, summaries, briefs, structured JSON, and command/configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports report, summary, brief, and json outputs with optional checkpoints, mock mode, time limits, and token budgets.] <br>

## Skill Version(s): <br>
2.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
