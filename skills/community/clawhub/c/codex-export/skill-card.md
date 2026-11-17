## Description:

Export Codex CLI or Codex Desktop sessions to Markdown transcripts, with options to list recent sessions, export by session ID, and omit tool-call details in brief mode.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinghan23](https://clawhub.ai/user/jinghan23)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to save, share, or review local Codex CLI and Codex Desktop sessions as Markdown transcripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Full transcript exports can include sensitive prompts, workspace paths, tool calls, and tool outputs.

Mitigation: Review exported Markdown before sharing it, use --brief to reduce sensitive detail, and avoid running the install command with elevated privileges.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jinghan23/skills/codex-export)
- [Relevant upstream Codex issue](https://github.com/openai/codex/issues/2880)

## Skill Output:

**Output Type(s):** [Markdown, Text, Files, Shell commands]

**Output Format:** [Markdown transcript to stdout or an output .md file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default exports can include tool calls and tool outputs; brief mode limits output to user and assistant messages.]

## Skill Version(s):

0.1.0 (source: release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
