## Description:

Use when you need to call deployed Bobine modules with typed params or perform a signed Ed25519 call through an auth module.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ccamel](https://clawhub.ai/user/ccamel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to prepare typed Bobine contract parameters, execute unsigned calls, and perform signed Ed25519 calls against a Bobine server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Signed calls require reusable private key material to be supplied through command-line arguments.

Mitigation: Use only low-scope or disposable Bobine auth keys, avoid shared terminals and CI logs, and do not expose sigkey values in prompts or transcripts.

Risk: Inline spark generation is CPU-bound and accepts user-provided effort targets.

Mitigation: Keep --spark-effort to known small values and prefer a single deliberate --spark-hex only when a one-off spark is already available.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ccamel/skills/bobine-contract-caller)
- [Publisher Profile](https://clawhub.ai/user/ccamel)
- [Bobine Concept Overview](https://www.bobine.tech/)
- [Bobine Project](https://github.com/hazae41/bobine)
- [Standard Bobine Libraries](https://github.com/hazae41/stdbob)
- [Param Grammar](references/params.md)
- [Runtime and Environment](references/runtime.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON result descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Successful calls return one JSON object containing logs, a normalized tagged return value, spark hex, and reported sparks.]

## Skill Version(s):

0.1.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
