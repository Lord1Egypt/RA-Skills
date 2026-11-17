## Description:

DeepRecall provides pure-Python recursive memory recall for persistent AI agents through a manager, worker, and synthesis RLM loop using HTTP calls to OpenAI-compatible LLMs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stefan27-4](https://clawhub.ai/user/stefan27-4)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use DeepRecall to let persistent OpenClaw agents search workspace memory and project files, extract source quotes, and synthesize cited recall answers through configured LLM providers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OpenClaw memory and selected workspace-derived file contents may be sent to the configured LLM provider.

Mitigation: Use the skill only in workspaces appropriate for external provider processing, and avoid workspaces containing secrets, private logs, or sensitive symlinks.

Risk: File-scope protections are weaker than documented, so identity or workspace scope may not be a strict privacy boundary.

Mitigation: Review the selected scope and workspace before use, and avoid relying on scope isolation until the scope enforcement and symlink validation issues are fixed.

## Reference(s):

- [DeepRecall ClawHub Skill Page](https://clawhub.ai/stefan27-4/skills/deeprecall)
- [DeepRecall GitHub Homepage](https://github.com/Stefan27-4/DeepRecall)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Text or Markdown with source citations, plus Python and shell snippets when showing usage.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns cited recall text or a DeepRecall status message; may call the user's configured LLM provider.]

## Skill Version(s):

1.0.8 (source: artifact/SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
