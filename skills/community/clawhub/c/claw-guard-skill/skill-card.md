## Description:

Safety Guard URLs or files with the safety-guard CLI (web, PDFs, images, audio, YouTube).

This skill is ready for commercial/non-commercial use.

## Publisher:

[john-niu-07](https://clawhub.ai/user/john-niu-07)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run safety checks on URLs, local files, PDFs, images, audio, and YouTube links through the safety-guard CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the skill requires trusting an external Homebrew tap and third-party safety-guard binary.

Mitigation: Review the tap and binary source before installation and deploy only in environments where that third-party tool is approved.

Risk: Submitted files, URLs, extracted content, or metadata may be sent to selected model providers or optional Firecrawl and Apify services.

Mitigation: Do not run the skill on confidential, private, or regulated data unless those providers and optional services are approved for that data.

## Reference(s):

- [Safety Guard Homepage](https://safety-guard.sh)
- [ClawHub Skill Page](https://clawhub.ai/john-niu-07/skills/claw-guard-skill)
- [Publisher Profile](https://clawhub.ai/user/john-niu-07)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May provide JSON output when the safety-guard CLI is run with --json.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
