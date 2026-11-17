## Description:

case.dev helps agents install and use the casedev CLI for legal document vaults, OCR, transcription, and web, legal, case law, patent, and vault search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maxsonderby](https://clawhub.ai/user/maxsonderby)

### License/Terms of Use:


## Use Case:

External users and legal-workflow developers use this skill to set up the casedev CLI, authenticate to case.dev, manage encrypted vaults, extract text from documents, transcribe recordings, and run legal or web research through CLI commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes a curl-to-sh installer path.

Mitigation: Prefer the Homebrew installation path, or independently verify the shell script source before executing it.

Risk: Legal documents, directories, recordings, and document URLs may contain privileged or confidential information.

Mitigation: Upload only materials the user is authorized to send to case.dev after checking privacy, retention, and client-confidentiality requirements.

Risk: API keys may be stored in a local config file on shared machines.

Mitigation: Prefer CASE_API_KEY environment variables or a managed secret store, and avoid persistent local key storage on shared systems.

## Reference(s):

- [case.dev](https://case.dev)
- [ClawHub skill listing](https://clawhub.ai/maxsonderby/skills/casedev)
- [case.dev shell installer source](https://raw.githubusercontent.com/CaseMark/homebrew-casedev/main/install.sh)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks and JSON-oriented CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI commands usually request --json for machine-readable agent workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
