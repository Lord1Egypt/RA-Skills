## Description:

clawgrep helps agents use a local grep-compatible CLI that combines semantic embedding search with keyword matching for code and document retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[schonhoffer](https://clawhub.ai/user/schonhoffer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search codebases, notes, and document folders when exact wording is unknown or plain grep misses relevant results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned installation commands can introduce ordinary package supply-chain risk.

Mitigation: Confirm the publisher and package source before installation, and prefer a pinned or reviewed release in controlled environments.

Risk: The first run downloads an embedding model from Hugging Face and writes a local cache.

Mitigation: Allow external model download only when expected, persist the cache for later offline use, and review cache location policies for the environment.

Risk: Semantic indexing may process private notes or repositories outside the intended scope.

Mitigation: Search only the specific directories intended for indexing, especially when working with private or sensitive content.

## Reference(s):

- [CLI reference](references/cli-reference.md)
- [Examples](references/examples.md)
- [clawgrep repository](https://github.com/Schonhoffer/clawgrep)
- [ClawHub skill page](https://clawhub.ai/schonhoffer/skills/clawgrep)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and grep-compatible text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results are one line per match in file:line:text form; context lines use grep-style separators.]

## Skill Version(s):

0.1.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
