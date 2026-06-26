## Description: <br>
Pure-Python recursive memory recall for persistent AI agents using a manager-to-workers-to-synthesis RLM loop with HTTP calls to OpenAI-compatible LLM endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Stefan27-4](https://clawhub.ai/user/Stefan27-4) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent builders use DeepRecall to let persistent AI agents search scoped memory or workspace files, extract cited quotes, and synthesize grounded recall answers through configured LLM providers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read broad local memory or workspace files and send selected content to configured external LLM providers. <br>
Mitigation: Use memory-only scopes where possible, exclude sensitive directories and secrets, and verify provider settings before broad recall runs. <br>
Risk: Recall over project or all-workspace scopes may expose personal notes, project files, or other sensitive content. <br>
Mitigation: Run broad scopes only after confirming the workspace contents are appropriate to share with the selected provider. <br>


## Reference(s): <br>
- [DeepRecall homepage](https://github.com/Stefan27-4/DeepRecall) <br>
- [DeepRecall on ClawHub](https://clawhub.ai/Stefan27-4/deeprecall) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [String or Markdown with cited recall results and optional Python or shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recall results may include filename-and-line citations or DeepRecall status messages when no matching content is found.] <br>

## Skill Version(s): <br>
1.0.8 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
