## Description:

Review, validate, and generate code with AI-powered linting for fixing bugs, generating boilerplate, formatting, and running analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to log code review notes, validation results, code generation requests, formatting and linting passes, explanations, conversions, fixes, reports, and related activity. It also supports status checks, recent-entry views, full-text search, statistics, and exports of the locally stored records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist code-related notes, prompts, and other development text in plaintext local logs.

Mitigation: Do not enter secrets, tokens, private keys, regulated data, proprietary source, or other sensitive material unless plaintext local storage is acceptable.

Risk: Saved logs are searchable and exportable, which can make sensitive entries easier to redistribute.

Mitigation: Review log contents before using search results or exports, and remove sensitive entries from ~/.local/share/ai-code-helper before sharing files.

## Reference(s):

- [Ai Code Helper on ClawHub](https://clawhub.ai/ckchzh/skills/ai-code-helper)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Plain text command output with optional JSON, CSV, or text export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores timestamped plaintext logs and generated export files under ~/.local/share/ai-code-helper.]

## Skill Version(s):

2.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
