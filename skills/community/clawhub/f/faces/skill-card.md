## Description:

Use this skill when the user wants to create, compile, or chat through a Face, compose personas with boolean formulas, compare minds by semantic similarity, import YouTube videos into a Face, or manage their Faces Platform account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sybileak](https://clawhub.ai/user/sybileak)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Faces to create and manage persona-like Faces from source materials, compile documents or transcripts, chat through those personas, compare semantic similarity, compose Faces with boolean formulas, and manage account credentials, billing, quotas, and API keys.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may send selected documents, transcripts, prompts, profile attributes, and account operations to the Faces Platform.

Mitigation: Confirm each upload or import with the user and avoid submitting passwords, API keys, SSNs, tax IDs, private addresses, or third-party personal data.

Risk: The skill can use account credentials and API keys for authenticated Faces Platform operations.

Mitigation: Prefer scoped, expiring API keys with budget limits over long-lived account credentials, and store credentials only through documented faces CLI configuration paths.

Risk: The CLI can perform billing, checkout, subscription, quota, and paid token-usage operations.

Mitigation: Require the human to complete payment or checkout steps in a browser and verify plan, balance, quota, and usage before running cost-incurring operations.

Risk: The security scan verdict is suspicious and notes under-disclosed or overbroad behavior around credentials, uploads, billing, OAuth, and persistent persona data.

Mitigation: Review the skill carefully before installing, verify the exact faces-cli package version and publisher, and disable or review local catalog persistence when privacy-sensitive.

## Reference(s):

- [Faces Skill on ClawHub](https://clawhub.ai/sybileak/skills/faces)
- [Quickstart](references/QUICKSTART.md)
- [Full command reference](references/REFERENCE.md)
- [Authentication & Registration](references/AUTH.md)
- [What is Faces](references/CONCEPTS.md)
- [OAuth - Connect ChatGPT](references/OAUTH.md)
- [Face Templates](references/TEMPLATES.md)
- [Accepted Attribute Keys](references/ATTRIBUTES.md)
- [Instruction Scope](references/SCOPE.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands commonly require the faces CLI, internet access, and a JWT or FACES_API_KEY; --json is used when structured command output is needed.]

## Skill Version(s):

1.6.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
