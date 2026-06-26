## Description: <br>
Search, inspect, and progressively read open-access academic papers with the deepxiv CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xupeng8](https://clawhub.ai/user/xupeng8) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, developers, and technical readers use this skill to search arXiv, PMC, and Semantic Scholar, triage papers, inspect targeted sections, compare baselines, and build compact literature reviews without loading full papers too early. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing the external deepxiv-sdk package can modify the user's environment. <br>
Mitigation: Verify deepxiv availability first, stop if it is missing, and run package-manager or pip commands only after explicit user approval. <br>
Risk: DeepXiv agent mode can consume LLM account usage and may be slower or less predictable than manual paper-reading commands. <br>
Mitigation: Prefer manual search and paper commands by default; use agent mode only when the user agrees to LLM usage and cost. <br>
Risk: Paper summaries can become misleading if the agent makes claims from sections it has not read. <br>
Mitigation: State the progressive-reading rung used and verify section-level claims with targeted paper sections before presenting them. <br>


## Reference(s): <br>
- [DeepXiv install instructions](references/install.md) <br>
- [DeepXiv workflows](references/workflows.md) <br>
- [Deepxiv Cli on ClawHub](https://clawhub.ai/xupeng8/deepxiv-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompts the agent to state which progressive-reading rung informed its answer and to keep paper reads scoped to the user's question.] <br>

## Skill Version(s): <br>
0.2.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
