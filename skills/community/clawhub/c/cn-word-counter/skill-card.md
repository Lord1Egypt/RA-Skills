## Description:

Counts whitespace-delimited words, characters, and lines in supplied text using a local Python script.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to count words, characters, and lines in Chinese or other supplied text locally without an API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive text supplied as a command-line argument may be exposed through shell history or local process inspection.

Mitigation: Avoid processing highly sensitive text through command-line arguments; adapt the invocation to read from a protected file or standard input if sensitive use is required.

Risk: The documentation is Chinese-only and includes promotional external links that are not required for runtime use.

Mitigation: Review the documented usage before deployment and rely on the local script path rather than promotional links when running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/cn-word-counter)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with shell command examples; the runtime script prints JSON counts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with the Python standard library and requires no API key.]

## Skill Version(s):

1.2.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
