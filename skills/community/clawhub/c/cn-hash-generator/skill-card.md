## Description:

Generates MD5, SHA-1, SHA-256, SHA-512, and BLAKE2b hashes, Base64 encodes or decodes text, creates UUIDs, and produces HMAC signatures using Python standard libraries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill for local hash generation, Base64 transforms, UUID generation, and HMAC signing during development, testing, and documentation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: README usage examples name a script that is not present in the artifact.

Mitigation: Verify the intended entry point before installation or execution and use the packaged script path, scripts/cn_hash_generator.py, unless the publisher updates the examples.

Risk: Passing HMAC keys through the --hmac command-line option can expose secrets in shell history or process listings.

Mitigation: Use local or test data only, or adapt the workflow to read production secrets through a safer prompt, stdin, or secret manager pattern.

Risk: Some command help and branding text is Chinese-only.

Mitigation: Review the CLI messages and documentation with a Chinese reader or translation workflow before relying on them in an English-only operational process.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/cn-hash-generator)
- [Publisher profile](https://clawhub.ai/user/freedompixels)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text or Markdown with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stdlib-only local utility output; command examples should be checked against the packaged script name.]

## Skill Version(s):

1.2.8 (source: server release metadata; artifact frontmatter says 1.2.6)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
